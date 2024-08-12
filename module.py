#!/usr/bin/python
import os
import json


class Module(object):
    def __init__(self, manifest_data={}):
        self.data_dict = manifest_data
        self.is_valid = False

        self.id = self._parse_value("id")
        self.name = self._parse_value("name")
        self.title = self._parse_value("title")
        self.description = self._parse_value("description")
        self.authors = self._parse_value("authors")
        self.version = self._parse_value("version")
        self.url = self._parse_value("url")
        self.manifest = self._parse_value("manifest")
        self.download = self._parse_value("download")

        if self.manifest and self.download:
            self.is_valid = True

    def install_module(self, destination, ovveride_version=True):
        if self.is_valid:
            # Version Override
            if ovveride_version:
                self.version = "0.0.0"

            if not os.path.isdir(destination):
                os.mkdir(destination)

            if self.title:
                module_dir = os.path.join(destination, self.title)

                with open(os.path.join(module_dir, "module.json"), "w") as json_file:
                    json.dump(self.data_dict, json_file, indent="  ")

    def _parse_value(self, key):
        if key in self.data_dict:
            return self.data_dict[key]
        else:
            return None

    def debug(self):
        print(json.dumps(self.data_dict, indent=2))
