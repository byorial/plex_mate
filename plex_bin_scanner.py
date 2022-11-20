import platform
import subprocess

from support import SupportSubprocess, d

from .setup import *


class PlexBinaryScanner(object):

    #su - plex -c "/usr/lib/plexmediaserver/Plex\ Media\ Scanner --section 8 --analyze --item 332875"

    @classmethod
    def scan_refresh_old(cls, section_id, folderpath, timeout=None, db_item=None, scan_item=None):
        def demote(user_uid, user_gid):
            def result():
                os.setgid(user_gid)
                os.setuid(user_uid)
            return result
        shell = False
        env = dict(PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR=f"{os.path.dirname(os.path.dirname(P.ModelSetting.get('base_path_metadata')))}", **os.environ)
        force_log = False
        try:
            if platform.system() == 'Windows':
                if folderpath is None or folderpath == '':
                    command = f'"{P.ModelSetting.get("base_bin_scanner")}" --scan  --refresh --section {section_id}"'
                else:
                    command = f'"{P.ModelSetting.get("base_bin_scanner")}" --scan  --refresh --section {section_id} --directory "{folderpath}"'
                logger.warning(command)
                tmp = []
                if type(command) == type([]):
                    for x in command:
                        if x.find(' ') == -1:
                            tmp.append(x)
                        else:
                            tmp.append(f'"{x}"')
                    command = ' '.join(tmp)
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, encoding='utf8')
            else:
                if folderpath is None or folderpath == '':
                    command = [P.ModelSetting.get("base_bin_scanner"), '--scan', '--refresh', '--section', str(section_id)]
                else:
                    command = [P.ModelSetting.get("base_bin_scanner"), '--scan', '--refresh', '--section', str(section_id), '--directory', folderpath]
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, preexec_fn=demote(P.ModelSetting.get_int('base_bin_scanner_uid'), P.ModelSetting.get_int('base_bin_scanner_gid')), encoding='utf8')
                

            if db_item is not None:
                db_item.process_pid = process.pid
                db_item.start_time = datetime.now()
                db_item.status = "working"
                db_item.save()
            if scan_item is not None:
                scan_item.scan_process_pid = process.pid
                scan_item.save()


            new_ret = {'status':'finish', 'log':None}
            logger.debug(f"PLEX SCANNER COMMAND\n{' '.join(command)}")
            try:
                process_ret = process.wait(timeout=timeout)
                logger.debug(f"process_ret : {process_ret}")

                if db_item is not None:
                    if process_ret == 0:
                        db_item.status = 'finished'
            except:
                import psutil
                process = psutil.Process(process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
                if db_item is not None:
                    db_item.status = 'timeout'
                if scan_item is not None:
                    scan_item.status = 'finish_timeout'

        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())
            logger.error('command : %s', command)
        finally:
            if scan_item is not None:
                scan_item.save()



    @classmethod
    def analyze(cls, section_id, folderpath=None, metadata_item_id=None, timeout=None, db_item=None):
        def demote(user_uid, user_gid):
            def result():
                os.setgid(user_gid)
                os.setuid(user_uid)
            return result
        shell = False
        env = dict(PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR=f"{os.path.dirname(os.path.dirname(ModelSetting.get('base_path_metadata')))}", **os.environ)
        force_log = False
        try:
            if platform.system() == 'Windows':
                if folderpath is not None and folderpath != '':
                    command = f'"{ModelSetting.get("base_bin_scanner")}" --analyze --section {section_id} --directory "{folderpath}"'
                elif metadata_item_id is not None and metadata_item_id != '':
                    command = f'"{ModelSetting.get("base_bin_scanner")}" --analyze --section {section_id} --item {metadata_item_id}'
                else:
                    cmd = f'"{ModelSetting.get("base_bin_scanner")}" --analyze --section {section_id}'
                tmp = []
                if type(command) == type([]):
                    for x in command:
                        if x.find(' ') == -1:
                            tmp.append(x)
                        else:
                            tmp.append(f'"{x}"')
                    command = ' '.join(tmp)
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, encoding='utf8')
            else:
                if folderpath is not None and folderpath != '':
                    command = [ModelSetting.get("base_bin_scanner"), '--analyze', '--section', str(section_id), '--directory', folderpath]
                elif metadata_item_id is not None and metadata_item_id != '':
                    command = [ModelSetting.get("base_bin_scanner"), '--analyze', '--section', str(section_id), '--item', metadata_item_id]
                else:
                    command = [ModelSetting.get("base_bin_scanner"), '--analyze', '--section', str(section_id)]
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, preexec_fn=demote(ModelSetting.get_int('base_bin_scanner_uid'), ModelSetting.get_int('base_bin_scanner_gid')), encoding='utf8')

            if db_item is not None:
                db_item.process_pid = process.pid
                db_item.start_time = datetime.now()
                db_item.status = "working"
                db_item.save()

            new_ret = {'status':'finish', 'log':None}
            logger.debug(f"PLEX SCANNER ANALYZE COMMAND\n{' '.join(command)}")
            try:
                process_ret = process.wait(timeout=timeout) # wait for the subprocess to exit
                logger.debug(f'process_ret : {process_ret}')
                if db_item is not None:
                    if process_ret == 0:
                        db_item.status = 'finished'
            except:
                import psutil
                process = psutil.Process(process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
                if db_item is not None:
                    db_item.status = 'timeout'
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())
            logger.error('command : %s', command)



    @classmethod
    def meta_refresh_by_id(cls, item_id, timeout=None):
        def demote(user_uid, user_gid):
            def result():
                os.setgid(user_gid)
                os.setuid(user_uid)
            return result
        shell = False
        env = dict(PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR=f"{os.path.dirname(os.path.dirname(ModelSetting.get('base_path_metadata')))}", **os.environ)
        force_log = False
        try:
            if platform.system() == 'Windows':
                command = f'"{ModelSetting.get("base_bin_scanner")}" --force --refresh --item {item_id}"'
                tmp = []
                if type(command) == type([]):
                    for x in command:
                        if x.find(' ') == -1:
                            tmp.append(x)
                        else:
                            tmp.append(f'"{x}"')
                    command = ' '.join(tmp)
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, encoding='utf8')
            else:
                command = [ModelSetting.get("base_bin_scanner"), '--force', '--refresh', '--item', str(item_id)]
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=shell, env=env, preexec_fn=demote(ModelSetting.get_int('base_bin_scanner_uid'), ModelSetting.get_int('base_bin_scanner_gid')), encoding='utf8')

            new_ret = {'status':'finish', 'log':None}
            logger.debug(f"PLEX SCANNER COMMAND\n{' '.join(command)}")
            try:
                process_ret = process.wait(timeout=timeout)
                logger.debug(f"process_ret : {process_ret}")
            except:
                import psutil
                process = psutil.Process(process.pid)
                for proc in process.children(recursive=True):
                    proc.kill()
                process.kill()
        except Exception as e: 
            logger.error(f"Exception:{str(e)}")
            logger.error(traceback.format_exc())
            logger.error('command : %s', command)
        finally:
            pass
    


    @classmethod
    def scan_refresh(cls, section_id, folderpath, call_id=None, timeout=None, callback_function=None, callback_id=None, join=False):
        env = os.environ.copy()
        env['PLEX_MEDIA_SERVER_APPLICATION_SUPPORT_DIR'] = os.path.dirname(os.path.dirname(P.ModelSetting.get('base_path_metadata')))
        
        if folderpath is None or folderpath == '':
            command = [P.ModelSetting.get("base_bin_scanner"), '--scan', '--refresh', '--section', str(section_id)]
        else:
            command = [P.ModelSetting.get("base_bin_scanner"), '--scan', '--refresh', '--section', str(section_id), '--directory', folderpath]
        process = SupportSubprocess(command, timeout=timeout,  stdout_callback=callback_function, env=env, uid=P.ModelSetting.get_int('base_bin_scanner_uid'), gid=P.ModelSetting.get_int('base_bin_scanner_gid'), call_id=call_id)
        process.start(join=join)
        return process
        
           