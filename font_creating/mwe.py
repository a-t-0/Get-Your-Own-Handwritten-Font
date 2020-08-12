# conda install -c conda-forge inkscape
# conda install scour
# https://www.commandlinefu.com/commands/view/2009/convert-a-svg-file-to-grayscale
# inkscape -f file.svg --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose
import re
import os
import fileinput
from PIL import Image
import cv2

# Doesn't work, creates a black square. Perhaps set a threshold to not convert rgb white/bright colors
def convert_svg_to_grayscale(filepath):
    # Read in the file
    with open(filepath, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = re.sub(r'rgb\(.*\)', 'black', filedata)

    # Write the file out again
    with open(filepath, 'w') as file:
      file.write(f'1{filedata}')
    
# opens inkscape, converts to grayscale but does not actually export to the output file again
def convert_svg_to_grayscale_inkscape(filepath):
    output_file = 'output.svg'
    #command = f'scour -i {filepath} -o output.svg'
    #command = f'scour -i {filepath} -o scrubbed.svg --enable-viewboxing --enable-id-stripping --enable-comment-stripping --shorten-ids --indent=none'
    #os.system(f'cmd /k {command}')
    
    command = f'inkscape -f {output_file} --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose --verb=FileQuit'
    #inkscape -f example.svg --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose --without-gui
    #inkscape -f example.svg --verb=org.inkscape.color.grayscale.noprefs
    os.system(f'cmd /k {command}')
    print(f'completed {command}')
   
# Pillow Image is not able to import .svg files
def grayscale(filepath):
    image = Image.open(filepath)
    cv2.imwrite(f'{filepath}', image.convert('L'))


# walks through png files and calls function to convert the png file to .svg
def main():
    filepath = 'example.svg'            
    convert_svg_to_grayscale_inkscape(filepath)
    print(f'method1')
    #convert_svg_to_grayscale(filepath)
    #grayscale(filepath)
                

if __name__ == '__main__':
    main()