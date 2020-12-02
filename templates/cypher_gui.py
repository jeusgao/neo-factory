#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-30 21:06:02
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$

import os
import math
import pandas as pd
import streamlit as st
from configuration import NEO_FIELDS
from models import g, build_cypher, NeoSeeker

seeker = NeoSeeker()


def _update_commit(df):
    if len(df):
        for r in df.iterrows():
            _cypher = build_cypher(r[1])
            st.text(f'!!!BOOM!!! \t{_cypher}')
            g.run(_cypher)


def _input_template(action='U'):
    # a_label = st.selectbox('Start node label:', list(NEO_FIELDS.Node_labels))
    a_label = st.text_input('Start node(Node A) label:')
    a_properties = None
    if action == 'U':
        a_properties = st.text_input('Start Node key-values properties, separate with comma:')
        st.markdown(
            'a set of KEY:VALUEs  *[value 如果是静态字符串需要用单引号引起来]*' +
            '\n\n\t' +
            "{USER_NAME:'张三', USER_CODE:'010101'}")
    # b_label = st.selectbox('End node label:', list(NEO_FIELDS.Node_labels))
    # r_type = st.selectbox('Relationship types', list(NEO_FIELDS.R_types))
    b_label = st.text_input('End node(Node B) label:')
    path_type = st.radio('Need Relationship?:', ('NONE', 'RELATION', 'Shortest', 'AllShortests'))
    r_type = None
    if path_type == 'RELATION':
        r_type = st.text_input('Relationship types:')
    p_depth = 1
    if path_type in ['Shortest', 'AllShortests']:
        p_depth = st.slider('Path depth:', min_value=1, max_value=10, value=1, step=1)
    r_properties = None
    if action == 'U':
        r_properties = st.text_input('Relationship key-values properties, separate with comma:')
        st.markdown(
            'a set of KEY:VALUEs  *[value 如果是静态字符串需要用单引号引起来]*' +
            '\n\n\t' +
            "{R_NAME:'部门成员', R_SORT:10}")
    conditions = st.text_input('Where conditions:')
    st.markdown(
        'a.key=avalue [and|or|>|<|contains ...] a.key2=b.value2...  *[value 如果是静态值需要用单引号引起来]*' +
        '\n\n\t' +
        "(a.USER_LOGIN_NAME='gaojinsong00' or a.USER_NAME contains '高') and b.DEPT_CODE='LR021201'")

    a_label = f'{a_label}' if a_label else None
    b_label = f'{b_label}' if b_label else None
    r_type = f'{r_type}' if r_type else None

    return a_label, a_properties, b_label, path_type, p_depth, r_type, r_properties, conditions


def _line_update():
    a_label, a_properties, b_label, path_type, p_depth, r_type, r_properties, conditions = _input_template()

    output = st.selectbox('Return command', list(NEO_FIELDS.Outputs.keys()))
    output_param = st.text_input('command params:').replace(output, '')

    st.markdown(NEO_FIELDS.Outputs.get(output), unsafe_allow_html=False)

    df = pd.DataFrame({
        'a_label': a_label,
        'a_properties': a_properties,
        'b_label': b_label,
        'path_type': path_type,
        'p_depth': p_depth,
        'r_type': r_type,
        'r_properties': r_properties,
        'conditions': conditions,
        'output': f'{output} {output_param}'
    }, index=[0])
    table = st.dataframe(df)

    _submit = st.button('Commit')

    if _submit and a_label:
        _update_commit(df)


def _upload_file():
    df = pd.DataFrame(columns=['a_label', 'a_properties', 'b_label', 'path_type', 'p_depth', 'r_type', 'r_properties', 'conditions', 'output'])
    file = st.file_uploader("上传CSV/TSV文件", type=["csv", "tsv"])

    if file:
        df = pd.read_csv(file)
        table = st.dataframe(df)

    _submit = st.button('Commit')
    if _submit and file:
        _update_commit(df)


def _update():
    _way = st.radio('Update way:', ('Batch input', 'Line input'))
    if _way == 'Batch input':
        _upload_file()
    else:
        _line_update()


def _match():
    a_label, a_properties, b_label, path_type, p_depth, r_type, r_properties, conditions = _input_template(action='M')
    output = st.multiselect('选择输出项(RETURN)', ['a: Start node', 'b: End node', 'r: Relationship'])
    st.markdown('*[输出项可多选，留空时默认输出所有元素]*')
    output = ','.join([o[0] for o in output])
    output = output if output else '*'

    df = pd.DataFrame({
        'a_label': a_label,
        'a_properties': a_properties,
        'b_label': b_label,
        'path_type': path_type,
        'p_depth': p_depth,
        'r_type': r_type,
        'r_properties': r_properties,
        'conditions': conditions,
        'output': output
    }, index=[0])

    _cypher = build_cypher(list(df.iterrows())[0][1], action='M')
    st.markdown('#### $\color{#1E90FF}{!!! Cypher BOOM !!! }$ *Check your cypher scripts below, copy or run it.*' +
                '\n\n\t' +
                _cypher)

    _submit = st.button('RUN')
    if _submit:
        try:
            result = seeker.get_sres_by_cypher(_cypher)
            st.json(result)
        except Exception as Err:
            st.warning(Err)


def runner(title=''):
    _task_type = st.sidebar.radio('Select cypher task:', ('Match', 'Update'))
    st.success(f'{title} - {_task_type}')
    if _task_type == 'Update':
        _update()
    else:
        _match()
