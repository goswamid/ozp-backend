"""
model access
"""
import logging
import re

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
import ozpcenter.models as models
import ozpcenter.utils as utils

# Get an instance of a logger
logger = logging.getLogger('ozp-center')


def get_storefront(username):
    """
    Returns data for /storefront api invocation including:
        * featured listings (max=12?)
        * recent (new) listings (max=24?)
        * most popular listings (max=36?)

    NOTE: think about adding Bookmark status to this later on
    """
    user = models.Profile.objects.get(user__username=username)
    try:
        # get featured listings
        featured_listings = models.Listing.objects.for_user(
            username).filter(
                is_featured=True,
                approval_status=models.Listing.APPROVED,
                is_enabled=True)[:12]

        # get recent listings
        recent_listings = models.Listing.objects.for_user(
            username).order_by(
                'approved_date').filter(
                    approval_status=models.Listing.APPROVED,
                    is_enabled=True)[:24]

        # get most popular listings via a weighted average
        most_popular_listings = models.Listing.objects.for_user(
            username).order_by(
            'avg_rate').filter(
                approval_status=models.Listing.APPROVED,
                is_enabled=True).order_by('-avg_rate')[:36]

        data = {
            'featured': featured_listings,
            'recent': recent_listings,
            'most_popular': most_popular_listings
        }
    except Exception as e:
        return {'error': True, 'msg': 'Error getting storefront: %s' % str(e)}
    return data


def get_metadata(username):
    """
    Returns metadata including:
        * categories
        * organizations (agencies)
        * listing types
        * intents
        * contact types

    Key: metadata
    """
    key = 'metadata'
    data = cache.get(key)
    if data is None:
        try:
            data = {}
            data['categories'] = models.Category.objects.all().values(
                'title', 'description')
            data['listing_types'] = models.ListingType.objects.all().values(
                'title', 'description')
            data['agencies'] = models.Agency.objects.all().values(
                'title', 'short_name', 'icon', 'id')
            data['contact_types'] = models.ContactType.objects.all().values(
                'name', 'required')
            data['intents'] = models.Intent.objects.all().values(
                'action', 'media_type', 'label', 'icon', 'id')

            # return icon/image urls instead of the id and get listing counts
            for i in data['agencies']:
                # i['icon'] = models.Image.objects.get(id=i['icon']).image_url()
                # i['icon'] = '/TODO'
                i['listing_count'] = models.Listing.objects.for_user(
                    username).filter(agency__title=i['title'],
                    approval_status=models.Listing.APPROVED).count()

            for i in data['intents']:
                # i['icon'] = models.Image.objects.get(id=i['icon']).image_url()
                i['icon'] = '/TODO'

            cache.set(key, data)
        except Exception as e:
            return {'error': True, 'msg': 'Error getting metadata: %s' % str(e)}
    return data