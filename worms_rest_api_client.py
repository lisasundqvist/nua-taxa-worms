#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (c) 2020-present SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import json
import urllib.request


class WormsRestApiClient:
    """ Python library for calling the REST API at World Register of Marine Species (WoRMS).
        REST API documentation: http://marinespecies.org/rest/
    """

    def __init__(self):
        """ """

    def get_aphia_id_by_name(self, scientific_name, marine_only=False):
        """ WoRMS REST: AphiaIDByName. """
        url = (
            "http://www.marinespecies.org/rest/AphiaIDByName/"
            + scientific_name
            + "?marine_only=false"
        )
        if marine_only:
            url = (
                "http://www.marinespecies.org/rest/AphiaIDByName/"
                + scientific_name
                + "?marine_only=true"
            )
        url = url.replace(" ", "%20")
        result = ""
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "Error: AphiaIDByName: "
                        + scientific_name
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = (
                "Error: AphiaIDByName: " + scientific_name + "  Exception: " + str(e)
            )
        #
        return (result, error)

    def get_record_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaRecordByAphiaID """
        url = "http://www.marinespecies.org/rest/AphiaRecordByAphiaID/" + str(aphia_id)
        # print(url)
        # url = url.replace(" ", "%20")
        result_dict = {}
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "Error: AphiaRecordByAphiaID: "
                        + str(aphia_id)
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = (
                "Error: AphiaRecordByAphiaID: "
                + str(aphia_id)
                + "  Exception: "
                + str(e)
            )
        #
        return (result_dict, error)

    def get_classification_by_aphiaid(self, aphia_id):
        """  WoRMS REST: AphiaClassificationByAphiaID """
        url = "http://www.marinespecies.org/rest/AphiaClassificationByAphiaID/" + str(
            aphia_id
        )
        # print(url)
        # url = url.replace(" ", "%20")
        result_dict = {}
        error = ""
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    result_dict = json.loads(response.read().decode("utf-8"))
                else:
                    error = (
                        "Error: AphiaClassificationByAphiaID: "
                        + str(aphia_id)
                        + "  Response code: "
                        + str(response.getcode())
                    )
        except Exception as e:
            error = (
                "Error: AphiaClassificationByAphiaID: "
                + str(aphia_id)
                + "  Exception: "
                + str(e)
            )
        #
        return (result_dict, error)

    def get_children_by_aphiaid(self, aphia_id):
        """  WoRMS REST: /AphiaChildrenByAphiaID/{ID} """
        url = "http://www.marinespecies.org/rest//AphiaChildrenByAphiaID/" + str(
            aphia_id
        )
        # print(url)
        # url = url.replace(" ", "%20")
        result_list = []
        response_list = []
        error = ""
        request_offset = 1
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 200:
                    response_list = json.loads(response.read().decode("utf-8"))
                elif response.getcode() == 204:
                    pass  # Normal case for leaf nodes.
                else:
                    error = (
                        "Error: AphiaChildrenByAphiaID: "
                        + str(aphia_id)
                        + "  Response code: "
                        + str(response.getcode())
                    )

            while (error == "") and (len(response_list) > 0):

                result_list += response_list

                if len(response_list) < 50:
                    response_list = []
                else:
                    response_list = []
                    request_offset += 50
                    url_next_chunk = url + "?offset=" + str(request_offset)
                    req = urllib.request.Request(url_next_chunk)
                    with urllib.request.urlopen(req) as response:
                        if response.getcode() == 200:
                            response_list = json.loads(response.read().decode("utf-8"))
                        elif response.getcode() == 204:
                            pass  # Normal case for leaf nodes.
                        else:
                            error = (
                                "Error: AphiaChildrenByAphiaID: "
                                + str(aphia_id)
                                + "  Response code: "
                                + str(response.getcode())
                            )

        except Exception as e:
            error = (
                "Error: AphiaChildrenByAphiaID: "
                + str(aphia_id)
                + "  Exception: "
                + str(e)
            )
        #

        print("DEBUG Number of children: ", len(result_list), " AphiaId:", aphia_id)

        return (result_list, error)
