#!/usr/bin/python

import os
import time
import json
import urllib.request as rq
import zipfile


class Module(object):
    def __init__(self, link=""):
        self.data_dict = self._parse_link(link)
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

            module_name = self.id if self.id else self.name

            if module_name:
                # module_dir = os.path.join(destination, self.id)

                if self.download:
                    file_name = (
                        module_name + ".zip"
                    )  # str(self.download).split("/")[-1]
                    full_path = os.path.join(destination, file_name)
                    rq.urlretrieve(self.download, full_path)

                    while not os.path.isfile(full_path):
                        time.sleep(0.1)

                    with zipfile.ZipFile(full_path, "r") as zip_ref:
                        zip_ref.extractall(destination + module_name)

                    os.remove(full_path)

                # if not os.path.isdir(module_dir):
                #    os.mkdir(module_dir)

                # with open(os.path.join(module_dir, "module.json"), "w") as json_file:
                #    json.dump(self.data_dict, json_file, indent="  ")

    def _parse_value(self, key):
        if key in self.data_dict:
            return self.data_dict[key]
        else:
            return None

    def _parse_link(self, link):
        json_data = {}

        try:
            with rq.urlopen(link) as url_file:
                json_data = json.load(url_file)

            if "manifest" not in json_data or "download" not in json_data:
                json_data = {}
                raise Exception()
        except Exception:
            # print("Module not found.")
            pass

        return json_data

    def _debug(self):
        print(json.dumps(self.data_dict, indent=2))
