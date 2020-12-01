#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-27 16:29:37
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

# from collections import OrderedDict
# from sessionstate import SessionState

# import hashlib
# import streamlit as st

# state = SessionState.get(rerun=False, login_info=OrderedDict())


# def _get_password(un, pw):
#     m = hashlib.md5()
#     m.update(f'{un}{pw}'.encode(encoding='utf-8'))
#     return m.hexdigest()


# def is_authenticated(username, password):
#     password = _get_password(username, password)
#     up = dic_users.get(username).get('password')
#     return password == up


# def generate_login_block():
#     block0 = st.empty()
#     block1 = st.empty()
#     block2 = st.empty()
#     block3 = st.empty()

#     return block0, block1, block2, block3


# def clean_blocks(blocks):
#     for block in blocks:
#         block.empty()


# def is_login(username):
#     if username in state.login_info:
#         return True
#     else:
#         login_blocks = generate_login_block()
#         _, username, password, _ = login(login_blocks)

#         if is_authenticated(username, password):
#             login_info.text(username)
#             state.login_info[username] = 'OK'
#             clean_blocks(login_blocks)
#             return True
#         elif password:
#             st.info("Please enter a valid password")
#     return False
