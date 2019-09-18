from pymongo import MongoClient
import configparser

class Mongo():

    def __init__(self, config_file):
        config = configparser.RawConfigParser()
        config.read(config_file)

        self.server = config.get('mongo', 'server') if 'server' in [i[0] for i in config.items('mongo')] else False
        self.db = config.get('mongo', 'db') if 'db' in [i[0] for i in config.items('mongo')] else False
        self.host = config.get('mongo', 'host') if 'host' in [i[0] for i in config.items('mongo')] else False
        self.port = int(config.get('mongo', 'port')) if 'port' in [i[0] for i in config.items('mongo')] else False
        self.user = config.get('mongo', 'user') if 'user' in [i[0] for i in config.items('mongo')] else False
        self.password = config.get('mongo', 'password') if 'password' in [i[0] for i in config.items('mongo')] else False

    def connect(self):
        if self.server == 'True':
            connection_string_basic = "mongodb+srv://{user}:{password}@{host}{port}{db}".format(user=self.user,
                                                                                                   password=self.password,
                                                                                                   host=self.host,
                                                                                                   port="{port}",
                                                                                                   db="{db}")
        else:
            connection_string_basic = "mongodb://{user}:{password}@{host}{port}{db}".format(user=self.user,
                                                                                            password=self.password,
                                                                                            host=self.host,
                                                                                            port="{port}",
                                                                                            db="{db}")

        if self.port:
            connection_string_port = connection_string_basic.format(port=":{}".format(self.port),
                                                                    db="{db}")
        else:
            connection_string_port = connection_string_basic.format(port="",
                                                                    db="{db}")

        if self.db:
            connection_string = connection_string_port.format(db="/{}".format(self.db))
        else:
            connection_string = connection_string_port.format(db="")

        return MongoClient(connection_string)
