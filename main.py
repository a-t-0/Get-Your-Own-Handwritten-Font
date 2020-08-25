from template_creating.CreateTemplate import CreateTemplate
from template_reading.read14 import ReadTemplate
from font_creating.PngToSvg.convert_png_to_svg import ConvertPngToSvg
from font_creating.convert_svg_to_grayscale import ConvertSvgToGrayscale
from font_creating.CreateFont import CreateFont

from shutil import copyfile
import pickle
import os
# Source: https://anaconda.org/conda-forge/miktex
#conda install -c conda-forge miktex
import subprocess

# Source: https://miktex.org/howto/deploy-miktex
# pip install wget
# conda install -c menpo 7zip
# wget https://miktex.org/download/win/miktexsetup-x64.zip
# unzip miktexsetup-x64.zip
# miktexsetup --verbose --local-package-repository=C:\temp\miktex --package-set=complete download

# Performs the steps to convert your handwriting into a font, from start to finish.
class MakeHandwrittenFont:
    
    # intializes object
    def __init__(self,language,custom_symbols,has_miktex,fill_missing_png=False,fill_missing_svg=False,artificial_svgs=False,overwrite_existing_svgs=True):
        self.language = language
        self.custom_symbols = custom_symbols
        self.has_miktex = has_miktex
        
        ## Specifications that are outputed by the template creating module
        self.nrOfSymbols = None
        self.boxWidth = None
        self.boxHeight = None
        self.nrOfBoxesPerLine = None
        self.nrOfBoxesPerLineMinOne = None
        self.nrOfLinesInTemplate = None
        self.nrOfLinesInTemplateMinOne = None
        self.maxNrOfLinesPerPage = None
        self.fill_missing_png = fill_missing_png
        self.fill_missing_svg = fill_missing_svg
        self.artificial_svgs = artificial_svgs
        self.overwrite_existing_svgs = overwrite_existing_svgs
        self.substituted_pngs = None
        
        ## hardcode script parameters
        # relative qr specification file location
        self.spec_filename = 'symbol_spec.txt'
        self.spec_loc = f'template_creating/{self.spec_filename}'
        
        # Remove testfiles
        self.test_handwritten_svg = 'template_reading/test_data/0.svg'
        self.test_computer_svg = 'template_reading/test_data/small.svg'
        self.test_handwritten_png = 'template_reading/test_data/0.png'
        
        self.remove_copied_test_files('.png')
        self.remove_copied_test_files('.svg')
        
        # read symbol specifications from symbol_spec.txt
        self.read_image_specs()
        
    # Compiles the pdf with the symbols
    def compile_pdf(self):
        # first output the font settings to a symbol_spec.txt file
        CreateTemplate('template_creating/')
        #os.system('cmd /k "pdflatex template_creating/main.tex')
        #self.create_pdf( 'template_creating/main.tex', 'template_creating/main.pdf')
        
        #self.create_pdfV1('template_creating/main.tex', 'template_creating/main.pdf')
        #self.create_pdfV1('/template_creating/main.tex', '/template_creating/main.pdf')
        #self.create_pdfV2('template_creating/main.tex', 'template_creating/main.pdf')
        #self.create_pdfV3('template_creating/main.tex', 'template_creating/main.pdf')
        
        # check if the pdf can be compiled automatically
        if not self.has_miktex:
            self.compile_pdf()
        elif self.pdf_exists():
            print(f'You can print the pdf template now and fill it. But please check if it contains all the symbols you want it to contain since this was just the default pdf that was in the repository.')

    # read image specs from the specifications txt file
    def read_image_specs(self):
        file1 = open(self.spec_loc, 'r') 
        Lines = file1.readlines() 
        self.nrOfSymbols = self.rhs_val_of_eq(Lines[0])
        self.boxWidth = self.rhs_val_of_eq(Lines[1])
        self.boxHeight = self.rhs_val_of_eq(Lines[2])
        self.nrOfBoxesPerLine = int(self.rhs_val_of_eq(Lines[3]))
        self.nrOfBoxesPerLineMinOne = self.rhs_val_of_eq(Lines[4])
        self.nrOfLinesInTemplate = int(self.rhs_val_of_eq(Lines[5]))
        self.nrOfLinesInTemplateMinOne = self.rhs_val_of_eq(Lines[6])
        self.maxNrOfLinesPerPage = int(self.rhs_val_of_eq(Lines[7]))
    
    # returns the integer value of the number on the rhs of the equation in the line
    def rhs_val_of_eq(self, line):
        start_index = line.find(' = ')
        rhs = line[start_index:]
        return ''.join(x for x in rhs if x.isdigit())

    # returns true if a file named main.pdf exists in subdir template_creating
    def pdf_exists(self):
        if os.path.isfile('./template_creating/main.pdf'):
            return True
        else:
            return False

    # returns True if the a pdf is in the input folder.
    # TODO: refactor to folder_has_filetype()
    def has_pdf_in_input(self):
        pdf_input_folder = './template_reading/in/'
        if self.folder_has_filetype(pdf_input_folder,'.pdf'):
            return True
        else:
            return False
            
    # returns true if a certain file extension is in some folder
    def folder_has_filetype(self,folder,extension):
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath[-len(extension):]==extension:
                    return True
        return False

    # Counts the combined number of images of types png jpeg and jpg in the input folder
    # and returns that number as integer
    def get_nr_of_input_images(self):
        input_folder = './template_reading/in/'
        extension_types = ['.png','.jpeg','.jpg']
        count = 0
        for i in range(0,len(extension_types)):
            count = count+self.count_folder_has_filetype(input_folder,extension_types[i])
        return count
    
    # Returns integer of how often a file with given file extension occurs in a specific folder.
    # subdirectories of the folder are excluded from the search.
    def count_folder_has_filetype(self,folder,extension):
        return len(self.get_filenames_in_folder(folder,extension))
        
    # Returns string of filename without dot without extension per file with given file extension occurs in a specific folder.
    # subdirectories of the folder are excluded from the search.
    def get_filenames_in_folder(self,folder,extension):
        filenames = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath[-len(extension):]==extension:
                    # only search specific folder and not subdirectories of folder
                    if not (('/' in filepath[len(folder):]) or ('\\' in filepath[len(folder):])):
                        filenames.append(self.get_filename_from_path(filepath,extension))
        return filenames
        
    # returns the filename of a path without file extension        
    def get_filename_from_path(self,path,extension):
        
        # remove file extension from file path
        string = path[:-len(extension)]
        
        # find the last /,//,\\ or \ in the filepath (without the extension)
        indices = [string[::-1].find('\\\\'),string[::-1].find('\\'),string[::-1].find('/'),string[::-1].find('//')]
        
        # return the end of the path without the extension back left towards the last(right to left) occurrence of the /,//,\\,\
        min_pos_index = min(i for i in indices if i > 0)
        
        # return filename
        return string[-min_pos_index:]    
        
        
    # creates the font from the scanned pages
    def create_font(self):
        
        # checks if the input folder contains a template
        if self.has_scanned_template():
            ReadTemplate()
            print(f'self.fill_missing_png={self.fill_missing_png}')
            
            if self.found_all_symbols('.png') or self.fill_missing_png:
                # Check if the symbols should be suplemented for testing purposes.
                if not self.found_all_symbols('.png'):
                    print(f'suplementing the following missing files ={self.find_missing_symbols(".png")}')
                    self.supplement_pngs_for_testing(self.test_handwritten_png,'.png')
                
                # convert the font images to svg
                ConvertPngToSvg('template_reading/font_in/',self.overwrite_existing_svgs)        
                
                
                # found the svg files                
                if self.found_all_symbols('.svg') or self.fill_missing_svg:
                    # Check if the symbols should be suplemented for testing purposes.
                    if not self.found_all_symbols('.svg'):
                        print(f'suplementing the following missing files ={self.find_missing_symbols(".svg")}')
                        if self.artificial_svgs:
                            print(f' substituting artificial svg from: {self.test_computer_svg}')
                            self.supplement_pngs_for_testing(self.test_computer_svg,'.svg')
                        else: 
                            self.supplement_pngs_for_testing(self.test_handwritten_svg,'.svg')
                    
                    # convert svg to grayscale
                    # TODO: change to font instead of font_in
                    ConvertSvgToGrayscale('template_reading/font_in/')
                        
                    # create json for font
                    # TODO 
                    
                    
                    # create font
                    print(f'creating font')
                    #CreateFont()
                    print(f'created font')
                else:
                    raise Exception (f'Not all png files were converted to svg files.\n In particular the missing symbol numbers are:{self.find_missing_symbols(".svg")}')
            
                # compile example latex to show font
                # TODO
            else:
                raise Exception (f'Please upload more/better scanned images, not all symbols were detected in the scans you provided.\n In particular the myssing symbol numbers are:{self.find_missing_symbols(".png")}')

    # injects multiple png files for testing purposes
    def supplement_pngs_for_testing(self,source_file,extension):
        copied_test_pngs_pickle_path = 'template_reading/test_data/copied_pngs.pkl'
        
        missing_symbols = self.find_missing_symbols(extension)
        # export list of copied files to test directory for removal upon next run.
        with open(f'template_reading/test_data/copied_{extension[1:]}s.pkl', 'wb') as f:
            pickle.dump(missing_symbols, f)
        
        # copy file 0.png from 'template_reading\test_data' to 'template_reading/font'
        # rename file from 0.png to <i><extension>
        for i in missing_symbols:
            if os.path.exists(source_file):
                copyfile(source_file, f'template_reading/font/{i}{extension}')
            else:
                raise Exception (f' could not find testfile in location:{source_file}')
                
    # removes injected test png files at start of run.
    def remove_copied_test_files(self,extension):
        copied_test_pngs_pickle_path = f'template_reading/test_data/copied_{extension[1:]}s.pkl'
        if os.path.exists(copied_test_pngs_pickle_path):
            with open(copied_test_pngs_pickle_path, 'rb') as f:
                copied_test_pngs = pickle.load(f)
                print(f'copied_test_pngs={copied_test_pngs}')
                for i in copied_test_pngs:
                    print(f' removing i={i}')
                    if os.path.exists(f'template_reading/font/{i}{extension}'):
                        os.remove(f'template_reading/font/{i}{extension}')
            os.remove(copied_test_pngs_pickle_path)
            
                

    
    # Checks whether the input has a pdf or at least as many images as there are pages in the template.
    # Does NOT check if all pages in the template are present.
    # TODO: Get the actual number of pages from the symbol_spec.txt file
    # Asks user to supply at least as much images as there are pages in the template before proceding. pdf always proceeds to decoding qrcodes.
    def has_scanned_template(self):
        nr_pdf_pages = 3 # TODO: get actual nr of pages from compiled pdf or symbol spec
        nr_of_input_images = self.get_nr_of_input_images() 
        if self.has_pdf_in_input():
            return True
        elif nr_of_input_images>=nr_pdf_pages:
            return True
        else:
            raise Exception (f'Please provide more scanned input images of your filled in template (or a pdf) in folder:template_reading/in to start creating your font. There were only {nr_of_input_images} images found.')

    def find_missing_symbols(self,extension):
        found_symbols = []    
        missing_symbols = []
        
        # Check which .png symbols are present in template_reading/in/
        filenames = self.get_filenames_in_folder('./template_reading/font/',extension)
        
        # Check which .svg symbols are present in template_reading/in/
        for i in range(1,int(self.nrOfSymbols)): # symbol indices start at 1.
            #print(f'{str(i)} is not in \n {filenames} is=\n{not str(i) in filenames}')
            if not str(i) in filenames:
                missing_symbols.append(i)
        return missing_symbols
            
    # Checks if all symbols are found by the decoder.
    # TODO: implement
    def found_all_symbols(self,extension):
        if len(self.find_missing_symbols(extension)) == 0:
            return True
        else:
            print(f'missing_symbols={self.find_missing_symbols(extension)}')
            return False
        

    # Automatically compiles the pdf template that the users can print and fill in
    # TODO: make it work on the automatically installed miktex
    def create_pdf(self, input_filename, output_filename):
        string = f'latex -output-format=pdf -job-name="{input_filename}" "{output_filename}" -enable-installer'
        process = subprocess.Popen([string])
        process.wait()        

    # Second attempt to compile the the pdf template that the users can print and fill in
    # TODO: make it work on the automatically installed miktex
    def create_pdfV1(self, input_filename, output_filename):
        import subprocess as Popen
        import subprocess as sp
        #string = f'latex -output-format=pdf -job-name="{input_filename}" "{output_filename}" -enable-installer'
        string = f'latex -output-format=pdf -job-name="{input_filename}" -enable-installer'
        print(f'executing command={string}')
        
        os.system(f'cmd /k {string}')

    # Second attempt to compile the the pdf template that the users can print and fill in
    # TODO: make it work on the automatically installed miktex            
    def create_pdfV2(self, input_filename, output_filename):
        process = subprocess.Popen([
            'latex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
            '-output-format=pdf',
            '-job-name=' + output_filename,
            input_filename,
            '-enable-installer'])

    # Second attempt to compile the the pdf template that the users can print and fill in
    # TODO: make it work on the automatically installed miktex
    def create_pdfV3(self, input_filename, output_filename):
        #pdflatex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #XeLaTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #laTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #MikTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #pdfTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #LuaTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        #MikTex -output-format=pdf -job-name="template_creating/main.pdf" "template_creating/main.tex" -enable-installer
        argList = [
            'pdflatex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
            #'XeLaTeX',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
            '-output-format=pdf',
            '-job-name=' + output_filename,
            input_filename,
            '-enable-installer',
            '-interaction nonstopmode']
        print(f'argList={argList}')
        process = subprocess.Popen(argList)                
    
    
  
# executes this main code
if __name__ == '__main__':
    import cv2
    print(cv2.__version__)
        
    # ask user which language the user wants to create
    language = "english"
    # ask user whether they created a custom set of symbols
    custom_symbols = False
    # ask if user has miktex installed already and can compile pdfs manually
    has_miktex = True
    # Fills missing png (and/or svg) pictures for testing purposes
    fill_missing_png = True
    fill_missing_svg = True
    artificial_svgs = True # uses svg of a letter designed in some font tool creator. Very small file of few kb/bytes
    overwrite_existing_svgs = False # speeds up main process by skipping already created svgs
    
    main = MakeHandwrittenFont(language,custom_symbols, has_miktex,fill_missing_png,fill_missing_svg,artificial_svgs,overwrite_existing_svgs)
                                
    main.compile_pdf()
    main.create_font()