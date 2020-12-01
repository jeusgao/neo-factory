#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-27 16:28:46
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import os
import streamlit as st

from templates.cypher_gui import runner


def main():
    # st.balloons()
    st.sidebar.subheader('通讯录')
    _action_type = st.sidebar.radio('', ('Cypher接口', '查询', '新增', '编辑', ))
    title = st.empty()

    if _action_type == 'Cypher接口':
        runner(title=_action_type)

if __name__ == '__main__':
    if is_login:
        main()
