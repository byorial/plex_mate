# -*- coding: utf-8 -*-
#########################################################
# python
import json
import os
import platform
import re
import shutil
import sys
import threading
import time
import traceback
from datetime import datetime

# third-party
import requests
import xmltodict
from flask import jsonify, redirect, render_template, request
# sjva 공용
from framework import (SystemModelSetting, Util, app, celery, db, path_data,
                       scheduler, socketio)
from plugin import LogicSubModuleBase, default_route_socketio_sub
from tool_base import ToolBaseFile, ToolSubprocess, d

# 패키지
from .plugin import P

logger = P.logger
package_name = P.package_name
ModelSetting = P.ModelSetting


from .logic_pm_base import LogicPMBase
from .plex_db import PlexDBHandle
from .plex_web import PlexWebHandle
from .task_pm_dbcopy_copy import Task

#########################################################


class LogicPMDbCopyStatus(LogicSubModuleBase):
    
    def __init__(self, P, parent, name):
        super(LogicPMDbCopyStatus, self).__init__(P, parent, name)
        self.db_default = {
            f'{self.parent.name}_{self.name}_db_version' : '1',
            f'{self.parent.name}_{self.name}_task_stop_flag' : 'False',
        }
        self.data = {
            'list' : [],
            'status' : {'is_working':'wait'}
        }
        self.list_max = 300
        default_route_socketio_sub(P, parent, self)


    def process_ajax(self, sub, req):
        try:
            ret = {}
            if sub == 'command':
                command = req.form['command']
                if command == 'start':
                    if ModelSetting.get(f'{self.parent.name}_{self.name}_path_source_db') == '' or ModelSetting.get(f'{self.parent.name}_{self.name}_path_source_section_id') == '' or ModelSetting.get(f'{self.parent.name}_{self.name}_path_source_root_path') == '' or ModelSetting.get(f'{self.parent.name}_{self.name}_path_target_root_path'):
                        ret = {'ret':'warning', 'msg':'설정을 저장 후 시작하세요.'}
                    else:
                        if self.data['status']['is_working'] == 'run':
                            ret = {'ret':'warning', 'msg':'실행중입니다.'}
                        else:
                            self.task_interface(command)
                            ret = {'ret':'success', 'msg':'작업을 시작합니다.'}
                elif command == 'stop':
                    if self.data['status']['is_working'] == 'run':
                        ModelSetting.set(f'{self.parent.name}_{self.name}_task_stop_flag', 'True')
                        ret = {'ret':'success', 'msg':'잠시 후 중지됩니다.'}
                    else:
                        ret = {'ret':'warning', 'msg':'대기중입니다.'}
                elif command == 'refresh':
                    self.refresh_data()
            return jsonify(ret)
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            return jsonify({'ret':'danger', 'msg':str(e)})
    
    #########################################################

    def task_interface(self, *args):
        def func():
            time.sleep(1)
            self.task_interface2(*args)
        th = threading.Thread(target=func, args=())
        th.setDaemon(True)
        th.start()


    def task_interface2(self, *args):
        self.data['list'] = []
        self.data['status']['is_working'] = 'run'
        self.refresh_data()
        ModelSetting.set(f'{self.parent.name}_{self.name}_task_stop_flag', 'False')
        try:
            if app.config['config']['use_celery']:
                result = Task.start.apply_async()
                ret = result.get(on_message=self.receive_from_task, propagate=True)
            else:
                ret = Task.start(self)
            self.data['status']['is_working'] = ret
        except Exception as e: 
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
            self.data['status']['is_working'] = 'wait'
        self.refresh_data()


    def refresh_data(self, index=-1):
        #logger.error(f"refresh_data : {index}")
        if index == -1:
            self.socketio_callback('refresh_all', self.data)
            
        else:
            self.socketio_callback('refresh_one', {'one' : self.data['list'][index], 'status' : self.data['status']})
        

    def receive_from_task(self, arg, celery=True):
        try:
            result = None
            if celery:
                if arg['status'] == 'PROGRESS':
                    result = arg['result']
            else:
                result = arg
            if result is not None:
                self.data['status'] = result['status']
                #logger.warning(result)
                del result['status']
                #logger.warning(result)
                if self.list_max != 0:
                    if len(self.data['list']) == self.list_max:
                        self.data['list'] = []
                result['index'] = len(self.data['list'])
                self.data['list'].append(result)
                self.refresh_data(index=result['index'])
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())