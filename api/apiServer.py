# coding:utf-8
'''
定义几个关键字，count type,protocol,country,area,
'''
import json
import sys
import web
import config
from db.DataStore import sqlhelper
from db.SqlHelper import Proxy

urls = (
    '/', 'select',
    '/delete', 'delete'
    '/validate', 'validate'
)

sleep_condition = None

def start_api_server(condition):
    global sleep_condition
    sleep_condition = condition
    sys.argv.append('0.0.0.0:%s' % config.API_PORT)
    app = web.application(urls, globals())
    app.run()


class select(object):
    def GET(self):
        inputs = web.input()
        json_result = json.dumps(sqlhelper.select(inputs.get('count', None), inputs))
        return json_result


class delete(object):
    params = {}

    def GET(self):
        inputs = web.input()
        json_result = json.dumps(sqlhelper.delete(inputs))
        return json_result


class validate(object):
    def GET(self):
        global sleep_condition
        sleep_condition.acquire()
        sleep_condition.notify()
        sleep_condition.release()


if __name__ == '__main__':
    sys.argv.append('0.0.0.0:8000')
    app = web.application(urls, globals())
    app.run()
