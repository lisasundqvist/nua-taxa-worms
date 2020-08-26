#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2020-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import datetime


class SharkSpeciesListGenerator:
    """ 
        
    """

    def __init__(self):
        """ """
        self.clear()

    def clear(self):
        """ """
        self.taxa_worms_header = {}
        self.taxa_worms_dict = {}  # Key: scientific_name.
        #
        self.define_out_headers()

    def define_out_headers(self):
        """ """
        self.taxa_worms_header = [
            "scientific_name",
            "rank",
            "aphia_id",
            "parent_name",
            "parent_id",
            "authority",
            "status",
            "kingdom",
            "phylum",
            "class",
            "order",
            "family",
            "genus",
            "classification",
            #             "isBrackish",
            #             "isExtinct",
            #             "isFreshwater",
            #             "isMarine",
            #             "isTerrestrial",
            #             "unacceptreason",
            #             "valid_AphiaID",
            #             "valid_authority",
            #             "valid_name",
            #             "citation",
            #             "url",
            #             "lsid",
            #             "match_type",
            #             "modified",
        ]

    def run_all(self):
        """ """
        print("\nClassification generator started.")
        self.import_taxa_worms()

        # Step 8. Add classification.
        for scientific_name in list(self.taxa_worms_dict.keys()):
            classification_list = []
            taxon_dict = self.taxa_worms_dict[scientific_name]
            while taxon_dict:
                classification_list.append(
                    "["
                    + taxon_dict.get("rank", "")
                    + "] "
                    + taxon_dict.get("scientific_name", "")
                )
                # Parents.
                parent_name = taxon_dict.get("parent_name", "")
                taxon_dict = self.taxa_worms_dict.get(parent_name, None)
            #
            self.taxa_worms_dict[scientific_name]["classification"] = " - ".join(
                classification_list[::-1]
            )

        # Step 10. Save the results.
        self.save_taxa_worms_with_classification()

        print("\nDone...")

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

    def save_taxa_worms_with_classification(self):
        """ """
        # Sort by classification.
        classification_dict = {}
        for row_dict in self.taxa_worms_dict.values():
            classification_dict[row_dict["classification"]] = row_dict
        #
        taxa_worms_file = pathlib.Path("data_out/taxa_worms_with_classification.txt")
        with taxa_worms_file.open(
            "w", encoding="cp1252", errors="ignore"
        ) as outdata_file:
            outdata_file.write("\t".join(self.taxa_worms_header) + "\n")
            #             for _taxa, taxa_rec in self.taxa_worms_dict.items():
            for key in sorted(classification_dict.keys()):
                taxa_rec = classification_dict[key]
                row = []
                for header_item in self.taxa_worms_header:
                    row.append(str(taxa_rec.get(header_item, "")))
                try:
                    outdata_file.write("\t".join(row) + "\n")
                except Exception as e:
                    try:
                        print(
                            "Exception when writing to taxa_worms.txt: ",
                            row[0],
                            "   ",
                            e,
                        )
                    except:
                        pass


# === MAIN ===
if __name__ == "__main__":
    """ """
    taxa_mgr = SharkSpeciesListGenerator()
    print("\nStarted.", datetime.datetime.now(), "\n")
    taxa_mgr.run_all()
    print("\nEnded.", datetime.datetime.now(), "\n")
