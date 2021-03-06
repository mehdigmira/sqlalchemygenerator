# -*- coing: utf-8 -*-
from __future__ import unicode_literals, division

from collections import defaultdict

import argparse


def text_parser(s):
    """

    :param s: list of strings like a->b->c
    :return: A dict that holds information about tables and foreign keys
    """
    result = defaultdict(list)
    for sub_s in s:
        tables = sub_s.split("->")
        for i, table in enumerate(tables):
            try:
                result[table].append(tables[i+1])
            except IndexError:
                pass
    return result


def code_builder(infos):
    """
    builds SA code from dict generated by text_parser
    """
    code = """
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload, contains_eager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite://', echo=True)
    """
    for table_name, foreign_keys in infos.items():
        code += """
class %s(Base):
    __tablename__ = '%s'
    id = Column(Integer, primary_key=True)
    name = Column(String)
""" % (to_camel_case(table_name), table_name)
        for fk in foreign_keys:
            code += """
    %s_id = Column(Integer, ForeignKey('%s.id'))
    %s = relationship('%s', backref='%ss')
            """ % (fk, fk, fk, to_camel_case(fk), table_name)
        code += """

        """
    code += """
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()
"""
    return code


def to_camel_case(s):
    return s.title().replace('_', '')


def main(s):
    return code_builder(text_parser(s))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='build SA code from string')
    parser.add_argument('list_strings', metavar='list_strings', type=str, nargs='+',
                        help='list of strings to build SA code upon')
    args = parser.parse_args()
    print main(args.list_strings)
