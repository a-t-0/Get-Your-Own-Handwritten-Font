import wget
import os
import zipfile
import subprocess

# required manual commands:
# pip install zipfile
# pip install wget

# Script to automate the following commands
# Source: https://miktex.org/howto/deploy-miktex
# wget https://miktex.org/download/win/miktexsetup-x64.zip
# unzip miktexsetup-x64.zip
# miktexsetup --verbose --local-package-repository=./tempfolder --package-set=complete download

class InstallMiktex:
    
    # intializes object
    def __init__(self):
        self.miktex_portable_dir = "./miktex_portable"
        url = 'https://miktex.org/download/win/miktexsetup-x64.zip'
        #wget.download(url) 
        
        
        
        
    # walks through zip files and calls function to unpack the zip file
    def walk_through_zip_files(self,folder):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f[-4:]==".zip":
                print('unsipping')
                with zipfile.ZipFile(f, 'r') as zip_ref:
                    zip_ref.extractall()
                print(f' done converting')
    
    def make_miktex_portable_directory(self):
        import os
        if not os.path.exists(self.miktex_portable_dir):
            os.makedirs(self.miktex_portable_dir)
    
    def install_miktex_portable(self):
        process = subprocess.Popen([
        #miktexsetup --verbose --local-package-repository=./tempfolder --package-set=complete download
            'miktexsetup',   
            '--verbose',
            f'--local-package-repository={self.miktex_portable_dir}',
            '--package-set=complete',
            'download'])

# executes this main code
if __name__ == '__main__':
       
    main = InstallMiktex()
    main.walk_through_zip_files("./")
    main.make_miktex_portable_directory()
    main.install_miktex_portable()