#! /bin/bash
#
#a simple script to place paths specified in a text file
#to a numbered location in a new folder
#
#Inputs:
#	$1: the path to a text file whose line by line entries
#		are file paths
#
#Outputs:
#	$2: the path to a directory to dump the files in
#	$3: a text file containing the paths to the viz files
#Copyright (c) 2015
#written by Eric Bridgeford on 2015-04-25
#

sed -e s/.npy/.png/g $1 > $2

