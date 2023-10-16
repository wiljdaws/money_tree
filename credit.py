import shutil
from colorama import Fore, Style
import time
import os

class credit():
    def __init__(self, file):
        '''
        initialize the credit class
        Args:
            file (str): the filepath of the file created 
        Ex use:
            file = __file__
            credit(file)
        '''
        self.file_creation_time = time.strftime('%m/%d/%Y', time.gmtime(os.path.getctime(file)))
        self.author = {
            "login": "wiljdaws",
            "name": "Dawson J. Williams",
            "fc": "FTW5",
            "title": "DA",
            "file": os.path.basename(file)
        }
        self.li_url = "https://www.linkedin.com/in/djwsoftdev/"
        self.phone_url = "https://phonetool.amazon.com/users/wiljdaws"
        self.drive_url = "https://drive.corp.amazon.com/personal/wiljdaws"
        self.terminal_width = shutil.get_terminal_size().columns
        self.border = '='*(self.terminal_width)
        self.half_len_of_border = int((len(self.border)/2))
        self.url_dict = {
            "LinkedIn": self.li_url, 
            "Phone tool": self.phone_url, 
            "Drive": self.drive_url
        }
    
    def skip_num_lines(self, start = 0, lines = 3):
        for num in range (start,lines):
            print(" ")
    
    def print_border(self):
        print(self.border)
    
    def get_border(self):
        return self.border
    
    def print_citation(self):
        citation = f'{Fore.RED} File: {self.author.get("file", None)} | Created by: {self.author.get("fc", None)} {self.author.get("title", None)} {self.author.get("name", None)} ({self.author.get("login", None)}) | Date created: {self.file_creation_time} {Style.RESET_ALL}'
        centered_citation = citation.center(self.terminal_width)
        print(centered_citation)
    
    def get_citation(self):
        citation = f'{Fore.RED} File: {self.author.get("file", None)} | Created by: {self.author.get("fc", None)} {self.author.get("title", None)} {self.author.get("name", None)} ({self.author.get("login", None)}) | Date created: {self.file_creation_time} {Style.RESET_ALL}'
        centered_citation = citation.center(self.terminal_width)
        centered_citation = f'{self.get_border()}\n{centered_citation}\n{self.get_border()}'
        # remove leading whitespace
        centered_citation = centered_citation.strip()
        return centered_citation
    
    def style_link(self, url):
        '''
        style url
        '''
        clickable_link = f"{Fore.BLUE}{url}{Style.RESET_ALL}"
        return clickable_link
    
    def print_links(self):
        '''
        print all links
        '''
        for key, value in self.url_dict.items():
            clickable_link = self.style_link(value)
            print(f"{Fore.RED}{key}{Style.RESET_ALL}: {clickable_link}")
    
    def create_env(self):
        '''
        create an enviroment
        '''
        try:
            os.system('python -m venv env')
        except:
            print("Error creating enviroment, trying python3")
            os.system('python3 -m venv env')
        
    def activate_env(self):
        '''
        activate the enviroment
        '''
        os.system('source env/bin/activate')
    
    def create_requiremnents_file(self):
        '''
        create a requirements.txt file
        '''
        os.system('pip freeze > requirements.txt')
    
    def install_requirements(self):
        '''
        install requirements
        '''
        os.system('pip install -r requirements.txt')
    
    def print_credits(self):
        '''
        print credits
        '''
        ''''
       
        
        combine above into one returnable string
        '''
        self.skip_num_lines()
        self.print_border()
        self.print_citation()
        self.print_border()
        self.print_links()
        self.print_border()
        self.print_border()
        self.skip_num_lines(lines=1)
        print(credits) 
    
    def get_credits(self):
        '''
        get print credits as one returnable string
        '''
        credits =(
        f'''
{self.get_citation()}
{Fore.RED}LinkedIn{Style.RESET_ALL}: {self.style_link(self.li_url)}
{Fore.RED}Phone tool{Style.RESET_ALL}: {self.style_link(self.phone_url)}
{Fore.RED}Drive{Style.RESET_ALL}: {self.style_link(self.drive_url)}
{self.get_border()}
{self.get_border()}
        '''
        )
        return credits
       
    def main(self):
        '''
        main
        '''
        if not os.path.exists("venv"):
            self.create_env()
        # check to see if venv is activated
        if not os.getenv('VIRTUAL_ENV'):
            print("not in virtual environment!")
            self.activate_env()
            print("virtual environment actiavted")
        if not os.path.exists("requirements.txt"):
            self.create_requiremnents_file()
        try:
            #print(self.get_credits())
           self.print_credits()
        except:
            self.install_requirements()
    
if __name__ == "__main__":
    credit(__file__).main()
    
        
        
        
        
        