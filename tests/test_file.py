#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: manu
# @Date:   2014-10-11 20:00:18
# @Last Modified by:   Manuel VIVES
# @Last Modified time: 2014-10-11 21:17:09

from pyutils.file import human_readable_file_size, compute_metadata
from pyutils.file import FileNotFound, NotAFile

import unittest
import os

first_dummy_file_path = os.getcwd() + os.sep + 'tests/first_dummy_file'


class TestFileModule(unittest.TestCase):
    def test_human_readable_file_size(self):
        self.assertEqual(human_readable_file_size(0), "0 B")
        self.assertEqual(human_readable_file_size(999), "999 B")
        self.assertEqual(human_readable_file_size(1023, False), "1023 B")
        self.assertEqual(human_readable_file_size(1024), "1.00 KB")
        self.assertEqual(human_readable_file_size(1100), "1.07 KB")
        self.assertEqual(human_readable_file_size(1000, True), "1.00 kiB")
        self.assertEqual(human_readable_file_size(1100, True), "1.10 kiB")
        self.assertEqual(human_readable_file_size(1100, True), "1.10 kiB")
        with self.assertRaises(TypeError):
            human_readable_file_size("test")

    def test_compute_metadate(self):
        with self.assertRaises(FileNotFound):
            compute_metadata('/pyutils')
        with self.assertRaises(NotAFile):
            compute_metadata('/tmp')
        wanted_ret = {
            'name': 'first_dummy_file',
            'size': '42 B',
            'path': first_dummy_file_path,
            'len': 42,
            'checksum': {
                'sha1': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
                'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
                'md5': 'd41d8cd98f00b204e9800998ecf8427e'
            },
            'mimetype': 'ASCII text'
        }
        self.assertEqual(compute_metadata(first_dummy_file_path, checksum_method=['sha1', 'md5', 'sha256']),
                         wanted_ret)
        wanted_ret = {
            'name': 'first_dummy_file',
            'size': '42 B',
            'path': first_dummy_file_path,
            'len': 42,
            'checksum': {
                'md5': 'd41d8cd98f00b204e9800998ecf8427e'
            },
            'mimetype': 'ASCII text'
        }
        self.assertEqual(compute_metadata(first_dummy_file_path, checksum_method='test'),
                         wanted_ret)


if __name__ == '__main__':
    unittest.main()
