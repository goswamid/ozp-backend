"""
Model access
"""
import json
import logging

import ozpiwc.models as models
import ozpiwc.errors as errors

# Get an instance of a logger
logger = logging.getLogger('ozp-center')

def get_data_resource(username, key):
    return models.DataResource.objects.filter(
                key=key, username=username).first()

def get_all_keys(username):
    return models.DataResource.objects.filter(username=username).values_list(
        'key', flat=True)