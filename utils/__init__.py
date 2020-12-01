#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-27 16:34:52
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$


def get_name(obj):
    return obj.__class__.__name__


def get_property(obj, prop):
    return obj[prop]
