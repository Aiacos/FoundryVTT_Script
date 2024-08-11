#!/usr/bin/python
import os
import json


class Module(object):
    def __init__(self, manifest_data={}):
        self.data_dict = manifest_data
        self.is_valid = False

        id = self._parse_value("id")
        title = self._parse_value("title")
        description = self._parse_value("description")
        authors = self._parse_value("authors")
        version = self._parse_value("version")
        manifest = self._parse_value("manifest")
        download = self._parse_value("download")

        if manifest:
            if download:
                # Ovveride version:
                version = "0.0.0"
                self.is_valid = True

    def install_module(self, module_dir):
        if self.is_valid:
            if not os.path.isdir(module_dir):
                os.mkdir(module_dir)

            with open(os.path.join(module_dir, "module.json"), "w") as json_file:
                json.dump(self.data_dict, json_file, indent="  ")

    def _parse_value(self, key):
        if key in self.data_dict:
            return self.data_dict[key]
        else:
            return None
