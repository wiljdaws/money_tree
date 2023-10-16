import getpass
import os
import random
import time
from subprocess import call


class Scheduler():
    def __init__(self, max_runs_per_hour:int=2, begin_hour:int=7, end_hour:int=16):
        '''
        Initialize the scheduler with maximum runs per hour and time window.
        
        Args:
            max_runs_per_hour (int): The maximum number of runs per hour.
            begin_hour (int): The beginning of the time window.
            end_hour (int): The end of the time window.
        '''
        self.max_runs_per_hour = max_runs_per_hour
        self.begin_hour = begin_hour
        self.end_hour = end_hour
        self.bat_folder = os.path.join(os.path.expanduser("~"), "Desktop", "Bat Files")
        self.money_tree_bat = os.path.join(self.bat_folder, "money_tree.bat")
        self.runs_this_hour = 0
        self.current_time = time.localtime()
    
    def get_random_time(self):
        '''
        Get a random time between begin_hour and end_hour.
        '''
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        current_timestamp = time.mktime(self.current_time)
        random_timestamp = current_timestamp + random_minutes * 60 + random_seconds
        random_time = time.localtime(random_timestamp)
        return random_time
        
    def main(self):
        while True:
            time.sleep(1)
            if self.current_time.tm_hour >= self.begin_hour and self.current_time.tm_hour <= self.end_hour:
                runs_this_hour = 0  
                while runs_this_hour < self.max_runs_per_hour:
                    random_time = self.get_random_time()
                    scheduled_time = time.strftime("%I:%M %p", random_time)
                    print(f"Scheduled time: {scheduled_time}")
                    while time.localtime() < random_time:
                        time.sleep(1)
                    try: call([self.money_tree_bat])
                    except: print("an error occured with the money tree workflow at:", time.time())
                    runs_this_hour += 1
                    print(f'There have been {runs_this_hour} exececutions of the money tree workflow at {self.current_time.tm_hour}:00')
            else:
                time.sleep(60)


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.main()