# A module for computing a correlation matrix
# given an input set of voxelwise timeseries

# Input:
#	infile: a numpy archive containing the timeseries
#		that we want to extract the timeseries for
#Output:
#	outfile: a numpy archive containing the correlation matrix
#		that we desire

# Copyright (c) 2015
# written by Eric Bridgeford on 2015-04-13

from numpy import load, empty, append
from os import system
from argparse import ArgumentParser

def get_corr_matrix(infile, outfile):
	data = load(infile)
	Corr = empty(shape=[0, len(data[0]) # assume the input has at least one 
					   # set of values
	for i = 0:len(data.files) - 1
		a = data.files[i]
			


def main():
	parser = ArgumentParser(description = "")
	parser.add_argument("in_file", help = "a numpy file to convert to a correlation matrix (.npz)")
	parser.add_argument("out_file", help = "the location to place the numpy output (.npy)")

	result = parser.parse_args()

	get_corr_matrix(result.in_file, result.out_file)

if __name__ == "__main__":
	main()	
	
