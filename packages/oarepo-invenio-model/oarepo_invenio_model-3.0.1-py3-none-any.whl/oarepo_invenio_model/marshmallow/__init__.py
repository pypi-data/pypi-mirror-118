# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CIS UCT Prague.
#
# CIS theses repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JSON Schemas."""

from __future__ import absolute_import, print_function

from flask_login import current_user
from invenio_records_rest.schemas.fields import GenFunction
from invenio_records_rest.schemas.fields.persistentidentifier import pid_from_context
from invenio_rest.serializer import BaseSchema as Schema
# noinspection PyUnusedLocal
from marshmallow import INCLUDE, RAISE, fields, missing, pre_load


def pid_from_context_or_data(value, context, **kwargs):
    """Get PID from marshmallow context."""
    pid = (context or {}).get('pid')
    if pid is None:
        return value
    else:
        return pid.pid_value


class PersistentIdentifier(GenFunction):
    """Field to handle PersistentIdentifiers in records.

    .. versionadded:: 1.2.0
    """

    def __init__(self, *args, **kwargs):
        """Initialize field."""
        super(PersistentIdentifier, self).__init__(
            serialize=pid_from_context, deserialize=pid_from_context_or_data,
            *args, **kwargs)


# def schema_from_context(_, context):
#     """Get the record's schema from context."""
#     record = (context or {}).get('record', {})
#     return record.get("_schema", missing)
#
#
# def bucket_from_context(_, context):
#     """Get the record's bucket from context."""
#     record = (context or {}).get('record', {})
#     return record.get('_bucket', missing)
#
#
# def files_from_context(_, context):
#     """Get the record's files from context."""
#     record = (context or {}).get('record', {})
#     return record.get('_files', missing)
#
#
# def get_id(obj, context):
#     """Get record id."""
#     pid = context.get('pid')
#     return pid.pid_value if pid else missing


class InvenioRecordMetadataSchemaV1Mixin(Schema):
    InvenioID = PersistentIdentifier()
    _schema = fields.String(
        attribute="$schema",
        data_key="$schema",
    )
    _submitter = fields.String(data_key='oarepo:submitter', attribute='oarepo:submitter')

    @pre_load
    def set_oarepo_submitter(self, data, **kwargs):
        """Set oarepo:submitter to record metadata if not known."""
        if not data.get('oarepo:submitter'):
            if current_user and current_user.is_authenticated:
                data['oarepo:submitter'] = current_user.email
            else:
                data['oarepo:submitter'] = 'anonymous'
        return data



class FileSchema(Schema):
    class Meta:
        unknown = INCLUDE


class InvenioRecordMetadataFilesMixin(Schema):
    _files = fields.Nested(FileSchema, many=True, data_key='_files', required=False)
    _bucket = fields.String(required=False)

