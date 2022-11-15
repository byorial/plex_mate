# -*- coding: utf-8 -*-
#########################################################
# python
import os, sys, traceback, re, json, threading, time, shutil, platform
from datetime import datetime
# third-party
import requests, xmltodict
from flask import request, render_template, jsonify, redirect
# sjva 공용
from framework import db, scheduler, path_data, socketio, SystemModelSetting, app, celery, Util
from plugin import LogicModuleBase, default_route_socketio
from tool_base import ToolBaseFile, d, ToolSubprocess
# 패키지
from .plugin import P
logger = P.logger
package_name = P.package_name
ModelSetting = P.ModelSetting
name = 'tool'

from .task_pm_base import Task
from .plex_db import PlexDBHandle
from .plex_web import PlexWebHandle
from .logic_pm_tool_simple import LogicPMDBToolSimple
from .logic_pm_tool_select import LogicPMDBToolSelect
from .logic_pm_tool_query import LogicPMDBToolQuery
#########################################################

class LogicPMTool(LogicModuleBase):
    db_default = None

    def __init__(self, P):
        super(LogicPMTool, self).__init__(P, 'select')
        self.name = name
        self.sub_list = {
            'simple' : LogicPMDBToolSimple(P, self, 'simple'),
            'select' : LogicPMDBToolSelect(P, self, 'select'),
            'query' : LogicPMDBToolQuery(P, self, 'query'),
        }

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        arg['sub'] = self.name
        arg['sub2'] = sub 
        try:
            #if sub == 'simple':
            arg['library_list'] = PlexDBHandle.library_sections()
            if sub == 'select':
                arg['library_list'].insert(0, {'id':0, 'name':'전체'})
                #arg['preset'] = LogicPMDBToolSelect.preset
            #logger.error(d(arg))
            return render_template(f'{package_name}_{name}_{sub}.html', arg=arg)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return render_template('sample.html', title=f"{package_name}/{name}/{sub}")

    def process_ajax(self, sub, req):
        try:
            ret = {}
            return jsonify(ret)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return jsonify({'ret':'danger', 'msg':str(e)})
    #########################################################

