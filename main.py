import argparse
import os
import yaml
from classes.watcher import Watcher
from classes.eventhandler import EventHandler
import coloredlogs
import logging
coloredlogs.install()


# Ordner erstellen
def create_dirs(path, type_dict):
    os.chdir(path)
    [os.mkdir(name) for name in type_dict.keys() if not os.path.isdir(name)]


if __name__ == "__main__":

    # Arg Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Insert the path', default='/Users/jan/Downloads')
    parser.add_argument('--patterns', help='Insert Pattern', default='')
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S %d-%m-%Y',
                        handlers=[
                            logging.FileHandler("logs.log"),
                            logging.StreamHandler()
                        ])

    # Import Config
    with open(os.path.dirname(__file__) + '/config.yaml') as f:
        folders = yaml.load(f, Loader=yaml.FullLoader)

    # Create dirs if not existing
    create_dirs(args.path, folders)

    # Start Watcher
    w = Watcher(args.path, EventHandler(folders=folders, path=args.path))
    w.run(False)


