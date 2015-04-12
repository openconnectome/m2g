#!/usr/bin/env python

# Copyright 2015 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# extract_vol.py
# Created by Greg Kiar on 2015-02-21;

# edited by Eric Bridgeford on 2015-04-08.
# Email: gkiar@jhu.edu
# Copyright (c) 2015. All rights reserved.

from argparse import ArgumentParser
from nibabel import load, save, Nifti1Image
from numpy import where, loadtxt

def extract_vol(func_img, vol_val, v0_vol):
  print "Loading fMRI data..."
  f_img = load(func_img)
  v0_data = f_img.get_data()
  v0_head = f_img.get_header()
  
 # print "Loading vol_val file..."
 # b = loadtxt(vol_val)
  
  print "Extracting volume..."
  v0_data=v0_data[:,:,:,vol_val]
  
  print "Updating image header..."
  v0_head.set_data_shape(v0_head.get_data_shape()[0:3])

  print "Saving..."
  out = Nifti1Image(v0_data,f_img.get_affine(),v0_head)
  save(out, v0_vol)

  print "Complete!"


def main():
  parser = ArgumentParser(description="")
  parser.add_argument("fmr", action="store", help="The fMRI image we want to extract vol from (.nii, .nii.gz)")
  parser.add_argument("vol_val", action="store", help="The volume file corresponding to the fmri image (int)")
  parser.add_argument("v0", action="store", help="The output file location of the B0 scan (.nii, .nii.gz)")

  result = parser.parse_args()

  extract_vol(result.fmr, result.vol_val, result.v0)

if __name__ == "__main__":
    main()
    
