# Fontmaker
Makes your own font so you can create your own personal handwritten (latex) letters.

## Usage Instructions
0. Print the pdf page with the qr codes from `/template_creating/main.pdf`
1. Scan the pages (or take pics of them with your phone).
2. Run the latest `/template_reading/readXX.py`.
3. That should be it, now you have your font in `/showing_your_font/`. (TODO: call the python script that makes the font once all symbols are found and compile the latex example to show the font in a pdf.)

## Advanced Usage Instructions
0. Fill the `/template_creating/symbols.txt` with the symbols that you want in your font.
1. Compile the main.tex (you can just import this github to overleaf and press "compile"), or install Texmaker, open `main.tex` and press F6 F7.
2. Print the handwriting templated called `main.pdf` file with the qr codes.
3. Fill in the template and scan it.
4. Put the scanned images or scanned pdf into the `template_reading/in/` folder.
5. Create a python 3.6 environment in anaconda (see `readXX.py`) and run the latest `readXX.py` file.
6. TODO: Scan the extracted font symbols and actually create the font.

## list of package installation commands
Assumes python 3.6 environment is installed and activated.

```
conda create -n py36 python=3.6 anaconda
conda activate py36
```

The following libraries are used in the python and can directly be installed with anaconda commands:
```
conda install -c conda-forge inkscape
conda install numpy
conda install -c conda-forge poppler
conda install -c conda-forge fonttools
pip install pdf2image
pip install scour
pip install pyunpack
pip install patool
```

The following packages require a bit more effort:
### Pillow installation
Source:https://anaconda.org/conda-forge/pillow
Command:
```
conda install -c conda-forge pillow
```

### opencv installation
Used for cv2 Perhaps this also requires: https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads download and install visual studio 2015, 2017 and 2019, the instructions were tested on a device that had those already installed.

Source:https://stackoverflow.com/questions/42994813/installing-opencv-on-windows-10-with-python-3-6-and-anaconda-3-6

Command:
```
conda install -c menpo opencv
```
Verify opencv is installed correctly in anaconda prompt by creating a python file named `test.py` with content:
```
import cv2
print(cv2.__version__)
```
by browsing to the directory of the `test.py` file in anaconda prompt and executing it in the python 3.6 environment with command:
```
python test.py
```
It should return a version number like `3.3.1`.

### Pyzbar installation
Source: https://stackoverflow.com/questions/63296571/decode-a-qr-code-in-python-3-6-in-anaconda-4-8-3-on-64-bit-windows

Command:
```
pip install pyzbar
```
Then from source: https://www.microsoft.com/en-US/download/details.aspx?id=40784
download `vcredist_x64.exe` (if you have an 64 bit pc, for x86 pick the 32 bit version).
You don't even have to restart anaconda prompt and you can verify pyzbar with a python file named `test.py` with content:
```
from pyzbar.pyzbar import decode
decode(Image.open('test.png'))
```
Next include an image named `test.png` in the same folder as `test.py`.
You can execute  `test.py` in Anaconda prompt in a python 3.6 environment with command:
```
python test.py
```
It shouldn't output anything.