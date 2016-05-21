#!/usr/bin/env python
# -*- coding: utf-8 -*-

import class_netsav, sys
from my_log import logger

if len(sys.argv) == 2:
   class_netsav.NetSav(sys.argv[1]).save()
else:
   logger.error(sys.argv[0]+" Error参数错误")
