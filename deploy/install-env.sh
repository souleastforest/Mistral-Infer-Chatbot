#!/bin/bash

deploydir=$(cd `dirname $0`; pwd)
basedir=$(dirname "$deploydir")
echo "BASEDIR: $basedir"

cd $basedir
python3 -m venv venv
source $basedir/venv/bin/activate
pip install -r requirements.txt
