# conda install -c conda-forge inkscape
# https://www.commandlinefu.com/commands/view/2009/convert-a-svg-file-to-grayscale
# inkscape -f file.svg --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose
import re
import os
import fileinput
from PIL import Image
import cv2

# walks through png files and calls function to convert the png file to .svg
class ConvertSvgToGrayscale():
    def __init__(self,folder):
        print(folder)
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath=="example.svg":
                    print(f'ound file')
                    #convert_svg_to_grayscale_inkscape(os.path.join(root, file))
                    #convert_svg_to_grayscale(os.path.join(root, file))
                    grayscale(os.path.join(root, file))

# Doesn't work, creates a black square
def convert_svg_to_grayscale(filepath):
    # Read in the file
    with open(filepath, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = re.sub(r'rgb\(.*\)', 'black', filedata)

    # Write the file out again
    with open(filepath, 'w') as file:
      file.write(filedata)
    
# opens inkscape, converts to grayscale but does not actually export to the output file again
def convert_svg_to_grayscale_inkscape(filepath):
   command = f'inkscape -f {filepath} --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose'
   os.system(f'cmd /k {command}')
   
# Pillow Image is not able to import .svg files
def grayscale(filepath):
    image = Image.open(filepath)
    cv2.imwrite(f'{filepath}', image.convert('L'))
    
    
if __name__ == '__main__':
    main = ConvertSvgToGrayscale('../template_reading/font_in/')