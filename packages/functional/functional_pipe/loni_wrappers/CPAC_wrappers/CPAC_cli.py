#!/usr/bin/env python


# CPAC_cli.py
# command-line interface wrapper for CPAC utility
# Eric Bridgeford (ebridge2@jhu.edu) on 08/042015
# Copyright (c) 2015
from CPAC.pipeline.cpac_runner import run
from argparse import ArgumentParser

def cpac_cli(config, subs, pipe):
	#extract_data.run(args.config_file)
	#config = yaml.load(open(args.config_file,'r'))
	#subject_list_file = os.path.join(config.get('outputSubjectListLocation'),args.sub_list)
	run(config, subs, pipe)

def main():
	params = ArgumentParser()
	params.add_argument("-s","--sub_list", help = "the subject list. Must be in CPAC format.")
	params.add_argument("-c","--config_file",help = "the configuration file. Must be in CPAC format.")
	params.add_argument("-n","--pipe_name",help = "the pipeline name.")

	args = params.parse_args()
	cpac_cli(args.config_file, args.sub_list, args.pipe_name)

if __name__=='__main__':
	main()
