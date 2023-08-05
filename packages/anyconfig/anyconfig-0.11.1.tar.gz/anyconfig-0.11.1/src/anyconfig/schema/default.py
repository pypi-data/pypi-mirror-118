#
# Copyright (C) 2015 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=unused-argument
"""Default (dummy) implementation.
"""
import typing

from ..common import (
    InDataT, InDataExT
)
from .datatypes import ResultT


def validate(data: InDataExT, schema: InDataT, ac_schema_safe: bool = True,
             ac_schema_errors: bool = False, **options: typing.Any
             ) -> ResultT:
    """
    Dummy function does not validate at all in actual.
    """
    return (True, 'Validation module (jsonschema) is not available')


def is_valid(data: InDataExT, schema: InDataT, ac_schema_safe: bool = True,
             ac_schema_errors: bool = False, **options) -> bool:
    """
    Dummy function never raise exceptions.
    """
    return True


def gen_schema(data: InDataExT, **options) -> InDataT:
    """
    Dummy function generates an empty dict in actual.
    """
    return dict()


# vim:sw=4:ts=4:et:
