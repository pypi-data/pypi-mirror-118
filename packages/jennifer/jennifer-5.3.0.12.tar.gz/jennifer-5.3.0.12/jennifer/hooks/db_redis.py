from jennifer.agent import jennifer_agent
import json
__hooking_module__ = 'redis'


def format_command(*args):
    cmd = args[0]
    parameters = [cmd]
    for arg in args[1:]:
        p = json.dumps(arg)
        parameters.append(p)

    return ' [REDIS] ' + ' '.join(parameters)

def wrap_execute_command(origin):
    agent = jennifer_agent()
    def handler(self, *args, **kwargs):
        transaction = agent.current_transaction()
        if transaction is not None:
            try:
                message = format_command(*args)
                transaction.profiler.message(message)
            except:
                pass
        ret = origin(self, *args, **kwargs)
        return ret
    return handler


def hook(redis):
    redis.Redis.execute_command = wrap_execute_command(
        redis.Redis.execute_command)
