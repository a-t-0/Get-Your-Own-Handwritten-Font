# conda install -c conda-forge fonttools
class CreateFont():
    def __init__(self):
        import os
        #os.system('cmd /k "fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"')
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"')
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "/font_creating/svgs2ttf.py" "/template_reading/font_in/example.json"')
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "/font_creating/svgs2ttf.py" "../template_reading/font_in/example.json"')
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "../font_creating/svgs2ttf.py" "../template_reading/font_in/example.json"')
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "../template_reading/font_in/example.json"')
        import os
        current= os.path.dirname(os.path.abspath(__file__))
        current= os.getcwd()
        path_to_fontforge= f'{current}/fontforge_portable/fontforge.bat'
        path_to_script = f'{current}/font_creating/svgs2ttf.py' 
        path_to_json = f'{current}/template_reading/font_in/example.json'
       
        print(f'current={current}')
        print(f'path_to_fontforge={path_to_fontforge}')
        print(f'isfile={os.path.isfile(path_to_fontforge)}')
        print(f'isfile={os.path.isfile(path_to_script)}')
        print(f'isfile={os.path.isfile(path_to_json)}')
        command = f'cmd /k "{path_to_fontforge}" -lang=py -script {path_to_script} {path_to_json}'
        print(f'command={command}')
        os.system(command)
        #os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"')
        
if __name__ == '__main__':
    main = CreateFont()

#fontforge_portable/fontforge -lang=py -script svgs2ttf.py template_reading/font_in/example.json
#fontforge_portable/fontforge --version
#"fontforge_portable/fontforge" --version
#"fontforge_portable/fontforge" -lang=py -script svgs2ttf.py template_reading/font_in/example.json"
#"fontforge_portable/fontforge" -lang=py -script "../font_creating/svgs2ttf.py" template_reading/font_in/example.json"
#"fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"
#"fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "/template_reading/font_in/example.json"
#"fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "../template_reading/font_in/example.json"

#"fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"