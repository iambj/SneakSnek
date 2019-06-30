import time
import sys
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    
    # Change DIR or use the command line argument -d {dir}
    #DIR = "C:\\Users\\bjoh0003\\dev\\sneaky-snek\\"
    DIR = "C:\\Users\\iambj\\Repo\\sneaky-snek\\"
    if os.name == 'posix':
        DIR = '/mnt/c/Users/iambj/Repo/sneaky-snek'
        # DIR = '/mnt/c/Users/iambj/Repo/HippoTimes/flask-backend/hippo_server' for testing installing


    CUSTOM_IGNORED_FILES = ['.devtime', '.md', '.sh'] # These are in adition to the gitfile and can overwrite or be added to it. 
    
    DELAY = 500  #Too low can cause the snek to pounce more than once for one change.
    TIME_DELTA = 0.015  # Adjust this for the same reason above.
    last_change = 0 # Timestamp in ms of the last change

    # WATCHED_DIRS = ['static'] unused, but maybe a feature later
    QUIET_MODE = False # Whether any logging to the stdout should occur

    

    # Refactor this out.
    try:
        with open("./.gitignore", 'r') as f:
            gitignore = [line.rstrip() for line in f]
            if len(gitignore) < 1:
                print('Warning: .gitfile dected but has no valid entries. Custom ignores will still be loaded. Hint: go to https://www.gitignore.io/ and get one!')
            else:
                print(".gitfile found.")
    except FileNotFoundError as e:
        print('Warning: No .gitfile dected. Custom ignores will still be loaded. Hint: go to https://www.gitignore.io/ and get one!')
        pass
        

    IGNORED_FILES = gitignore + CUSTOM_IGNORED_FILES
    TOKEN_LOCATION = f'{DIR}/.devtime'

    def __init__(self):
        # Command line args
        try:
            if sys.argv[1] in ['-q', '--quiet']:
                Watcher.QUIET_MODE = True

            if sys.argv[2] in ['-d', '--directory']:
                Watcher.DIR = sys.argv[3]
        except:
            pass
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIR, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(Watcher.DELAY)
        except:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        mtime = datetime.now().timestamp()
        # Check if filename in modified files, if so remove from modified to start over.
        if (mtime - Watcher.last_change) > Watcher.TIME_DELTA:
            Watcher.last_change = mtime
            return
            
        (head, tail) = os.path.split(event.src_path)
        (_, this_file) = os.path.split(__file__)
        
        if tail == this_file:
            print("KILL", this_file)
            quit()
            #simpulate the key stroke?
            #os.execv(this_file, ())

        if tail in Watcher.IGNORED_FILES:
            return
        elif event.is_directory:
            return None
        elif event.event_type == "created":
            Handler.update_change_time()
            log("Created: " + event.src_path)
        elif event.event_type == "modified":
            Handler.update_change_time()
            log("Modified: " + event.src_path)

    @staticmethod
    def update_change_time():
        # Updates the local .devtime file with the latest UNIX timestamp.
        # Call this at the end of the initialization process for the app.
        with open(Watcher.TOKEN_LOCATION, 'w+') as f:
            res = str(datetime.now().timestamp())
            f.write(res)
            f.close()

    @staticmethod
    def handle_request(data):
        # Called when /check_changes on the flask server gets hit. Checks whether
        # a change occurred by comparing the timestamp.
        with open(Watcher.TOKEN_LOCATION, 'r+') as f:
            then = f.readline()
            f.close()
        if then == data:
            return "same"
        else:
            return then

def log(msg):
    ''' Utility function for allowing for a quiet execution.'''
    if Watcher.QUIET_MODE is False:
        print(msg)

if __name__ == '__main__':
    w = Watcher()
    w.run()
