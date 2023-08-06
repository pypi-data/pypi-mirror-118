#!/usr/bin/env python3
# coding: utf-8

import flask

from joker.flasky import viewutils


def decorate_all_view_funcs(app, decorator):
    keys = list(app.view_functions)
    for key in keys:
        func = app.view_functions[key]
        app.view_functions[key] = decorator(func)


class FlaskPlus(flask.Flask):
    json_encoder = viewutils.JSONEncoderPlus
    decorate_all_view_funcs = decorate_all_view_funcs
    serialize_current_session = viewutils.serialize_current_session


__all__ = ['FlaskPlus', 'decorate_all_view_funcs']
