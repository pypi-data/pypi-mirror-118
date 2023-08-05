#
# Copyright (C) 2012 - 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Utility funtions to process file and file paths.
"""
import pathlib
import typing


def is_io_stream(obj: typing.Any) -> bool:
    """Is given object ``obj`` an IO stream, file or file-like object?
    """
    return callable(getattr(obj, 'read', False))


def get_path_from_stream(strm: typing.IO, safe: bool = False) -> str:
    """
    Try to get file path from given file or file-like object 'strm'.

    :param strm: A file or file-like object might have its file path info
    :return: file path or None
    :raises: ValueError
    """
    if not is_io_stream(strm) and not safe:
        raise ValueError(f'It does not look a file[-like] object: {strm!r}')

    path = getattr(strm, 'name', None)
    if path is not None:
        try:
            return str(pathlib.Path(path).resolve())
        except (TypeError, ValueError):
            pass

    return ''

# vim:sw=4:ts=4:et:
