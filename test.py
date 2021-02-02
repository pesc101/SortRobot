from os import listdir
from os.path import isfile, join
import os
import shutil
from pathlib import Path

## Ordner erstellen
def create_dirs(path, dir_names):
    os.chdir(path)
    for name in dir_names:
        if not os.path.isdir(name):
            os.mkdir(name)

## Ordner sortieren 
def sort_dirs(mypath, dir_names):
    dirs = [f for f in listdir(mypath) if '$' not in f]
    dirs.remove('.DS_Store')
    if len(dirs) == 0:
        return print('No new Dirs in Download Dir')
    
    for dir in dirs:
        src_path = mypath  + dir
        dest_path = mypath + dir_names[6]
        shutil.move(src_path, dest_path)
        print(src_path + '  >>>  ' + '$rest')

## Dateien sortieren 
def sort_files(mypath, dir_names, types):
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files.remove('.DS_Store')
    if len(files) == 0:
        return print('No new Files in Download Dir')

    for file in files:
        src_path = mypath + file
        filetype = file.split('.')[len(file.split('.')) - 1]
        counter = 0
        for i in range(6):
            if filetype in types[i]:
                dest_path = mypath + dir_names[i]
                shutil.move(src_path, dest_path)
                print(src_path + '  >>>  ' + dest_path.split('/')[len(dest_path.split('/')) - 1])
            else:
                counter = counter + 1
        if counter == 6:
            dest_path = mypath + dir_names[6]
            shutil.move(src_path, dest_path)
            print(src_path + '  >>>  ' + dest_path.split('/')[len(dest_path.split('/')) - 1])
        
 
    # Finish
    print('All Files got moved.')

if __name__ == "__main__":
    mypath='/Users/jan/Downloads/'
    dirs = ['$installer','$archiv','$office','$pdf','$img','$code','$rest']
    types = [   ['dmg'],
                ['rar','RAR','zip','tar','7z'],
                ['doc','docx','csv','ppt','pptx','xls','xlsx','.one','odt','key','ods','pages','numbers'],
                ['pdf'],
                ['png','webp','jpeg','jpg','gif','psd','tif'],
                ['r','R','py','js','htm','html','HTML','css','bib','tex','c','c++','php','jar']
            ]
    create_dirs(mypath, dirs)
    sort_files(mypath, dirs, types)
    sort_dirs(mypath, dirs)