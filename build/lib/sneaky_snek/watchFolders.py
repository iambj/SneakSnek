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

		Import:

			from sneaky_snek import watchFolders
			handler = watchFolders.Handler()


        Place a route to the handle_request() function:

            #watchFolders dumby route used by refresher.js
            @app.route("/check_changes", methods=["GET", 'POST'])
            def check_changes():
                return handler.handle_request(bytes.decode(request.data))

        At the end of your flask app startup code, place:

            handler.update_change_time()


		Load up a second terminal to your project directory and activate your venv. Run watchdog.py.

        Make sure to send the decoded data as plain text.

    Bugs:

		- Has to be run out of the flask-backend folder. this needs to be more flexible. For the .devtime file. 
		  But there should be a better way for communication. What is this file solving? Its for the other watchdog to say
		  Python code changed. Duh. Use mine and disable the apps. 
		- Still double logs a modified file. For both static and python
'''


class Watcher:
    #DIR = "/mnt/c/Users/iambj/Repo/HippoTimes/flask-backend/hippo_server"
    DIR = "/c/Users/bjoh0003/dev/sneaky-snek"
    DELAY = 5
    # .files are ignored automatically by ''
    IGNORED_FILE_EXTS = ['', '.pyy', '.pyc', '.md', '.devtime', '.map', '.scss']
    WATCHED_DIRS = ['static']
    QUIET_MODE = False

    def __init__(self):
        self.observer = Observer()
        try:
            if sys.argv[1] in ['-q', '--quiet']:
                Watcher.QUIET_MODE = True

            if sys.argv[2] in ['-d', '--directory']:
                Watcher.DIR = sys.argv[3]
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
            Handler.update_change_time()
            log("Created: " + event.src_path)
        elif event.event_type == "modified":
            Handler.update_change_time()
            log("Modified: " + event.src_path)

    @staticmethod
    def amend_file():
        with open(f'{Watcher.DIR}/.devtime', 'w+') as f:
            res = str(datetime.now().timestamp())
            # log(res)
            f.write(res)
            f.close()

    @staticmethod
    def update_change_time():
        # Updates the local .devtime file with the latest UNIX timestamp.
        # Call this at the end of the initialization process for the app.
        with open(f'{Watcher.DIR}/.devtime', 'a+') as f:
            res = str(datetime.now().timestamp())
            f.write(res)
            f.close()
            # log(res)

    @staticmethod
    def handle_request(data):
        # now = str(datetime.now().timestamp())
        with open(f'{Watcher.DIR}/.devtime', 'r+') as f:
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
