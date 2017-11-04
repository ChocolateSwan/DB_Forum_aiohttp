# -*- coding: utf-8 -*-

import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

# MONGODB_HOST = "192.168.1.2"
# MONGODB_PORT = 27017

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/te", RootHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)

        # MongoDB
        # self.connection = pymongo.Connection(MONGODB_HOST, MONGODB_PORT)
        # self.db = self.connection["mallertv"]


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return "hello"
        # return self.application.db


class RootHandler(BaseHandler):
    def get(self):
        # result = list(self.db.contents.find({}, limit=1))[0]["_id"]
        # self.write(str(result))
        self.write("Hello, world")


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()