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
import yaml
import contextlib

@contextlib.contextmanager
def yaml_load(yml_stream):
    try:
        f = yaml.load(yml_stream)
        yield f
    except AttributeError, e:
        print "Error %s" %(e)
    finally:
        del f
        


def get_root_path(parent_path= os.getcwd(), root_path='cloudroutes-service'):    
    """
    Gets the root directory path given current working directory for
    execution iff current directory is a subdirectory of root directory.
    """
    parent_path, cur_dir = os.path.split(os.path.abspath
    (parent_path))
    if cur_dir == root_path: return parent_path, cur_dir
    else: return get_root_path(parent_path=parent_path)


def path_insert(path_keys, yml_path=r'src\bridge\config\config.yml.example', dry_run = 1):
    """
    Gets the correct target root path.
    Iterates over paths given as yaml configuration keys
    and adds them to the sys.path if legitimate.
    
    Run it like:
    path_insert(['common_src'], dry_run=1)
    """
    #Get the project root path
    parent_path, root_dir_name = get_root_path()
    #Get the YAML config file path from rel path - supply a yml config file
    yml_path = os.path.join(parent_path, root_dir_name, yml_path)
    #print yml_path
    with yaml_load(open(yml_path)) as f:
        for key in path_keys:
            #We can use any value separator.using yaml sequence
            paths = [root_dir_name] + f[key]
            target_path = os.path.join(parent_path, *paths)
            if os.path.exists(target_path):
                if dry_run:
                    print "Dry run path %s" %(target_path)
                else:
                    sys.path.insert(1,target_path)
            else:
                raise Exception("PathError: Supplied target path is not correct. Please check one of the supplied path values in the root path and configuration file.")