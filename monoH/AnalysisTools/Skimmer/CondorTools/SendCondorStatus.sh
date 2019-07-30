#!/bin/bash
while [ ! -e StopRun.txt ]; do
	python Email_Condor_status.py
	sleep 3600
done 
