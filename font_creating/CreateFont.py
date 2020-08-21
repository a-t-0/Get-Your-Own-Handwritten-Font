# conda install -c conda-forge fonttools
import os

# runs a fontforge command to generate an actual font based on the .svg and .json files in template_reading/font_in/
class CreateFont():
    def __init__(self):        
        current= os.getcwd() # gets path of parent script that is running
        path_to_fontforge= f'{current}/fontforge_portable/fontforge.bat'
        path_to_script = f'{current}/font_creating/svgs2ttf.py' 
        path_to_json = f'{current}/template_reading/font_in/example.json'
       
        command = f'cmd /k "{path_to_fontforge}" -lang=py -script {path_to_script} {path_to_json}'
        print(f'command={command}')
        os.system(command)
        
if __name__ == '__main__':
    main = CreateFont()

