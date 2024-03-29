"""
Serializers
"""
import logging

from rest_framework import serializers

import ozpcenter.models as models

# Get an instance of a logger
logger = logging.getLogger('ozp-center')

class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactType