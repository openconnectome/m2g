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

# cpac_list_gen.py
# Created by Eric Bridgeford on 2015-05-14.
# Email: ebridge2@jhu.edu
# Copyright (c) 2015. All rights reserved.

from argparse import ArgumentParser
from os import listdir
from os.path import isdir, join
from re import compile, sub
from random import random
from numpy import floor

def make_list(subname, fmri, mprage, template, outlist):
  
  inf = open(template, 'r')
  content = inf.readlines()
  inf.close()
  out_data = list()

  p = compile('num|path')
  temp_sub =  content[:]
    
  subj_id = subname
  unique_id = floor(random()*pow(2,32))
  mprage_path = mprage
  fmri_path = fmri

  temp_sub[1] = p.sub("'"+subj_id+"'", temp_sub[1])
  temp_sub[2] = p.sub("'"+str(int(unique_id))+"'", temp_sub[2])
  temp_sub[3] = p.sub("'"+mprage_path+"'", temp_sub[3])
  temp_sub[5] = p.sub("'"+fmri_path+"'", temp_sub[5])
  out_data.append(temp_sub)
  
  ouf = open(outlist, 'w')
  for subj in out_data:
    for val in subj:
      ouf.write(val)
  ouf.close()

def main():
  parser = ArgumentParser(description="")
  parser.add_argument("subID", type=str, help="the name corresponding to the subject")
  parser.add_argument("fMRI", type=str, help="the fMRI corresponding to the subject")
  parser.add_argument("mprage",type=str, help="the mprage structural file for the subject.")
  parser.add_argument("outfile", help="the subject list in CPAC format")
  parser.add_argument("template",type=str,  help="the mprage corresponding to the subject")

  result = parser.parse_args()
  if result.template:
    make_list(result.subID, result.fMRI, result.mprage, result.template, result.outfile)
  else:
    make_list(result.data_dir, 'template_for_cpac.yml', result.outfile)

if __name__=='__main__':
  main()
