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
        os.system('cmd /k "/fontforge_portable/fontforge" -lang=py -script "font_creating/svgs2ttf.py" "template_reading/font_in/example.json"')
        
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