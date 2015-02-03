import json
import redis
import sys
import time


def create_retriever(config, logger):
    MDRClass = getattr(sys.modules[__name__], config['mdr_class'])
    return MDRClass(config, logger)


class MonitorDataRetriever(object):

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def retrieve(self):
        raise NotImplementedError


class RedisMDR(MonitorDataRetriever):

    def __init__(self, config, logger):
        super(RedisMDR, self).__init__(config, logger)

        try:
            self.r_server = redis.Redis(
                host=config['redis_host'], port=config['redis_port'],
                db=config['redis_db'], password=config['redis_password'])
        except:
            logger.error("Cannot connect to redis, shutting down")
            sys.exit(1)

    def retrieve(self):
        # Get list of members to check from queue
        for check in self.r_server.smembers(self.config['queue']):
            checkdata = {'cid': check, 'data': {}}
            # Non-Data Keys
            monkey = "monitor:" + check
            for key in self.r_server.hkeys(monkey):
                value = self.r_server.hget(monkey, key)
                if value == "slist":
                    checkdata[key] = []
                    listkey = monkey + ":" + key
                    for entry in self.r_server.smembers(listkey):
                        checkdata[key].append(entry)
                else:
                    checkdata[key] = value
            # Data Keys
            monkey = "monitor:" + check + ":data"
            for key in self.r_server.hkeys(monkey):
                value = self.r_server.hget(monkey, key)
                if value == "slist":
                    checkdata['data'][key] = []
                    listkey = monkey + ":" + key
                    for entry in self.r_server.smembers(listkey):
                        checkdata['data'][key].append(entry)
                else:
                    checkdata['data'][key] = value
            checkdata['time_tracking'] = {'control': time.time(),
                                        'ez_key': self.config['stathat_key'],
                                        'env': str(self.config['envname'])}
            checkdata['zone'] = self.config['zone']
            jdata = json.dumps(checkdata)
            yield jdata
