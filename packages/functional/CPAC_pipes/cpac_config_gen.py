#!/usr/bin/env python



from argparse import ArgumentParser
from os import listdir
from re import compile, sub
from random import random
from numpy import floor

def make_list(outpath, template, config):
  
  inf = open(str(template), 'r')
  content = inf.readlines()
  inf.close()

  p = compile('num|path')
  temp_sub =  content[:]
  
  out_data = list()

  temp_sub[45] = temp_sub[45].replace('path',outpath + '/working')
  print(outpath + '/outputs')
  temp_sub[49] = p.sub(outpath + '/crash', temp_sub[49])
  temp_sub[53] = p.sub(outpath + '/outputs', temp_sub[53])
  
  out_data.append(temp_sub)
  
  ouf = open(config, 'w')
  for line in out_data:
    for val in line:
      ouf.write(val)
  ouf.close()

def main():
  parser = ArgumentParser(description="")
  parser.add_argument("path", help="base directory in which cpac outputs will be placed")
  parser.add_argument("config", help="output config file")
  parser.add_argument("-t","--template", help="template for cpac config")

  result = parser.parse_args()
  if result.template:
    make_list(result.path, result.template, result.config)
  else:
    make_list(result.path, 'template_cpac_config.yml', result.config)

if __name__=='__main__':
  main()
