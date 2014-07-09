#!/usr/bin/python

# Copyright 2014 Open Connectome Project (http://openconnecto.me)
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

# create_atlas.py
# Created by Disa Mhembere on 2014-04-10.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

# This simply takes a (182, 218, 182) atlas and creates
# a ~30-non-zero k region atlas by relabelling each
#   3x3x3 region with a new label then masking
# using a base atlas

import argparse
import mrcap.roi as roi
import nibabel as nib
import numpy as np
from math import ceil
from copy import copy
import sys
from time import time

def create(roixmlfn="MNI152_T1_1mm_brain_mask_integer.xml", 
          roirawfn="MNI152_T1_1mm_brain_mask_integer.raw", start=2):
  """
  Create a new atlas given some scaling factor determined by the 
  start index. Opaque doc, but best I can do.

  @param roixmlfn: xml mask file name
  @param roirawfn: raw mask file name
  @param start: the x,y,z start position which determines the scaling
  """

  start_time = time()
  print "Loading rois as base ..."
  base = roi.ROIData (roirawfn, roi.ROIXML(roixmlfn).getShape()).data
  true_dim = base.shape

  # Labelling new 
  label_used = False
  print "Labeling new ..."
  region_num = 1

  step = 1+(start*2)
  mstart = -start
  mend = start+1

  # Align new to scale factor
  xdim, ydim, zdim = map(ceil, np.array(base.shape)/float(step)) 
  resized_base = np.zeros((xdim*step, ydim*step, zdim*step), dtype=int)
  resized_base[:base.shape[0], :base.shape[1], :base.shape[2]] = base
  base = resized_base
  del resized_base

  # Create new matrix
  new = np.zeros_like(base) # poke my finger in the eye of malloc

  for z in xrange(start, base.shape[2]-start, step):
    for y in xrange(start, base.shape[1]-start, step):
      for x in xrange(start, base.shape[0]-start, step):

        if label_used: 
          region_num += 1 # only increase counter when a label was used
          label_used = False

        # set other (step*step)-1 around me to same region
        for zz in xrange(mstart,mend):
          for yy in xrange(mstart,mend):
            for xx in xrange(mstart,mend):
              if (base[x+xx,y+yy,z+zz]): # Masking
                label_used = True
                new[x+xx,y+yy,z+zz] = region_num
  
  new = new[:true_dim[0], :true_dim[1], :true_dim[2]] # shrink new to correct size
  print "Your atlas has %d regions ..." % new.max()
  img = nib.Nifti1Image(new, np.identity(4))
  
  print "Building atlas took %.3f sec ..." % (time()-start_time)
  return img

def validate(atlas_fn, roixmlfn, roirawfn):
  """
  Validate that an atlas you've created is a valid based on the
  masking you have

  @param atlas_fn: the new atlas you've created
  @param roixmlfn: xml mask file name
  @param roirawfn: raw mask file name
  """
  from operator import xor

  base = roi.ROIData (roirawfn, roi.ROIXML(roixmlfn).getShape()).data
  try:
    new = nib.load(atlas_fn).get_data()
  except:
    sys.stderr.write("[Error]: Loading file %s failed!\n" % atlas_fn);
    exit(-1)

  for i in xrange(new.shape[2]):
    for ii in xrange(new.shape[1]):
      for iii in xrange(new.shape[0]):
        if (xor(bool(new[i,ii,iii]), bool(base[i,ii,iii])) and base[i,ii,iii]==0):
          print "Created [%d,%d,%d] != 0 as it should be ..." % (i, ii, iii)

  print "Validation complete. If you saw no other messages then you atlas is valid!"


def main():
  parser = argparse.ArgumentParser(description="Downsample a fibergraph")
  parser.add_argument("roixmlfn", action="store", help="XML mask")
  parser.add_argument("roirawfn", action="store", help="RAW mask")
  parser.add_argument("-n","--niftifn",  action="store", default="atlas.nii", \
          help="Nifti outfile name if creating else the infile name if validation")
  parser.add_argument("-s", "--start", default=2, action="store", type=int, help="Start index")
  parser.add_argument("-v", "--validate", action="store_true", help="Perform validation")

  result = parser.parse_args()
  if result.validate:
    print "Validating %s..." % result.niftifn
    validate(result.niftifn, result.roixmlfn, result.roirawfn)
    exit(1)
  
  img = create(result.roixmlfn, result.roirawfn, result.start)
  nib.save(img, result.niftifn)

if __name__ == "__main__":
  main()
