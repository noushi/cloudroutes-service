#!/usr/bin/python
#################################################

# Use common code from src/common
# Description:
# ------------------------------------------------------------------
# 1. Finds root project dir
# 2. Iterates over paths given as yaml configuration keys
# 3. Adds them to the sys.path if legitimate.
# Original Author: Akul S - akurnya@gmail.com
#################################################


import os
import sys


class PathError(Exception):
    """
    Excetion handling for incorrect path.
    """
    def __init__(self, target_path):
        # Call the base class
        super(PathError, self).__init__()
        self.message = """Supplied target path %s is not correct.\n
        Please check one of the supplied path values in the root path and configuration file.""" %(target_path)
    
    def __str__(self):
        return (self.message)


def get_root_path(parent_path= os.getcwd(), root_path='cloudroutes-service'):    
    """
    Gets the root directory path given current working directory for
    execution iff current directory is a subdirectory of root directory.
    """
    parent_path, cur_dir = os.path.split(os.path.abspath
    (parent_path))
    if cur_dir == root_path: return parent_path, cur_dir
    else: return get_root_path(parent_path=parent_path)


def add_path(target_path, dry_run=1):
    #Inserts path to namespace
    if os.path.exists(target_path):
        if dry_run:
            print "Dry run path %s" %(target_path)
        else:
            sys.path.insert(1,target_path)
    else:
        raise PathError(target_path)
    

def path_insert(yml_config, path_keys, dest_path = None, dry_run = 1):
    """
    Gets the correct target root path.
    Adds dest_path if it is the relative path to a directory to include in 
    the sys.path.
    Else retrives from path_keys a list of keys that correspond to keys in 
    a yaml config file, iterates over these keys and adds values as the 
    destination path to the sys.path if legitimate.
    
    Run it like:
    with open(yaml_file, 'r') as cfh:
        config = yaml.safe_load(cfh)
        path_insert(config, ['common_src'])
    
    yml_config: A parsed yaml document
    path_keys: A list of keys to lookup from the given yaml file.
    dest_path: A string destination path if given else None.
    dry_run: If value is 1, runs the procedure without adding to the sys.path
    returning the legitimate path(s) else if the value is 0, adds those paths.
    """
    
    #Get the project root path
    parent_path, root_dir_name = get_root_path()
    
    if isinstance(dest_path, str):
        target_path = os.path.join(parent_path, root_dir_name, dest_path)
        add_path(target_path, dry_run=dry_run)
    
    for key in path_keys:
        target_path = os.path.join(parent_path, root_dir_name, *yml_config[key])
        add_path(target_path, dry_run=dry_run)