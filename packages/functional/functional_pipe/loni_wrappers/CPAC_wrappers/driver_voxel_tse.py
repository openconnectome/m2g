#!/usr/bin/env python

#a module to wrap the CPAC voxelwise timeseries extraction

#Created by Eric Bridgeford on 2015-04-11
#Email: ebridge2@jhu.edu

from CPAC.timeseries.timeseries_analysis import get_voxel_timeseries
from argparse import ArgumentParser
from os import system

def extract_tse(img, mask, bd, tse):
	tsePipe = get_voxel_timeseries()
	tsePipe.inputs.inputspec.rest = img
	tsePipe.inputs.input_mask.mask = mask
	tsePipe.inputs.inputspec.output_type = [True,True]
	tsePipe.base_dir = bd
	tsePipe.run()
	maskPath = mask.split("/")
	maskName = maskPath[len(maskPath) - 1].split(".")[0] # the name of the mask itself, without any of the path or the filetype 
	system('cp ' + bd + '/voxel_timeseries/timeseries_voxel/mask_' + maskName + '.npz ' + tse)
	


def main():
	parser = ArgumentParser(description="")
	parser.add_argument("rest", help = "The fMRI image we want to acquire the voxelwise timeseries from (.nii, .nii.gz)")
	parser.add_argument("mask", help = "The mask for which timeseries will be extracted (.nii, .nii.gz)")
	parser.add_argument("base", help = "The base directory in which the outputs will be placed (Dir)")
	parser.add_argument("tse", help = "The location the timeseries files will be placed (.npz)")

	result = parser.parse_args()
	
	extract_tse(result.rest, result.mask, result.base, result.tse)

if __name__ == "__main__":
	main()
