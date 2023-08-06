# This file is placed in the Public Domain.

import unittest

from bot.obj import getmain
from bot.run import Cfg

k = getmain("k")

class Test_Kernel(unittest.TestCase):

    def test_cfg(self):
        self.assertEqual(type(k.cfg), Cfg)
