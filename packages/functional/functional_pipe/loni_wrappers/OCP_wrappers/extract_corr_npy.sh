#!/bin/bash
# a simple shell script that will find all files, starting from a particular
# base directory, with a particular extension.
# Inputs:
#	$1 the base path
#	$2 a string to match
#
# Outputs:
#	$3 the location to store the outputs
#
# copyright 2015
# written by Eric Bridgeford on 2015-04-23
#

find $1. -name "*.npy" | grep $2 >> $3
