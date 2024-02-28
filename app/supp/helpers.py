
import time, sys
from pprint import pprint
from supp.config import todo


# ---
# (1) feedback for string commands
#

def str_1_fb(r):
    return r.mget(['joke:42'])

def str_2_fb(r):
    return r.mget(['joke:42','joke:44','joke:45'])

def str_5_fb(r):
    return r.mget(['joke:42','joke:42:votes'])

def str_6_fb(r):
    return r.mget(['joke:44','joke:44:votes'])

def str_7_fb(r):
    fb = []
    fb.append({'ttl 0': r.ttl('joke:45')})
    time.sleep(1)
    fb.append({'ttl 1': r.ttl('joke:45')})
    time.sleep(1)
    fb.append({'ttl 2': r.ttl('joke:45')})
    return fb


# ---
# (2) feedback for hash commands
#

def hash_1_fb(r):
    jokes = []
    for key in r.keys('joke:*'): jokes.append(r.hgetall(key))
    return jokes
 
hash_2_fb = hash_1_fb
hash_3_fb = hash_1_fb

def hash_8_fb(r):
    return r.hgetall('joke:50')

hash_9_fb  = hash_8_fb
hash_10_fb = hash_8_fb
hash_11_fb = hash_1_fb


# ---
# (3) feedback for list commands
#

def list_1_fb(r):
    return r.lrange('task:backlog', 0, -1)

list_5_fb = list_1_fb
list_6_fb = list_1_fb
list_7_fb = list_1_fb
list_8_fb = list_1_fb
list_9_fb = list_1_fb


# ---
# (4) feedback for set commands
#

def set_1_fb(r):
    return {
        'staff':   r.smembers('group:staff'),
        'student': r.smembers('group:student'),
        'admin':   r.smembers('group:admin'),
    }

set_2_fb  = set_1_fb
set_3_fb  = set_1_fb
set_9_fb  = set_1_fb
set_10_fb = set_1_fb


# ---
# (5) feedback for sorted set commands
#

def zet_1_fb(r):
    return r.zrevrange('league:table', 0, -1, withscores=True)

zet_8_fb = zet_1_fb


#


_BLUE = '\033[94m'
_BOLD = '\033[1m'
_RESET = '\033[0m'


def _bold_print(text):
    '''
    prints text in uppercase bold
    '''
    print(f'\n{_BOLD}{text.upper()}{_RESET}')


def fbprint(stuff):
    '''
    prints feedback in blue text
    '''
    print(f'{_BLUE}', end='')
    pprint(stuff)
    print(f'{_RESET}', end='')


def reset(r):
    '''
    removes all keys from db
    '''
    all_keys = r.keys('*')
    return(r.delete(*all_keys) if len(all_keys) else 0)


def run_all(r, command):
    '''
    executes all commands
    '''
    helpers = sys.modules[__name__]
    reset(r)

    param = 1

    while True:

        func_name = f'{command}_{param}'
        fb_name = f'{func_name}_fb'

        if not hasattr(todo['queries'], func_name): break

        function = getattr(todo['queries'], func_name)
        feedback = getattr(helpers, fb_name) \
            if hasattr(helpers, fb_name) else None

        _bold_print(f'{command} ({param})')
        pprint(function(r))
        if feedback: fbprint(feedback(r))

        param += 1

    print()
