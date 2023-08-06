#!/usr/bin/env python

import sys
import os

import yaml

USAGE_INFO = 'Usage: ggsr --help\n' \
             '       ggsr <config filename>'

dirname = os.path.split(os.path.abspath(os.path.realpath(sys.argv[0])))[0]

HELP_INFO = 'ggsr is a program for designing SCHEMA-RASPP libraries with ' \
            'Golden Gate Assembly.\n\n' \
            'The following procedure will design a library that can ' \
            'be assembled with BsaI Golden Gate Assembly into a vector with ' \
            'BsaI overhangs: \n' \
            '    1. Make a new directory.\n' \
            '    2. Copy a fasta file with your parent names and sequences ' \
            'into the directory.\n' \
            '    3. Optionally copy a .pdb file with structure information ' \
            'related to your parent sequences into the directory.\n' \
            f'    4. Inside the directory, run "cp {dirname}/' \
            'run_config.yaml ."\n' \
            '    5. Edit this configuration file according to your library' \
            ' requirements.\n' \
            '    6. Run "nohup ggsr run_config.yaml &> ggsr.log &".\n\n' \
            f'Alternatively, run "cp -r {dirname} <new directory name>",' \
            ' edit the stepx.py scripts, and run them individually to ' \
            'get more flexibility.\n' \
            'View https://github.com/RomeroLab/SCHEMA-library-design/wiki ' \
            'for more information.'

if len(sys.argv) != 2:
    print(USAGE_INFO)
    sys.exit()

if sys.argv[1] == '--help':
    print(HELP_INFO)
    sys.exit()

with open(sys.argv[1]) as f:
    config_map = yaml.safe_load(f)

excluded_steps = config_map['excluded_steps']

if 1 not in excluded_steps:
    sys.argv = [sys.argv[0], config_map['seq_fn'], config_map['pdb_fn'],
                config_map['out_prefix']]
    run_args = [str(c)+' ' for c in sys.argv]
    run_args[0] = 'step1.py '
    print('Running:', ''.join(run_args))
    exec(open(dirname + '/step1.py').read())
    print('Step1 done\n')

if 2 not in excluded_steps:
    sys.argv = [sys.argv[0],
                config_map['num_bl'], config_map['minBL'], config_map['maxBL'],
                config_map['start_oh_seq'], config_map['start_oh_pos'],
                config_map['end_oh_seq'], config_map['end_oh_pos'],
                config_map['out_prefix']+'_AA.fasta',
                config_map['out_prefix']+'_contacts.json',
                config_map['libraries_fn']]
    run_args = [str(c)+' ' for c in sys.argv]
    run_args[0] = 'step2.py '
    print('Running:', ''.join(run_args))
    exec(open(dirname + '/step2.py').read())
    print('Step2 done\n')

if 3 not in excluded_steps:
    sys.argv = [sys.argv[0], config_map['libraries_fn'],
                config_map['gg_prob_threshold'], config_map['chosen_lib_fn']]
    run_args = [str(c)+' ' for c in sys.argv]
    run_args[0] = 'step3.py '
    print('Running:', ''.join(run_args))
    exec(open(dirname + '/step3.py').read())
    print('Step3 done\n')

if 4 not in excluded_steps:
    sys.argv = [sys.argv[0], config_map['out_prefix']+'_AA.fasta',
                config_map['out_prefix']+'_CDN.fasta',
                config_map['chosen_lib_fn'], config_map['frags_order_fn']]
    run_args = [str(c)+' ' for c in sys.argv]
    run_args[0] = 'step4.py '
    print('Running:', ''.join(run_args))
    exec(open(dirname + '/step4.py').read())
    print('Step4 done')
