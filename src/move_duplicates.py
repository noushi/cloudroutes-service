#!/usr/bin/python
#################################################

# Remove Dupliate Files to Common Directory
# Description:
# ------------------------------------------------------------------
# 1. Finds duplicate py files from multiple locations
# by deep directory scanning,
# 2. Copies each file to the destination directory path and inserts them to the # global namespace,
# 3. removes the original file paths
# Original Author: Akul S - akurnya@gmail.com
#################################################

import os
import sys
import fnmatch
from shutil import copy2
from collections import defaultdict, Counter


def find_duplicates(start_dir, exclude=('__init__.py', 'views.py', 'logconfig.py', 'http.py', 'forms.py')):
    """
    finds duplicate files by name with all paths.
    excludes common files such as log files or web framework related fiels.
    Note: This function does not indicate files with same name implies same content. Internal contents might have changed.

    start_dir: Parent directory to start scanning down to.
    exclude: duplicate files to ignore.
    """
    files_count = Counter()
    dir_path_dct = defaultdict(list)

    for dirpath, subdirs, fname_list in os.walk(start_dir):
        files = fnmatch.filter(fname_list, '*.py')

        if files_count:
            files_count.update(files)
            add_files = filter(lambda f: (f not in files_count) or (files_count[f]>1), files)
        else:
            add_files = files
        map(lambda fn: dir_path_dct[fn].append(dirpath), add_files)

    dir_path_dct = dict(filter(lambda x: (len(x[1]) > 1) \
    and x[0] not in exclude, dir_path_dct.iteritems()))

    return dir_path_dct


def delete_insert_namespace(start_dir, dest_dir, dry = 1):
    """
    gets a map of duplicate files to remove
    removes the original source paths and copies the file to the dest_dir
    inserts the files copied to the dest_dir into the global namespace
    start_dir: Parent directory to start scanning down to
    dest_dir: Destination directory to copy duplicate files to
    dry: Whether to do a dry run or not. 1 for dry run, 0 for actually running it.
    """
    dir_path_dct = find_duplicates(start_dir)

    print "Dry Run?: {}".format(dry == 1)
    #for each file
    for fn in dir_path_dct:
        #get the list of file paths
        paths = dir_path_dct[fn]
        print "copying file: {}".format(os.path.join(paths[0], fn))
        if not dry:
            #copy the file to dest dir
            copy2(os.path.join(paths[0], fn), dest_dir)
            #delete each file path
            #map(os.remove, paths)
            #append to the global namespace
            sys.path.insert(0, os.path.join(dest_dir, fn))

if __name__ == "__main__":
    start_dir = os.getcwd()
    dest_dir = os.path.join(os.getcwd(), 'common')
    print "Start dir: {}\n".format(start_dir)
    print "dest dir: {}\n".format(dest_dir)

    delete_insert_namespace(start_dir, dest_dir)
