#!/usr/bin/pythob3
import datetime
import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import peewee
import uuid

from tornado.options import define, options

from src.db import create_tables, database, LoginRecord, Message, User
create_tables()

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/chatsocket", ChatSocketHandler),
                    (r"/login", LoginHandler),
                    (r"/register", RegisterHandler),
                    (r"/preflight", UserPreflightHandler)]
        settings = dict(
            cookie_secret="2wdgQU9UQn+6KBnUocm75KHpqxMSHElBj+BINI7k7zY=",
            # template_path=os.path.join(os.path.dirname(__file__), "../src/html"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # xsrf_cookies=True, # TODO
            debug=True
        )
        super().__init__(handlers, **settings)


class BaseRequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):

        origin = self.request.headers.get('Origin')
        if origin:
            self.set_header("Access-Control-Allow-Origin", origin)
            self.set_header("Access-Control-Allow-Credentials", "true")
        else:
            self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def options(self):
        self.set_status(204)

    def prepare(self):
        if not database.is_closed():
            database.close()
            database.connect()
        return super().prepare()

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super().on_finish()


class RegisterHandler(BaseRequestHandler):

    def post(self):
        '''
        request body will be
        {
            "username": "xxx",
            "password": "xxx",
            "email": "xxx",
        }
        '''
        data = tornado.escape.json_decode(self.request.body)
        data['join_date'] = datetime.datetime.now()
        try:
            User.create(**data)
            result = True
        except peewee.IntegrityError:
            result = False
        # save to database, return True if successfull otherwise False
        self.write(dict(result=result))


class LoginHandler(BaseRequestHandler):

    def post(self):
        '''
        {
            id: "username or email",
            password: "password"
        }
        '''
        # return True if successfull otherwise False
        data = tornado.escape.json_decode(self.request.body)
        identifier = data.get('id')
        password = data.get('password')
        login = True
        try:
            user = User.get(((User.username == identifier) &
                             (User.password == password)) |
                            ((User.email == identifier) &
                             (User.password == password)))
            now = datetime.datetime.now()
            credential = str(uuid.uuid4())
            try:
                lc = LoginRecord.get(
                    ((LoginRecord.username == user.username) &
                     (LoginRecord.valid == True)))
                lc.valid = False
                lc.save()
            except peewee.DoesNotExist:
                pass
            finally:
                LoginRecord.create(
                    username=user.username,
                    login_date=now,
                    credential=credential)
                self.set_cookie('uid', credential)
        except peewee.DoesNotExist:
            login = False
        if login:
            self.write(dict(result=login, username=user.username))
        else:
            self.write(dict(result=login))


class UserPreflightHandler(BaseRequestHandler):

    def post(self):
        '''
        {
            type: "", # two types: "username" and "email"
            value: "" # the value of username or email
        }
        '''
        # if exists then return True and False otherwise
        data = tornado.escape.json_decode(self.request.body)
        field = data.get('type')
        value = data.get('value')
        if field == 'username':
            try:
                User.get(User.username == value)
                result = False
            except peewee.DoesNotExist:
                result = True
        elif field == 'email':
            try:
                User.get(User.email == value)
                result = False
            except peewee.DoesNotExist:
                result = True
        else:
            result = True
        self.write(dict(result=result))


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache_size = 200

    def prepare(self):
        if not database.is_closed():
            database.close()
        database.connect()
        return super().prepare()

    def on_finish(self):
        if not database.is_closed():
            database.close()
        return super().on_finish()

    def close(self):
        if not database.is_closed():
            database.close()
        try:
            ChatSocketHandler.waiters.remove(self)
        except KeyError:
            pass
        super().close()

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        return {}

    def open(self):
        credential = self.get_cookie('uid')
        if not credential:
            self.close()
        else:
            try:
                lc = LoginRecord.get((LoginRecord.credential == credential) &
                                     (LoginRecord.valid == True))
                self.credential = credential
                self.username = lc.username
                self.__class__.waiters.add(self)

                query = (
                    Message
                    .select(Message.username, Message.message, Message.date)
                    .limit(200)
                    .dicts()
                    .iterator()
                )
                cached = [
                    {
                        "username": row.get('username'),
                        "message": row.get('message'),
                        "date": str(row.get('date'))
                    }
                    for row in query
                ]
                self.write_message(dict(cached=cached))
            except peewee.DoesNotExist:
                self.close()

    def on_close(self):
        try:
            ChatSocketHandler.waiters.remove(self)
        except KeyError:
            pass
        if not database.is_closed():
            database.close()

    @classmethod
    def update_cache(cls, chat):
        Message.create(
            username=chat.get('username'),
            message=chat.get('message'),
            date=chat.get('date'))

    @classmethod
    def send_updates(cls, chat):
        logging.info("sending_message to %d waiters", len(cls.waiters))
        for waiters in cls.waiters:
            try:
                waiters.write_message(chat)
            except:
                logging.error('Error sending message', exc_info=True)

    def on_message(self, message):
        logging.info('got message %r', message)
        parsed = tornado.escape.json_decode(message)
        now = datetime.datetime.now()
        username = self.username
        try:
            LoginRecord.get(((LoginRecord.credential == self.credential)
                             & LoginRecord.valid == True))
        except peewee.DoesNotExist:
            self.close()
        else:
            chat = {
                "username": username,
                "message": parsed["body"],
                "date": now.strftime("%y/%m/%d %H:%M:%S")
            }
            self.__class__.update_cache({
                'username': username,
                'message': parsed["body"],
                'date': now
            })
            self.__class__.send_updates(chat)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
