import wget
import os
import zipfile
import subprocess
import py7zr

# required manual commands:
# pip install zipfile
# pip install wget

# Script to automate the following commands
# Source: https://miktex.org/howto/deploy-miktex
# wget https://miktex.org/download/win/miktexsetup-x64.zip
# unzip miktexsetup-x64.zip
# miktexsetup --verbose --local-package-repository=./tempfolder --package-set=complete download

class InstallFontforge:
    
    # intializes object
    def __init__(self):
        self.fontforge_portable_dir = "./fontforge_portable"
        
        # get fontforge installer (SKIP)
        #url = 'https://github.com/fontforge/fontforge/releases/download/20200314/FontForge-2020-03-14-Windows.exe'
        
        #get the portable fontforge version
        url = 'https://sourceforge.net/projects/fontforgebuilds/files/x86_64/Portable/FontForge-mingw-w64-x86_64-e5275e-r1.7z'
        wget.download(url) 
        
        
        
        
    # walks through zip files and calls function to unpack the zip file
    def walk_through_zip_files(self,folder):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f[-3:]==".7z":
                if (('font' in f) or ('Font' in f)) and (('forge' in f) or ('Forge' in f)):
                    print('unsipping')
                    # with zipfile.ZipFile(f, 'r') as zip_ref:
                        # zip_ref.extractall() # 7z is not a zip file
                    
                    
                    # with py7zr.SevenZipFile(f, mode='r') as z:
                        # z.extractall() # decryption error 
                    #os.system(f'7z x {f} -oPath/to/Name' ) # error
                    print(f' done converting')
                    
                    #from subprocess import run
                    #run('C:\\Program Files\\7-Zip\\7zG.exe x'+ archive_name + ' -o' + folder_name_to_extract)`                    
                    from pyunpack import Archive
                    Archive(f).extractall(self.fontforge_portable_dir)
                    
    def make_portable_directory(self):
        import os
        if not os.path.exists(self.fontforge_portable_dir):
            os.makedirs(self.fontforge_portable_dir)
    
    def install_miktex_portable(self):
        process = subprocess.Popen([
        #miktexsetup --verbose --local-package-repository=./tempfolder --package-set=complete download
            'miktexsetup',   
            '--verbose',
            f'--local-package-repository={self.fontforge_portable_dir}',
            '--package-set=complete',
            'download'])

# executes this main code
if __name__ == '__main__':
       
    main = InstallFontforge()
    main.make_portable_directory()
    main.walk_through_zip_files("./")
    
    # main.install_miktex_portable()