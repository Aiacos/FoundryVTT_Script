#!/usr/bin/python

import os
import argparse
import json
import sys
from tqdm import tqdm

import module


def dir_tester(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("Destination directory does not exist")

    return path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Install Foundry VTT modules from a file with links"
    )
    parser.add_argument("file", help="File containing links")
    parser.add_argument(
        "destination", type=dir_tester, help="Destination directory for modules"
    )

    return parser.parse_args()


def convert(file, destination):
    # Opening JSON file

    if not os.path.isdir(destination):
        print("Invalid Destination")

        return None

    if not os.path.isfile(file):
        print("Invalid File")

        return None

    f = open(file)

    # returns JSON object as
    # a dictionary
    data = json.load(f)
    module_list = data["modules"]
    filtered_links = []

    for mod in module_list:
        if "manifest" in mod:
            manifest = mod["manifest"]
            filtered_links.append(manifest)

    mod_instance_list = []
    for link in tqdm(filtered_links):
        # print(f"Downloading {link}... ", end="")

        module_instance = module.Module(link)
        module_instance.install_module(destination)
        mod_instance_list.append(module_instance)

    print("Skiped Modules: ")
    for mod in mod_instance_list:
        if mod.is_valid:
            print(" -- id: ", mod.id, "  -- name: ", mod.name)

        # print(f"Installed {module_instance.id}: {module_instance.title}")


def main():
    print()
    print("============================")
    print("Foundry VTT module installer")
    print("    By LorenzoArgentieri    ")
    print("============================")
    print()

    sys.stdout.flush()

    args = parse_args()
    convert(args.file, args.destination)


if __name__ == "__main__":
    main()
