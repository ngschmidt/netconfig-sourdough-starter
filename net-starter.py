#!/usr/bin/python3
# Jinja Network Device Builder
# Nicholas Schmidt
# 28 May 2021

# Command line parsing imports
import argparse

# Import System calls
import sys

# YAML. Used for human inputs

from ruamel.yaml import YAML
from ruamel.yaml import scanner

# JSON. Used for non-human inputs

import json

# Cerberus. Used to validate human and non-human inputs

from cerberus import Validator

# Templates. Basically the core to what we're doing here.

from jinja2 import Environment, FileSystemLoader

# Arguments Parsing
parser = argparse.ArgumentParser(description='Process YAML Inputs')
parser.add_argument('-v', '--verbosity', action='count', default=0, help='Output Verbosity')
parser.add_argument('--gen-kind', help='Generate a device file to customize. Pass this a kind to generate against')
parser.add_argument('--gen-test', help='Generate a truth file based on hashed data to be consumed by the testing framework')
parser.add_argument('--test', help='Perform a self-test')
parser.add_argument('-o', help='Output file')
parser.add_argument('-i', '--input', help='Input. Pass this a YAML file')
args = parser.parse_args()

# Load Templates folder as Jinja2 root
local_env = Environment(loader=FileSystemLoader('templates'))

# Load Definition Classes
yaml_input = YAML(typ='safe')
yaml_dict = {}

# Input can take a file first, but will fall back to YAML processing of a string
try:
    yaml_dict = yaml_input.load(open(args.input, 'r'))
except FileNotFoundError:
    print('I2000: Not found as file, trying as a string...')
    yaml_dict = yaml_input.load(args.input)
except scanner.ScannerError as exc:
    # Test for malformatted yaml
    print('E1001: YAML Parsing error!')
    if (args.verbosity > 0):
        print(exc)
except Exception as exc:
    # Fallback error dump
    print('E9999: An unknown error has occurred!')
    if (args.verbosity > 0):
        print(exc)
        print(type(exc))
        print(exc.args)
else:
    if args.verbosity > 0:
        print(json.dumps(yaml_dict, indent=4))
finally:
    print("Valid YAML Found! Executing Template Actions...")

# Set Templates and Validators now that we know what to validate against

try:
    device_kind = yaml_dict['kind']
except KeyError as e:
    sys.exit('E1101: Device kind not found! Could not find key ' + str(e))
finally:
    device_template = local_env.get_template(yaml_dict['kind'] + '.j2')

# Do stuff with the data!

# Generate Overall Configuration file
output_output = ""
output_output += device_template.render(yaml_dict)
output_output += "\n"

# Do interfaces
for i in yaml_dict['interfaces']:
    try:
        interface_kind = i['kind']
    except KeyError as e:
        sys.exit('E1102: Interface kind not found! Could not find key ' + str(e))
    finally:
        interface_template = local_env.get_template(i['kind'] + '.j2')
        output_output += interface_template.render(i)

print(output_output)

# Write all that to a file
if(args.o):
    try:
        filehandle = open(args.o, "w")
        filehandle.write(output_output)
        filehandle.close()
    except:
        sys.exit("Error writing to file!")
