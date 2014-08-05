#coding:utf-8
import os
import sys
import constant 
if __name__ == '__main__':
    sys.path.insert(0, constant.PROJECT_DIR)
import logging
import tornado.web
import tornado.options
import tornado.httpserver
from tornado.ioloop import IOLoop
from timer.log import LocalLog
os.environ['DJANGO_SETTINGS_MODULE'] = 'constant'

logger = logging.getLogger('Robot')
logger.propagate = False
logger.setLevel(logging.INFO)
not os.access(constant.LOCAL_LOG_DIR, os.F_OK) and os.makedirs(constant.LOCAL_LOG_DIR)
local_log_hdl = logging.StreamHandler(stream=LocalLog)
log_format = logging.Formatter(
        '%(asctime)s %(name)s [%(levelname)s] [%(process)d] [%(filename)s:%(lineno)s] %(message)s',
        '%Y-%m-%dT%H:%M:%S')
local_log_hdl.setFormatter(log_format)
logger.addHandler(local_log_hdl)
tornado.options.define("port", default=8888, help=u"指定启动端口", type=int)

from django.conf import settings

from handler.novel import NovelHandler


urls = [
    (r'/novel', NovelHandler),
]

class Application(tornado.web.Application):
    'application'
    
    def __init__(self):
        
        settings = dict(
            static_path = os.path.join(constant.PROJECT_DIR, "static"),
            template_path = os.path.join(constant.PROJECT_DIR, "template"),
            constant=constant,
            debug=constant.DEBUG,
            cookie_secret=constant.COOKIE_SECRET,
        )
        self.visit_logger = logging.getLogger('Robot.Visit')
        for url in (r'/favicon.ico', r'/robots.txt'):
            urls.append((url, tornado.web.StaticFileHandler, dict(path=settings['static_path'])))
        tornado.web.Application.__init__(self, urls, **settings)
        
    def log_request(self, handler):
        '记录日志'
        
        status = handler.get_status()
        if status < 400:
            log_method = self.visit_logger.info
        elif status < 500:
            log_method = self.visit_logger.warning
        else:
            log_method = self.visit_logger.error
        request_time = 1000.0 * handler.request.request_time()

        request = handler.request
        headers = request.headers

        arguments = request.arguments
        msg = '|'.join(['%s' % getattr(handler, 'uuid', ''),
                        '%s' % getattr(handler, 'guid', ''),
                        '%s' % (handler.current_user.userid if handler.current_user else None),
                        '%s' % str(handler.get_status()),
                        '%.2f' % request_time,
                        handler.request.remote_ip,
                        headers.get('Host', ''),
                        headers.get('Content-Length', ''),
                        request.method,
                        request.full_url() if not self._is_secret_request(handler) else request.path,
                        str(arguments) if not self._is_secret_request(handler) else 'secret-arguments',
                       ])

        if status < 500:
            log_method(msg)
        else:
            log_method(msg, exc_info=True)

    def _is_secret_request(self, handler):
        
        return False

if __name__ == '__main__':

    tornado.options.parse_command_line()
    options = tornado.options.options

    if constant.DEBUG:
        # CONSOLE日志
        stream_hd = logging.StreamHandler()
        stream_hd.setFormatter(log_format)
        logger.addHandler(stream_hd)
        logger.setLevel(logging.DEBUG)
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)

    # 定时保存本地日志
    LocalLog(1000 * constant.LOCAL_LOG_FLUSH_INTERVAL,
            constant.LOCAL_LOG_DIR, options.port).start()
    logger.info('Server Starting at port %s...' %options.port)
    tornado.ioloop.IOLoop.instance().set_blocking_log_threshold(10)
    tornado.ioloop.IOLoop.instance().start()
    
