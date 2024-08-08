#!/usr/bin/python

import argparse
import json
import os
import re
import sys
import urllib.request
from tqdm import tqdm


def dir_tester(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError('Destination directory does not exist')

    return path


def parse_args():
    parser = argparse.ArgumentParser(description='Install Foundry VTT modules from a file with links')
    parser.add_argument('--filters', nargs='*', help='Link filters')
    parser.add_argument('file', help='File containing links')
    parser.add_argument('destination', type=dir_tester, help='Destination directory for modules')

    return parser.parse_args()


def convert(file, destination, filters):
    # Opening JSON file
    print('File: ', file, type(file))
    f = open(file)

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    module_list = data['modules']
    filtered_links = []

    try:
        for mod in module_list:
            manifest = mod['manifest']
            filtered_links.append(manifest)
    except:
        print('No Manifest Found on: ', mod['id'])


    for link in tqdm(filtered_links):
        print(f'Downloading {link}... ', end='')

        try:
            with urllib.request.urlopen(link) as url_file:
                json_data = json.load(url_file)

            if 'manifest' not in json_data or 'download' not in json_data:
                raise Exception()
        except Exception:
            print('Module not found.')
            continue

        print('Done.')



        id = json_data['id']
        title = json_data['title']
        description = json_data['description']
        author = json_data['author']
        name = json_data['name']
        version = json_data['version']
        manifest = json_data['manifest']
        download = json_data['download']

        module_dir = os.path.join(destination, name)

        json_data['version'] = '0.0.0'

        print('-- Module: ', title)
        print(name, id, manifest)

        #if not os.path.isdir(module_dir):
        #    os.mkdir(module_dir)

        #with open(os.path.join(module_dir, 'module.json'), 'w') as json_file:
        #    json.dump(json_data, json_file, indent='  ')

        print(f'Installed {name}: {title}')


def main():
    print()
    print('============================')
    print('Foundry VTT module installer')
    print('    By LorenzoArgentieri    ')
    print('============================')
    print()

    sys.stdout.flush()

    args = parse_args()
    convert(args.file, args.destination, args.filters)


if __name__ == '__main__':
    main()
