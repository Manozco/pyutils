#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: manu
# @Date:   2014-10-11 19:33:20
# @Last Modified by:   manu
# @Last Modified time: 2014-10-11 20:59:04
from pyutils import exceptions

from typedecorator import params, Union, returns
import magic

import os
import math
import hashlib


class FileNotFound(exceptions.PyUtilsException):
    """raised when no file is found"""
    pass


class NotAFile(exceptions.PyUtilsException):
    """raised when it is not a file"""
    pass


@returns(str)
@params(file_len=int, si=bool)
def human_readable_file_size(file_len, si=False):
    unit = 1000 if si else 1024
    if file_len < unit:
        return "{} B".format(file_len)
    exp = int(math.log10(file_len) / math.log10(unit))
    pre = "kMGTPE"[exp - 1] + 'i' if si else "KMGTPE"[exp-1]
    return "{0:.2f} {pre}B".format(file_len / math.pow(unit, exp), pre=pre)


@returns((str, str))
@params(file_path=str, algorithm=str, blocksize=int)
def hash_file(file_path, algorithm, blocksize=65536):
    hasher = getattr(hashlib, algorithm, None)
    if not hasher:
        algorithm = 'md5'
        hasher = getattr(hashlib, algorithm, None)
    fd = open(file_path, 'rb')
    buf = fd.read(blocksize)
    while len(buf) > 0:
        hasher().update(buf)
        buf = fd.read(blocksize)
    return(algorithm, hasher().hexdigest())


@returns(dict)
@params(file_path=str, checksum_method=Union(str, [str]))
def compute_metadata(file_path, checksum_method='md5'):
    if not os.path.exists(file_path):
        raise FileNotFound(file_path)
    if not os.path.isfile(file_path):
        raise NotAFile(file_path)
    ret = {
        'name': "",
        'path': file_path,
        'len': 0,
        'size': "0 B",
        'checksum': {
        },
        'mimetype': "application/octet-stream"
    }
    ret['name'] = os.path.basename(file_path)
    ret['len'] = os.stat(file_path).st_size
    ret['size'] = human_readable_file_size(ret['len'])
    ret['mimetype'] = magic.from_file(file_path).decode('utf-8')
    checksums = [checksum_method, ] if isinstance(checksum_method, str) else checksum_method
    for c in checksums:
        res = hash_file(file_path, c)
        ret['checksum'][res[0]] = res[1]
    return ret
