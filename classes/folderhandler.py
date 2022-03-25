import os
import shutil
import re


class FolderHandler:

    def __init__(self, path):
        self.path = path
        self.rest_folder = 'rest'
        self.num = 0

    def sort_dir(self, folders):
        dirs = [f for f in next(os.walk('.'))[1] if f not in folders and f != self.rest_folder]
        dirs = [f for f in dirs if not re.match('^\\.', f)]

        for dir in dirs:
            src_path = os.path.join(self.path, dir)
            dest_path = os.path.join(self.path, self.rest_folder)
            shutil.move(src_path, dest_path)

