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

#https://miktex.org/faq/setup-cli
#miktexsetup --package-set=basic download (did not do this, chose second command)
#miktexsetup install

class InstallMiktex:
    
    # intializes object
    def __init__(self):
        self.miktex_portable_dir = "./miktex_portable"
        self.zipfile = 'miktexsetup-x64.zip'
        self.url = f'https://miktex.org/download/win/{self.zipfile}'
        if not self.check_if_zip_exists():
            wget.download(self.url) 
        
        
    def install_miktex(self):
        current= os.path.dirname(os.path.abspath(__file__))
        path_to_miktex= f'{current}/miktex_portable/miktexsetup.exe'
        print(f'current={current}')
        print(f'path_to_miktex={path_to_miktex}')
        print(f'isfile={os.path.isfile(path_to_miktex)}')
        os.system(f'cmd /k "{path_to_miktex}" install')
        print(f'COMPLETED MIKTEX INSTALLTION YOU CAN NOW COMPILE THE LATEX!')
        
    def check_if_zip_exists(self):
        current= os.path.dirname(os.path.abspath(__file__))
        foundfile= os.path.isfile(f'{current}/{self.zipfile}')
        return foundfile
        
    # walks through zip files and calls function to unpack the zip file
    def extract_zipfile(self,folder):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        current= os.path.dirname(os.path.abspath(__file__))
        for f in files:
            if f[-4:]==".zip":
                if not os.path.isfile(f'{current}/miktexsetup.exe'):
                    print('unzipping')
                    with zipfile.ZipFile(f, 'r') as zip_ref:
                        zip_ref.extractall()
                    print(f' done unzipping')
                else:
                    print(f'miktex zip already unzipped into miktexsetup.exe')
    
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
    main.extract_zipfile("./")
    main.make_miktex_portable_directory()
    main.install_miktex_portable()
    main.install_miktex()