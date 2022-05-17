import logging

from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer

import jenkins
import json
import time
import requests


logger = logging.getLogger(__name__)


def debug_func(func):
    def wapper(*args, **kwargs):
        logger.error(func.__name__)
        return func(*args, **kwargs)
    return wapper


class ChatConsumer(JsonWebsocketConsumer):
    disconnected = False

    def connect(self):
        user = self.scope["user"]
        if user:
            self.accept()
        else:
            self.close()

    @debug_func
    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        logger.error(data)
        sapi = JenkinsAPI()
        # output = sapi.server.get_build_console_output('kkb-zeus-websocket-output-runner', 10)
        output_offset = 0
        output_finish_mark = 0

        while not self.disconnected:
            output = sapi.server.get_build_console_output('kkb-zeus-websocket-output-runner', 10)
            if output and output_finish_mark == 0:
                self.send(output[output_offset:])
                output_offset = len(output)
                if output.find('Finished: ') != -1:
                    logger.error('exec find')
                    logger.error(output.find('Finished: '))
                    output_finish_mark = 1
            elif output_finish_mark:
                print('output finish')
                self.close()
                break
            time.sleep(3)

    def disconnect(self, code):
        self.disconnected = True
        self.close()


class JenkinsAPI:
    def __init__(self) -> None:
        self.server = jenkins.Jenkins('http://192.168.100.170:18080', 'admin', 'admin')

    def progressive_html(self, job_name, build_id):
        url = '{}job/{}/{}/logText/progressiveHtml'.format(self.server.server, job_name, build_id)
        headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
        ret = self.server.jenkins_open(requests.Request('POST', url, data=form_data, headers=headers))
        return ret
