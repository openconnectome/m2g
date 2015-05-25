#! /bin/bash

#a simple shell script for generating the file paths for the
#resultant numpy arrays created in the pairwise correlation 
#module.

#Inputs: 
#	$1: the location of the npz files that will be pairwise
#		correlated
#
#Outputs:
#	$2: the location of the pairwise correlations
#		files will be of equal length to $1
#		and will be the same filenames + 'pcorr.npy'
#
#Copyright (c) 2015
#written by Eric Bridgeford on 2015-04-25

sed -e s/.npz/pcorr.npy/g $1 > $2

