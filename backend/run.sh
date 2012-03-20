#!/bin/bash

cd /root/workspace/riskyListy/backend

pushd ..

mkdir -p archives
echo "*" > archives/.gitignore
tar cvfz archives/backup-$(date +"%s").tar.bz2 db /var/mail/itp ~itp/mbox

source ./bin/activate
popd

python CheckMail.py
python AddEmailers.py
python ComputeScores.py
python ComputeEmailerScores.py


