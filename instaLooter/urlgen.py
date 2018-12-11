# coding: utf-8
"""
instaLooter.urlgen
==================

Contains several url generators that can be passed as ``url_generator``
argument to the ``InstaLooter`` constructor.
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import re

__all__ = ["default", "resizer", "thumbnail"]


DEFAULT_RX = re.compile(r'(https://.*?/.*?/).*(/.*\.jpg)')
NEW_DEFAULT_RX = re.compile(r'(https://.*?/h-ak-igx/).*(/.*\.jpg)')
RESIZER_RX = re.compile(r"(s[0-9x]*/)?(e[0-9]*)/")


def default(media):
    """Generates a link to the default picture, without processing effects.
    """
    result = NEW_DEFAULT_RX.search(media['display_src'])

    return 'anything'.join(result.groups()) \
        if result is not None \
      else ''.join(DEFAULT_RX.search(media['display_src']).groups())


def resizer(size):
    """Creates a generator that generate a link to a scaled picture.

    Aspect ratio is not modified, and the largets of the two
    dimensions of the picture will equal to ``size`` once it
    is transformed.
    """
    target = 's{0}x{0}/'.format(size)
    def resize(media):
        return RESIZER_RX.sub(target, media['display_src'])
    resize.__doc__ = "Generates a link to a picture {} pixels large.".format(size)
    return resize


def thumbnail(media):
    """Generates a link to the thumbnail.
    """
    try:
        return media['thumbnail_src']
    except KeyError:
        url_parts = media['display_src'].split('/')
        url_parts.insert(4, 'c121.0.669.669')
        url_parts.insert(5, 's640x640')
        return '/'.join(url_parts)
