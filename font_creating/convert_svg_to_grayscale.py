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
                        #convert_svg_to_grayscale(grayed_output_filepath)

# Doesn't work, creates a black square
def convert_svg_to_grayscale(filepath):
    # Read in the file
    with open(filepath, 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = re.sub(r'rgb\(.*\)', print_replacement(r'rgb\(.*\)'), filedata)

    # Write the file out again
    with open(filepath, 'w') as file:
      file.write(filedata)
      
def print_replacement(incoming):
    print(f'incoming={incoming}')
    return 'black'
    
# Doesn't work, creates a black square
def convert_svg_to_grayscale_V0(filepath):
    # Read in the file
    with open(filepath, 'r') as file :
      filedata = file.read()

    # Replace the target string
    patterns = [[(m.group(0)), m.start(0), m.end(0)] for m in re.finditer(r'rgb\(.*\)', filedata) ]
    
    # swap the patterns
    modified_filedata = swap_pattern_V1(filedata,patterns)
    lines = modified_filedata.splitlines()
    
    # remove lines longer than 300 and lines that were filtered by merging rgb>249 to black
    filtered = []
    for i in range(0,len(lines)):
        if not "fill:black" in lines[i]:
                filtered.append(lines[i])
    merged = "".join(str(x) for x in filtered)
    
    # Write the file out again
    with open(filepath, 'w') as file:
      file.write(merged)
       
# takes a string and a list of patterns consisting of a string in element one, 
# and a tuple with start and end index in the original string of the pattern in element 2.
# Then replaces the patterns in the original string with something else.
def swap_pattern_V1(original_string,patterns):
    modified=""
    same_strs = []
    middles =[]   
    concat = []
    start_same = 0
    
    # loop through the patterns that contain the rgb codes
    for i in range(0,len(patterns)):
        
        # the end characters of the substring that is literally copied from the original string
        end_same = int(patterns[i][1])
                
        # get list of parts that remain the same
        same_strs.append(original_string[start_same:end_same])
        
        # get list of middle parts
        middles.append(filter_rgbcodes(patterns[i][0]))
        
        # set start for new filler as end of previous middle
        start_same = int(patterns[i][2])
    
    # get last filler/same substring from original
    same_strs.append(original_string[start_same:])
    
    # go through list of parts that reamin the same, put middle in, put same after
    for i in range(0,len(middles)):
    #for i in range(0,10):        
        concat.append(same_strs[i])
        concat.append(middles[i])
    
    concat.append(same_strs[-1])
    return "".join(str(x) for x in concat)

# returns "black" if the rgb codes are close to white values >249    
def filter_rgbcodes(rgb_str):
    remove_left = rgb_str[4:]
    nrs = remove_left[:-1]
    
    red = nrs.split(',')[0]
    green = nrs.split(',')[1]
    blue = nrs.split(',')[2]
    
    if int(red)>249 and int(green)>249 and int(blue)>249:
        return 'black'
    return rgb_str
    
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