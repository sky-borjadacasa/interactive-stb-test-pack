#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test cases for MySky
"""

import json
import requests

TSM_URL = 'http://vm006200:8080'
API_ANY_VCN = '/vcn/any_vcn'
API_VIP_VCN = '/vcn/vip_status'

def print_error(response):
    """Print error message from REST call
    """
    print 'Status code: {0}'.format(response.status_code)

def get_territory_param(territory):
    """Get the territory query string

    Args:
        territory (str): Territory of the user ()

    Returns:
        String that can be used in a REST request
    """
    if territory is None:
        return ''

    if territory.lower() == 'uk':
        return 'territory=uk'
    elif territory.lower() == 'roi':
        return 'territory=roi'
    else:
        return ''

def get_any_vcn(territory=None):
    """Get any valid VCN created in the last 6 months

    Args:
        territory (str): Territory of the user ()

    Returns:
        VCN that satisfies the given conditions
    """
    url = TSM_URL + API_ANY_VCN
    query = get_territory_param(territory)
    if len(query) > 0:
        url += '?'
        url += query

    response = requests.get(url)
    if response.ok:
        vcn = json.loads(response.text)
        return str(vcn)
    else:
        print_error(response)
    return ''

def get_vip_vcn(territory=None):
    """Get any valid VCN created in the last 6 months

    Args:
        territory (str): Territory of the user ()

    Returns:
        VCN that satisfies the given conditions
    """
    url = TSM_URL + API_VIP_VCN
    query = get_territory_param(territory)
    if len(query) > 0:
        url += '?'
        url += query

    response = requests.get(url)
    if response.ok:
        vcn = json.loads(response.text)[0]
        return str(vcn)
    else:
        print_error(response)
    return ''
