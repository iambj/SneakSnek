import time
import sys
from os import path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


'''
    TODO:

        - Figure out better path for .devtime
        - Make a quiet mode? Use a command line arg?

    Docs:

        Place a route to the handle_request() function:

            @app.route("/newshit", methods=["GET", 'POST'])
            def newshit():
                return Handler.handle_request(app, bytes.decode(request.data))

        Make sure to send the decoded data as plain text.

    Bugs:

		- Has to be run out of the flask-backend folder. this needs to be more flexible. For the .devtime file. 
		  But there should be a better way for communication. What is this file solving? Its for the other watchdog to say
		  Python code changed. Duh. Use mine and disable the apps. 
'''


class Watcher:
    DIR = "/mnt/c/Users/iambj/Repo/HippoTimes/flask-backend/hippo_server"
    DELAY = 5
    IGNORED_FILE_EXTS = ['', '.pyy', '.pyc', '.devtime', '.map', '.scss'] # .files are ignored automatically by ''
    WATCHED_DIRS = ['static']
    QUIET_MODE = False

    def __init__(self):
        self.observer = Observer()
        try:
            if sys.argv[1] in ['-q', '--quiet']:
                Watcher.QUIET_MODE = True
        except:
            pass

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIR, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(Watcher.DELAY)
        except:
            self.observer.stop()
            log("Woof! Doggy stopped.")
        self.observer.join()




class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        # e_path = path.split(event.src_path)
        # if len(Watcher.WATCHED_DIRS) > 0:
        #     for d in Watcher.WATCHED_DIRS:
        #         print(d, e_path)
        #     return


        ext = path.splitext(event.src_path)
        # I think this works, it's a little hacky. Probably a more pythonista way to do it. 
        if '.pyc' in event.src_path or ext[1] in Watcher.IGNORED_FILE_EXTS:
            return
        if event.is_directory:
            return None
        elif event.event_type == "created":
            Handler.amend_file()
            log("Created: " + event.src_path)
        elif event.event_type == "modified":
            Handler.amend_file()
            log("Modified: " + event.src_path)



    @staticmethod
    def amend_file():
        with open('./hippo_server/.devtime', 'w+') as f:
            res = str(datetime.now().timestamp())
            # log(res)
            f.write(res)
            f.close()

    @staticmethod
    def make_new_shit(app):
        # Updates the local .devtime file with the latest UNIX timestamp.
        # Call this at the end of the initialization process for the app.
        with open(app.root_path + "/.devtime", 'w') as f:
            res = str(datetime.now().timestamp())
            f.write(res)
            f.close()
            # log(res)

    @staticmethod
    def handle_request(app, data):
        # now = str(datetime.now().timestamp())
        with open(app.root_path + "/.devtime", 'r+') as f:
            then = f.readline()
            f.close()
        if then == data:
            return "same"
        else:
            # Should return JSON
            return then

def log(msg):
    if Watcher.QUIET_MODE is False:
        print(msg)



if __name__ == '__main__':
    w = Watcher()
    w.run()
