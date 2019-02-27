#!/bin/sh

unzip ./Data/output_sub.zip
unzip ./Data/output_rch.zip

python swat_ewvs.py >> ewvs.txt
