#!/usr/bin/env python
# a simple program for making correlation matrix plots for a given input file

# to be used locally and will be modified as needed

# written 2015-04-16 by Eric Bridgeford

from numpy import load
from os import system
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from string import replace

def get_corr_img(infile, outfile):
 	filein = open(infile, 'r')
	fileout = open(outfile, 'r')
	subj = 1;
	for linein in filein:
		lineout = fileout.readline()
		linein = replace(linein, "\n", "")
		lineout = replace(lineout, "\n", "")
		corr = load(linein)
		f = plt.figure()
		f.suptitle("");
		i = plt.imshow(corr[:,:],vmin=0,vmax=1)
		plt.axis([0, corr.shape[0], corr.shape[0], 0])
		cax = f.add_axes([.9, .1, .03, .8])
		f.colorbar(i, cax = cax)
		plt.savefig(lineout)
		plt.close()
		subj = subj + 1
	

def main():
	parser = ArgumentParser(description = "")
	parser.add_argument("in_file", help = "a numpy file containing the 3D correlation files (slices x numpts x numpts, .npy)")
	parser.add_argument("out_file", help = "the output location of the file containing the output images")
	result = parser.parse_args()
	get_corr_img(result.in_file, result.out_file)

if __name__ == "__main__":
	main() 

