#!/cis/project/migraine/centos6/anaconda/bin/python
#LONI usable functional preprocessing module
#uses CPAC func_preproc function
#version 0.3.8

from CPAC.func_preproc.func_preproc import create_func_preproc
import os
import argparse

params=argparse.ArgumentParser()
params.add_argument("-f","--inimg", help="the path to an input image to be preprocessed.")
params.add_argument("-fs", "--start_id", type=int, help = "the starting slice to be considered.")
params.add_argument("-ls", "--stop_id", type = int, help = "the last slice to be considered.")
params.add_argument("-tr", "--tr", type=float, help = "the tr scan parameter.")
params.add_argument("-a", "--acquisition", type=str, help = "the acquisition pattern of the scan.")
params.add_argument("-b","--base_dir", help="the base directory for the functions.")
params.add_argument("-bet","--bet",type=int,help = "bool for whether or not to use bet.")
params.add_argument("-eov","--erode_one_voxel",help="file location of function erode one voxel (nii.gz).")
params.add_argument("-d","--deoblique",help="file location of function deoblique (nii.gz).")
params.add_argument("-ed","--edge_detect",help="file location of function edge detect (nii.gz).")
params.add_argument("-gbm","--get_brain_mask",help="location of function get brain mask (nii.gz).")
params.add_argument("-gmm","--get_mean_motion",help="location of function get mean motion (nii.gz).")
params.add_argument("-gmr","--get_mean_rpi",help="location of function get mean rpi (nii.gz).")
params.add_argument("-mn","--mask_normalize",help="location of normalized mask (nii.gz).")
params.add_argument("-ms","--mean_skullstrip",help="location of mean skullstripped image (nii.gz).")
params.add_argument("-mc","--motion_correct",help="location of motion corrected image (nii.gz).")
params.add_argument("-mca","--motion_correct_a",help="location of motion corrected image A (nii.gz).")
params.add_argument("-n","--normalize",help="location of normalized image (nii.gz).")
params.add_argument("-r","--reorient",help="location of reoriented image (nii.gz).")

args = params.parse_args()
preproc=create_func_preproc(use_bet=args.bet)
preproc.inputs.inputspec.func=args.inimg
'''if args.start_id:
	preproc.inputs.inputspec.start_idx=args.start_id
if args.stop_id:
	preproc.inputs.inputspec.stop_idx=args.start_id
if args.tr:
	preproc.inputs.inputspec.tr=args.tr
if args.acquisition:
	preproc.inputs.inputspec.acquisition=args.acquisition
'''
if args.base_dir:
	preproc.base_dir=args.base_dir

preproc.run() #doctest: +SKIP

if args.erode_one_voxel:
	os.system('cp '+args.base_dir+'/func_preproc/erode_one_voxel/*.nii.gz '+args.erode_one_voxel)
if args.deoblique:
	os.system('cp '+args.base_dir+'/func_preproc/func_deoblique/*.nii.gz '+args.deoblique)
if args.edge_detect:
	os.system('cp '+args.base_dir+'/func_preproc/func_edge_detect/*.nii.gz '+args.edge_detect)
if args.get_brain_mask:
	os.system('cp '+args.base_dir+'/func_preproc/func_get_brain_mask*/*.nii.gz '+args.get_brain_mask)
if args.get_mean_motion:
	os.system('cp '+args.base_dir+'func_preproc/func_get_mean_motion/*.nii.gz '+args.get_mean_motion)
if args.get_mean_rpi:
	os.system('cp '+args.base_dir+'/func_preproc/func_get_mean_RPI/*.nii.gz '+args.get_mean_rpi)
if args.mask_normalize:
	os.system('cp '+args.base_dir+'/func_preproc/func_mask_normalize/*.nii.gz '+args.mask_normalize)
if args.mean_skullstrip:
	os.system('cp '+args.base_dir+'/func_preproc/func_mean_skullstrip/*.nii.gz '+args.mean_skullstrip)
if args.motion_correct:
	os.system('cp '+args.base_dir+'/func_preproc/func_motion_correct/*.nii.gz '+args.motion_correct)
if args.motion_correct_a:
	os.system('cp '+args.base_dir+'/func_preproc/func_motion_correct_A/*.nii.gz '+args.motion_correct_a)
if args.normalize:
	os.system('cp '+args.base_dir+'/func_preproc/func_normalize/*.nii.gz '+args.normalize)
if args.reorient:
	os.system('cp '+args.base_dir+'/func_preproc/func_reorient/*.nii.gz '+args.reorient)


