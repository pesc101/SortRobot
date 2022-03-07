import datetime
from watchdog.events import PatternMatchingEventHandler


def get_datetime():
    return datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")


class EventHandler(PatternMatchingEventHandler):

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)

    def on_created(self, event):
        print(f'{get_datetime()} CREATED: {event.src_path} created.')

    def on_deleted(self, event):
        print(f'{get_datetime()} DELETED: {event.src_path} deleted.')

    def on_modified(self, event):
        print(f'{get_datetime()} MODIFIED: {event.src_path} has been modified.')

    def on_moved(self, event):
        print(f'{get_datetime()} MOVED: {event.src_path} >> {event.dest_path}.')
