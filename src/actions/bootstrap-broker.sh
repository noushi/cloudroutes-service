#!/bin/bash
## Docker Bootstrap Script

echo "[BOOTSTRAP] Exporting /code/common to PYTHONPATH"
echo "-------------------------------------------------"
export PYTHONPATH=$PYTHONPATH:/code/common

echo "Bootstrapping Application Environmental"
echo "[BOOTSTRAP] Dumping Docker Environment:"
echo "-------------------------------------------------"
env

echo "[BOOTSTRAP] Generating config file"
echo "-------------------------------------------------"
cp /code/config/actionBroker.yml.example /config/config.yml

echo "[BOOTSTRAP] Starting broker.py"
echo "-------------------------------------------------"
python /code/broker.py /config/config.yml
