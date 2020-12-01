#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-11-20 22:41:00
# @Author  : Joe Gao (jeusgao@163.com)
# @Link    : https://www.jianshu.com/u/3b77f85cc918
# @Version : $Id$
import time
import uuid

from ZODB import DB
from ZODB.FileStorage import FileStorage
from ZODB.PersistentMapping import PersistentMapping
from Persistence import Persistent
import transaction


def make_uid(pkey):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, pkey))


class Record(Persistent):
    """An entity"""

    def __init__(self, body):
        self.body = body


def map_root(root, code):
    if code not in root:
        root[code] = {}
    return root[code]


def add_records(root, code, bodys):
    records = map_root(root, code)
    for k, v in bodys.items():
        records[k] = Record(v)
    root[code] = records


def get_objects(subject, root, code):

    # setup the databases
storage = FileStorage("data/db.fs")
db = DB(storage)
connection = db.open()
root = connection.root()


def listEmployees():
    if len(employees.values()) == 0:
        print("\nThere are no employees.")
        return
    for employee in employees.values():
        print(f"\nEmployee's name: {employee.name}")
        if employee.manager:
            print(f" Manager's name: {employee.manager.name}")


def addEmployee(name, manager_name=None):
    if name in employees:
        print("\nThere is already an employee with this name.")
        return
    if manager_name:
        try:
            manager = employees[manager_name]
        except KeyError:
            print("\nNo such manager.")
            return
        employees[name] = Employee(name, manager)
    else:
        employees[name] = Employee(name)

    root['employees'] = employees  # reassign to change
    transaction.commit()
    print(f"\nEmployee {name} added.")


if __name__ == "__main__":
    code = 'users'
    pkey_admin = 'admin'
    pkey_pwd = make_uid(f'admin_password_cosmer_user_{time.time()}')
    pkey_group = make_uid(f'group_name_finance_group_{time.time()}')
    bodys = {
        'admin': {
            'key': 'user_id',
            'value': 'admin',
            'type': 'user',
            'timestamp': ''
        },
        pkey_pwd: {
            'key': 'password',
            'value': 'admin',
            'type': 'user',
            'timestamp': ''
        },
        pkey_group: {
            'key': 'group_name',
            'value': 'finance',
            'type': 'group',
            'timestamp': '',
        },
    }
    add_records(root, code, bodys)

    code = 'groups'
    bodys = {
        f"{pkey_admin}_{pkey_pwd}_{time.time()}": {
            'type': 'auth',
            'value': 'user_password',
            'subject_id': pkey_admin,
            'object_id': pkey_pwd,
            'count': 1,
        },
        f"{pkey_admin}_{pkey_group}_{time.time()}": {
            'type': 'org',
            'value': 'dept',
            'subject_id': pkey_admin,
            'object_id': pkey_group,
            'count': 1,
        },
    }
    add_records(root, code, bodys)

    transaction.commit()

    print([[r[k].body for k in r] for r in [root[e] for e in root]])
    print(root)

    connection.close()
