# conda install -c conda-forge inkscape
# https://www.commandlinefu.com/commands/view/2009/convert-a-svg-file-to-grayscale
# inkscape -f file.svg --verb=org.inkscape.color.grayscale --verb=FileSave --verb=FileClose
import re
import os
import fileinput
from PIL import Image
import cv2
from shutil import copyfile

# walks through png files and calls function to convert the png file to .svg
class ConvertSvgToGrayscale():
    def __init__(self,folder='../template_reading/font_in/'):
        print(f'folder={folder}')
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                grayed_output_filepath =f'{filepath[:-4]}_grayed{filepath[-4:]}'
                if filepath[-4:] == ".svg" and filepath[-11:] != "_grayed.svg":
                    print(f'filepath={filepath} and grayed_output_filepath={grayed_output_filepath}')
                    if not os.path.exists(grayed_output_filepath):
                        copyfile(filepath, grayed_output_filepath)
                        print(f'created copy')
                        #convert_svg_to_grayscale_inkscape(os.path.join(root, file))
                        #convert_svg_to_grayscale(os.path.join(root, file))
                        #grayscale(grayed_output_filepath)
                        #grayscale(filepath)
                        #convert_svg_to_grayscale(grayed_output_filepath)
                        #convert_svg_to_grayscale_inkscape(grayed_output_filepath)
                        #grayscale(grayed_output_filepath)
                        convert_svg_to_grayscale_V0(grayed_output_filepath)

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
    
# Doesn't work, creates a black square
def convert_svg_to_grayscale_V0(filepath):
    # Read in the file
    with open(filepath, 'r') as file :
      filedata = file.read()

    # Replace the target string
    #patterns = re.finditer(r'rgb\(.*\)', filedata) 
    patterns = [[(m.group(0)), m.start(0), m.end(0)] for m in re.finditer(r'rgb\(.*\)', filedata) ]
    #print(f'patterns={patterns}')
    
    modified_filedata = swap_pattern(filedata,patterns)
    
    # Write the file out again
    print(f'writing modified to={filepath}')
    with open(filepath, 'w') as file:
      file.write(modified_filedata)    
    exit()
    
# takes a string and a list of patterns consisting of a string in element one, 
# and a tuple with start and end index in the original string of the pattern in element 2.
# Then replaces the patterns in the original string with something else.
def swap_pattern(original_string,patterns):
    modified = original_string
    count = 0
    for i in range(0,len(patterns)):
        string = patterns[i][0]
        start_index = int(patterns[i][1])
        end_index = int(patterns[i][2])
        #print(f'pattern={patterns[i]}')
        print(f'string={string},start_index={start_index}, end_index={end_index}')
        remove_left = string[4:]
        nrs = remove_left[:-1]
        #nrs = "123,546,788"
        red = nrs.split(',')[0]
        green = nrs.split(',')[1]
        blue = nrs.split(',')[2]
        #print(f'remove_left ={remove_left },remove_right={nrs}')
        #print(f'red={red},green={green},blue={blue}')
        if int(red)>249 and int(green)>249 and int(blue)>249:
            patterns[i][0] = 'black'
            print(f'before={modified[start_index:end_index]}')
            count = end_index-start_index - len(patterns[i][0])
            lhs = modified[:start_index-count]
            rhs = modified[end_index-count:]
            modified = f'{lhs}{patterns[i][0]}{rhs}'
            print(f'after={modified[start_index:end_index]}')
            
            #print(f'string={patterns[i][0]},start_index={start_index}, end_index={end_index}')
        else:
            patterns[i][0] = 'w'
            #print(f'string={patterns[i][0]},start_index={start_index}, end_index={end_index}')
        
        
    return modified
    
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