#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: manu
# @Date:   2014-10-11 19:33:49
# @Last Modified by:   Manuel VIVES
# @Last Modified time: 2014-10-11 21:14:09

from pyutils.file import human_readable_file_size, compute_metadata

ret = compute_metadata('tests/first_dummy_file', checksum_method=['sha1', 'md5', 'sha256'])
print(ret)
