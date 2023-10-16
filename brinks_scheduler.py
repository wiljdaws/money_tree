import os
import shutil
import subprocess
import sys
import random
import threading
import time
from subprocess import call
from pathlib import Path
from credit import credit
from tabulate import tabulate

class Scheduler:
    def __init__(self, config):
        '''
        Initialize the scheduler with maximum runs per hour and time window.
        
        Args:
            max_runs_per_hour (int): The maximum number of runs per hour.
            begin_hour (int): The beginning of the time window.
            end_hour (int): The end of the time window.
        '''
        self.max_runs_per_hour = config.get("max_runs_per_hour", 2)
        self.begin_hour = config.get("begin_hour", 7)
        self.end_hour = config.get("end_hour", 16)
        self.bat_folder = os.path.join(os.path.expanduser("~"), "Desktop", "BAT MAN Files")
        self.bat_file = os.path.join(self.bat_folder, "brinks_truck.py")
        self.runs_this_hour = 0
        self.terminal_width = shutil.get_terminal_size().columns
        self.spacing = int((self.terminal_width-15)/4)-3
        self.num = 20
        self.frames = [
            " "* self.spacing + "╔════╤"+"╤╤"*self.num+"╤════╗\n" +
            " "* self.spacing + "║    │"+"││"*self.num+" \\   ║\n" +
            " "* self.spacing + "║    │"+"││"*self.num+"  O  ║\n" +
            " "* self.spacing + "║    O"+"OO"*self.num+"     ║",

            " "* self.spacing + "╔════╤"+"╤╤"*self.num+"╤════╗\n" +
            " "* self.spacing + "║    │"+"││"*self.num+"│    ║\n" +
            " "* self.spacing + "║    │"+"││"*self.num+"│    ║\n" +
            " "* self.spacing + "║    O"+"OO"*self.num+"O    ║",

            " "* self.spacing + "╔════╤╤"+"╤╤"*self.num+"════╗\n" +
            " "* self.spacing + "║   / │"+"││"*self.num+"    ║\n" +
            " "* self.spacing + "║  O  │"+"││"*self.num+"    ║\n" +
            " "* self.spacing + "║     O"+"OO"*self.num+"    ║",

            " "* self.spacing + "╔════╤"+"╤╤"*self.num+"╤════╗\n" +
            " "* self.spacing + "║    │"+"││"*self.num+"│    ║\n" +
            " "* self.spacing + "║    │"+"││"*self.num+"│    ║\n" +
            " "* self.spacing + "║    O"+"OO"*self.num+"O    ║"
        ]
        self.random_time = None
        
    def increment_runs(self):
        '''
        Increment runs per hour.
        '''
        self.runs_this_hour += 1
    
    def get_runs(self):
        '''
        Return runs per hour.
        '''
        return self.runs_this_hour
    
    def create_bat_folder(self):
        '''
        Create a folder for BAT files on the desktop if it doesn't exist.
        '''
        if not os.path.exists(self.bat_folder):
            os.makedirs(self.bat_folder)
            self.create_bat_file()
        elif not os.path.exists(self.bat_file):
            self.create_bat_file()

    
    def create_bat_file(self):
        '''
        Create a BAT file that runs a Python script.
        Args:
            py_file_path (str): The path to the Python script to be executed.
        '''
        brinks_file = os.path.join(os.getcwd(), "brinks_truck.py")
        bat_contents = f'@echo off\n"{sys.executable}" "{brinks_file}"\nexit'
        bat_file_path = os.path.join(str(self.bat_folder), 'brinks_truck.bat')
        if not os.path.exists(self.bat_folder):
            self.create_bat_folder()
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(bat_contents)
    
    def display_animation(self, repeat=True, frame_delay=0.5):
        """
        Display the animation in the console.
        
        Args:
            random_time (time.struct_time): The time at which the animation will be displayed.
            repeat (bool): Whether to repeat the animation.
            frame_delay (float): The delay between frames.
        """
        file = __file__
        author = credit(file)
        author = author.get_credits()
        print(f'{author}')
        UP = '\033[9A'
        CLEAR = '\x1b[2K'
        
        while True:
            table = "\n".join([" " * (self.spacing+7)  + line for line in self.get_tabulated_table().split("\n")])
            for frame in self.frames:
                print(f'{table}\n{frame}')
                time.sleep(frame_delay)
                print(UP, end=CLEAR)
            if not repeat:
                break
    
    def set_random_time(self):
        '''
        Get a random time between begin_hour and end_hour.
        '''
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        random_timestamp = time.mktime(time.localtime()) + random_minutes * 60 + random_seconds
        random_time = time.localtime(random_timestamp)
        self.random_time = random_time
    
    def get_random_time(self):
        '''
        Get a random time between begin_hour and end_hour.
        '''
        if self.random_time is None:
            self.set_random_time()
        return self.random_time
    
    def get_tabulated_table(self):
        '''
        Return a tabulated table of the scheduler's attributes.
        
        Args:
            random_time (time.struct_time): The time at which the animation will be displayed.
        '''
        scheduled_time = time.strftime("%I:%M %p", self.get_random_time())
        dict = {
            "Scheduled time": [scheduled_time],
            "Runs this hour": [self.get_runs()]
        }
        table = tabulate(dict, headers="keys", tablefmt="fancy_grid", numalign="center", stralign="center")
        return table

    def main(self):
        self.create_bat_folder()
        while True:
            if self.begin_hour <= time.localtime().tm_hour <= self.end_hour:
                while self.runs_this_hour <= self.max_runs_per_hour:
                    animation_thread = threading.Thread(target=self.display_animation)
                    animation_thread.start()
                    while time.localtime() < self.get_random_time():
                        time.sleep(1)
                    bat_file = os.path.join(self.bat_folder, "brinks_truck.bat")
                    try:
                        subprocess.call(bat_file)
                        self.increment_runs()
                        self.set_random_time()
                        animation_thread.join()
                    except Exception as e:
                        print(f"An error occurred with the brinks truck file at: {time.time()}")
                        print(f"Error: {e}")
            else:
                time.sleep(60)

if __name__ == "__main__":
    config = {
        "max_runs_per_hour": 2,
        "begin_hour": 7,
        "end_hour": 16,
    }
    scheduler = Scheduler(config)
    scheduler.main()