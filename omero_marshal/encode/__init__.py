#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENCE file
# you can find at the root of the distribution bundle.
# If the file is missing please request a copy by contacting
# jason@glencoesoftware.com.
#

from omero import RType
from omero_model_UnitBase import UnitBase
from omero.rtypes import unwrap


class Encoder(object):

    TYPE = ''

    def __init__(self, ctx):
        self.ctx = ctx

    def set_if_not_none(self, v, key, value):
        if value is None:
            return
        if isinstance(value, RType):
            v[key] = value.getValue()
        if isinstance(value, UnitBase):
            self.encode_unit(v, key, value)

    def encode_unit(self, v, key, value):
        unit_name = value.getUnit().__class__.__name__
        v[key] = {
            '@type': 'TBD#%s' % value.__class__.__name__,
            'Unit': {
                '@type': 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
                         '#%s' % unit_name,
                '@id': value.getSymbol(),
                'Name': value.getUnit().name
            },
            'Value': value.getValue()
        }

    def encode(self, obj):
        v = {'@type': self.TYPE}
        if hasattr(obj, 'id'):
            obj_id = unwrap(obj.id)
            if obj_id is not None:
                v['@id'] = obj_id
        if hasattr(obj, 'details'):
            encoder = self.ctx.get_encoder(obj.details.__class__)
            v['omero:details'] = encoder.encode(obj.details)

        return v
