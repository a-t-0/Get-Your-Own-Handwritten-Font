from template_creating.CreateTemplate import CreateTemplate
from template_reading.read14 import ReadTemplate
from font_creating.PngToSvg.convert_png_to_svg import ConvertPngToSvg
from font_creating.convert_svg_to_grayscale import ConvertSvgToGrayscale
from font_creating.CreateFont import CreateFont

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

class MakeHandwrittenFont:
    
    # intializes object
    def __init__(self,language,custom_symbols,has_miktex):
        self.language = language
        self.custom_symbols = custom_symbols
        self.has_miktex = has_miktex
        
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

    def pdf_exists(self):
        if os.path.isfile('./template_creating/main.pdf'):
            return True
        else:
            return False

    def has_pdf_in_input(self):
        pdf_input_folder = './template_reading/in/'
        if self.folder_has_filetype(pdf_input_folder,'.pdf'):
            return True
        else:
            return False
            
    def folder_has_filetype(self,folder,extension):
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath[-len(extension):]==extension:
                    return True
        return False

    def get_nr_of_input_images(self):
        input_folder = './template_reading/in/'
        extention_types = ['.png','.jpeg','.jpg']
        count = 0
        for i in range(0,len(extention_types)):
            count = count+self.count_folder_has_filetype(input_folder,extention_types[i])
        return count
        
    def count_folder_has_filetype(self,folder,extension):
        count = 0
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath[-len(extension):]==extension:
                    # only search specific folder and not subdirectories of folder
                    if not (('/' in filepath[len(folder):]) or ('\\' in filepath[len(folder):])):
                        print(f'found file = {filepath} and count = {count}')
                        count=count+1
        return count
        
    # creates the font from the scanned pages
    def create_font(self):
        
        if self.has_scanned_template():
            ReadTemplate()
        
            if self.found_all_symbols():
        
                # convert the font images to svg
                ConvertPngToSvg()        
                
                # convert svg to grayscale
                ConvertSvgToGrayscale('../template_reading/font_in/')
                
                # create json for font
                # TODO 
                
                # create font
                print(f'creating font')
                CreateFont()
                print(f'created font')
                
                # compile example latex to show font
                # TODO
            else:
                raise Exception (f'Please upload more/better scanned images, not all symbols were detected in the scans you provided.')
    
    def has_scanned_template(self):
        nr_pdf_pages = 3 # TODO: get actual nr of pages from compiled pdf or symbol spec
        nr_of_input_images = self.get_nr_of_input_images() 
        if self.has_pdf_in_input():
            return True
        elif nr_of_input_images>=nr_pdf_pages:
            return True
        else:
            raise Exception (f'Please provide more scanned input images of your filled in template (or a pdf) in folder:template_reading/in to start creating your font. There were only {nr_of_input_images} images found.')
            
    def found_all_symbols(self):
        max_nr_of_symbols= 100 # TODO: read from symbol_spec.txt
        found_symbols = []
        return True
        


    def create_pdf(self, input_filename, output_filename):
        string = f'latex -output-format=pdf -job-name="{input_filename}" "{output_filename}" -enable-installer'
        process = subprocess.Popen([string])
        process.wait()        

    def create_pdfV1(self, input_filename, output_filename):
        import subprocess as Popen
        import subprocess as sp
        #string = f'latex -output-format=pdf -job-name="{input_filename}" "{output_filename}" -enable-installer'
        string = f'latex -output-format=pdf -job-name="{input_filename}" -enable-installer'
        print(f'executing command={string}')
        
        os.system(f'cmd /k {string}')
        
    def create_pdfV2(self, input_filename, output_filename):
        process = subprocess.Popen([
            'latex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
            '-output-format=pdf',
            '-job-name=' + output_filename,
            input_filename,
            '-enable-installer'])

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
    
    # ask user which language the user wants to create
    language = "english"
    # ask user whether they created a custom set of symbols
    custom_symbols = False
    # ask if user has miktex installed already and can compile pdfs manually
    has_miktex = True
    main = MakeHandwrittenFont(language,custom_symbols, has_miktex)
    main.compile_pdf()
    main.create_font()