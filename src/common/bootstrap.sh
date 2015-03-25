#!/bin/bash
## Docker Bootstrap Script

echo "SYMLINKING PATH_INSERT MODULE TO EACH CONTAINER"

ln -s /code/common/path_insert.py /code/actions/path_insert.py
ln -s /code/common/path_insert.py /code/web/path_insert.py
ln -s /code/common/path_insert.py /code/monitors/path_insert.py
ln -s /code/common/path_insert.py /code/bridge/path_insert.py

echo "-------------------------------------------------"
echo "ADDING /common DIRECTORY TO PYTHOPATH"
export PYTHONPATH=$PYTHONPATH:/code/common