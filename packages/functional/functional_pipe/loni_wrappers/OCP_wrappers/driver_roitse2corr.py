#!/usr/bin/env python
# a revised module for computing a correlation
# matrix given an input set of roi voxelwise timeseries

# Input: 
# 	infile: the numpy archive containing the timeseries that we want to
#		extract the timeseries information for
#		file must be setup such that the information contained in the
#		archive, letting data = data[infile.files[0]]
#		data[tse information, slice #]
# Algorithm:
#	the algorithm used to compute the timeseries information is as follows:
#	C(x,y) = 1/(n-1) * (sum from i = 0 to n(xi - xbar)*(yi - ybar)/(dev(x)*dev(y))

# Output:
#	outfile: the resulting array containing the correlation matrix extracted
#		from the roi timeseries

# Copyright (c) 2015
# written by Eric Bridgeford on 2015-04-13

from numpy import zeros, load, save
from os import system
from argparse import ArgumentParser
from numpy import std, mean
from string import replace

def get_corr_matrix(infile, outfile):
 	filein = open(infile, 'r')
	fileout = open(outfile, 'r')
	for linein in filein:
		lineout = fileout.readline()
		linein = replace(linein, "\n", "")
		lineout = replace(lineout, "\n", "")
		data = load(linein)
		data = data[data.files[0]]
		Std = zeros((data.shape[0]))
		Me = zeros((data.shape[0]))
		Corr = zeros((data.shape[0], data.shape[0]))
		for i in range(0, data.shape[0]):
			Std[i] = std(data[i, :])
			Me[i] = mean(data[i, :])
		for x in range(0, data.shape[0]):
			for y in range(0, data.shape[0]):
				sum = 0
				for i in range(0, data.shape[1]):
					sum += (data[x, i] - Me[x])*(data[y, i] - Me[y])
				Corr[x,y] = sum/((data.shape[1]-1)*(Std[x]*Std[y]))
		save(lineout, Corr)
	
def main():
	parser = ArgumentParser(description = "")
	parser.add_argument("in_file", help = "a numpy file to convert to a correlation matrix (.npz)")
	parser.add_argument("out_file", help = "the location to place the numpy output (.npy)")

	result = parser.parse_args()

	get_corr_matrix(result.in_file, result.out_file)

if __name__ == "__main__":
	main()	
			
