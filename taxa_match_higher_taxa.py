#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2020-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import datetime


class SharkSpeciesListGenerator:
    """ 
        For usage instructions check "https://github.com/sharkdata/species".
    """

    def __init__(self):
        """ """
        self.clear()

    def clear(self):
        """ """
        self.taxa_worms_header = {}
        self.taxa_worms_dict = {}  # Key: scientific_name.
        #
        self.indata_not_processed = []

    def run_all(self):
        """ """
        print("\nStarted...\n")

        self.import_taxa_worms()
        self.import_indata_not_processed()

        match_result_path = pathlib.Path("data_out/match_higher_taxa_results.txt")
        match_result_file = match_result_path.open("w")
        match_result_file.write("scientific_name" + "\n")

        for row in self.indata_not_processed:
            if row in self.taxa_worms_dict:
                print("OK:\t", row)
                match_result_file.write(row + "\t" + "OK" + "\n")
            else:
                print("Missing:\t", row)
                match_result_file.write(row + "\t" + "Missing" + "\n")

        print("\n...done")
        match_result_file.close()

    def import_taxa_worms(self):
        """ """
        indata_worms = pathlib.Path("data_out/taxa_worms.txt")
        if indata_worms.exists():
            print("Importing file: ", indata_worms)
            with indata_worms.open(
                "r", encoding="cp1252", errors="ignore"
            ) as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split("\t")]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get("scientific_name", "")
                        if scientific_name:
                            #                             self.old_taxa_worms_dict[scientific_name] = row_dict
                            self.taxa_worms_dict[scientific_name] = row_dict
            print("")

    def import_indata_not_processed(self):
        """ """
        indata_path = pathlib.Path("data_out/indata_not_valid_names.txt")
        if indata_path.exists():
            print("Importing file: ", indata_path)
            with indata_path.open(
                "r", encoding="cp1252", errors="ignore"
            ) as indata_file:
                header = None
                for row in indata_file:
                    row = [item.strip() for item in row.strip().split("\t")]
                    if header is None:
                        header = row
                    else:
                        row_dict = dict(zip(header, row))
                        scientific_name = row_dict.get("scientific_name", "")
                        if scientific_name:
                            #                             self.old_taxa_worms_dict[scientific_name] = row_dict
                            self.indata_not_processed.append(scientific_name)
            print("")


# === MAIN ===
if __name__ == "__main__":
    """ """
    taxa_mgr = SharkSpeciesListGenerator()
    print("\nStarted.", datetime.datetime.now(), "\n")
    taxa_mgr.run_all()
    print("\nEnded.", datetime.datetime.now(), "\n")

