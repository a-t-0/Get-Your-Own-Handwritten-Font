# conda install -c conda-forge fonttools
import os

# runs a fontforge command to generate an actual font based on the .svg and .json files in template_reading/font_in/
class CreateFont():
    def __init__(self,path):        
        
        path_to_fontforge= f'{path}/fontforge_portable/fontforge.bat'
        path_to_script = f'{path}/font_creating/svgs2ttf.py' 
        path_to_json = f'{path}/template_reading/font_in/example.json'
        if self.all_files_exist([path_to_fontforge,path_to_script,path_to_json]):
            command = f'cmd /k "{path_to_fontforge}" -lang=py -script {path_to_script} {path_to_json}'
            print(f'command={command}')
            os.system(command)
    
    def all_files_exist(self,files):
        for file in files:
            if not os.path.isfile(file):
                raise Exception (f'file {file} does not exist yet it is needed to create the font.')
        return True

    def modify_json(self,json_path):
        # read the json file content
        
        # find the , "glyphs":{} line.
        
        # find the list of symbols as a list with one character per element
        
        # find the asci code of the character
        
        # find the filename of the character
        
        # generate the glyphs line
        
        # merge the glyphs lines
        
        # write the glyphs lines back to the json file
       
if __name__ == '__main__':
    filepath = os.getcwd() # gets path of parent script that is running
    parent_filepath= os.path.abspath(os.path.join(filepath, os.pardir))
    main = CreateFont(parent_filepath)

