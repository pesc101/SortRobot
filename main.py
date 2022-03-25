import argparse
import logging
import os
import shutil
import re
import re
import yaml
import yaml
from classes.watcher import Watcher
from classes.eventhandler import EventHandler


# Ordner erstellen
def create_dirs(path, type_dict):
    [os.mkdir(name) for name in type_dict.keys() if not os.path.isdir(name)]
    os.chdir(path)


if __name__ == "__main__":

    # Arg Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Insert the path', default='/Users/jan/Downloads')
    parser.add_argument('--patterns', help='Insert Pattern', default='')
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S %d-%m-%Y')

    # Import Config
    with open(os.path.dirname(__file__) + '/config.yaml') as f:
        folders = yaml.load(f, Loader=yaml.FullLoader)

    # Create dirs if not existing
    create_dirs(args.path, folders)

    # Start Watcher
    w = Watcher(args.path, EventHandler(folders=folders, path=args.path))
    w.run(False)

    # sort_dirs(download_dir, dirs)

