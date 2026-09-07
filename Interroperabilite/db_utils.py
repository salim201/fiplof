# coding: utf-8
from Utils import create_connection


def connection_is_broken(connection):
    return connection is None or connection.closed


def reconnect_connection():
    return create_connection()
