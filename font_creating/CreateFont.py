# conda install -c conda-forge fonttools
import os
import codecs
from shutil import copyfile

# runs a fontforge command to generate an actual font based on the .svg and .json files in template_reading/font/
class CreateFont():
    def __init__(self,path):        
        
        self.path = path
        path_to_fontforge= f'{self.path}/fontforge_portable/fontforge.bat'
        path_to_script = f'{self.path}/font_creating/svgs2ttf.py' 
        #path_to_json = f'{self.path}/template_reading/font/example.json'
        self.path_to_symbols = f'{self.path}/template_creating/symbols.txt'
        
        self.json_example_source = f'{self.path}/template_reading/test_data/example.json'
        self.json_example_target = f'{self.path}/template_reading/font/example.json'
        
        # verify required files exist
        if self.all_files_exist([path_to_fontforge,path_to_script,self.json_example_source,self.path_to_symbols]):
            self.export_json()
            self.modify_json(self.json_example_target)
                    
            command = f'cmd /k "{path_to_fontforge}" -lang=py -script {path_to_script} {self.json_example_target}'
            print(f'command={command}')
            os.system(command)
    
    def all_files_exist(self,files):
        for file in files:
            if not os.path.isfile(file):
                raise Exception (f'file {file} does not exist yet it is needed to create the font.')
        return True

    def export_json(self):
        if os.path.exists(self.json_example_source):
            copyfile(self.json_example_source, self.json_example_target)
        else:
            raise Exception (f' could not find testfile in location:{source_file}')

    def modify_json(self,json_path):
        
        # read the json file content
        lines = self.read_file_content(json_path)
        print(lines)
        
        # find the , "glyphs":{} line.
        [glyphs_line_index,glpyhs_line] = self.get_glyps_line_and_index(lines)
        print(f'[glyphs_line_index,glpyhs_line]={[glyphs_line_index,glpyhs_line]}')
        
        # find the list of symbols as a list with one character per element
        [symbol_indices,symbols] = self.get_symbols_list()
        print(symbol_indices)
        print(symbols)
        
        # find the asci code of the character
        #asci_indices_symbols =  list(map(lambda x: ord(x), symbols))
        asci_indices_symbols =  list(map(lambda x: hex(ord(x)), symbols))
        print(asci_indices_symbols)
        
        # find the filename of the character
        svg_filenames = list(map(lambda x: f'{x}_grayed.svg', symbol_indices))
        svg_paths = list(map(lambda x: f'{self.path}/template_reading/font/{x}', svg_filenames))
        self.all_files_exist(svg_paths)
        
        # generate the glyphs line
        glyphs_lines = self.generate_glyphs_lines(asci_indices_symbols,svg_filenames)
        print(f'\n\n\nglyphs_lines={glyphs_lines}')
        
        
        # merge the glyphs lines
        merged_lines = self.merge_glyphs_lines(lines,glyphs_line_index,glyphs_lines)
        single_string_merged_lines = "\n".join(str(x) for x in merged_lines)
        print(merged_lines)
        # write the glyphs lines back to the json file
        #self.write_merged_lines_to_target_json(self.json_example_target,single_string_merged_lines)
        self.write_merged_lines_to_target_json(self.json_example_target,merged_lines)
        pass
        
    def write_merged_lines_to_target_json(self,target_filepath,merged_lines):
        # Write the file out again
        with open(target_filepath, 'w') as file:
            for i in range(0, len(merged_lines)):
                print(f' writing={merged_lines[i]}')
                file.write(merged_lines[i]+'\n')
    
    def merge_glyphs_lines(self,lines,glyphs_line_index,glyphs_lines):
        merged_lines = []
        for i in range(0,len(lines)):
            if not i == glyphs_line_index:
                merged_lines.append(lines[i])
            else:
                #merged_lines.append(glyphs_lines)
                for line in glyphs_lines: # can do this with recursion to this method
                    merged_lines.append(line)
        return merged_lines
        
    def generate_glyphs_lines(self,asci_indices_symbols,svg_filenames):
        lines = []
        lines.append(f', "glyphs":{{')
        for i in range(0,len(asci_indices_symbols)):
            if i==0:
                lines.append(f'"{asci_indices_symbols[i]}": {{ "src": "{svg_filenames[i]}", "width": 128}}')
            else:
                lines.append(f', "{asci_indices_symbols[i]}": {{ "src": "{svg_filenames[i]}", "width": 128}}')
        lines.append(f'}}')
        return lines
        
    # returns a list of symbols with 1 symbol per element.
    def get_symbols_list(self):
        symbols = []
        indices = []
        lines = self.read_file_content(self.path_to_symbols)
        for line in lines:
            if line[-2]==" " and line[-3] =="=":
                symbols.append(line[-1])
                indices.append(int(line.split("=")[0]))
            else:
                raise Exception(f'There appears to be an error in the formatting of file {self.path_to_symbols}.\n\nPlease ensure it follows syntax: <number><space><=><space><symbol>.\n\n In particular the following line is incorrect:{line}')
        return [indices,symbols]
        
    def read_file_content(self,filepath):
        # Read in the file
        with open(filepath, 'r') as file :
          filedata = file.read()  
        return filedata.splitlines()
        
    def get_glyps_line_and_index(self,lines):
        count = 0
        for line in lines:
            if ', "glyphs":{}' in line:
                return [count,line]
            count = count+1
        raise Exception(f'Did not find the , "glyphs": line even though it was expected')
        
if __name__ == '__main__':
    filepath = os.getcwd() # gets path of parent script that is running
    parent_filepath= os.path.abspath(os.path.join(filepath, os.pardir))
    main = CreateFont(parent_filepath)

