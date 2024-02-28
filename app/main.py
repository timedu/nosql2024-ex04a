
import traceback
try: import readline
except: pass 

from os import environ
from pprint import pprint
from dotenv import load_dotenv # pyright: ignore
import importlib
import redis # pyright: ignore

from supp.config import set_config, todo
from supp import helpers

def repl():

    r = redis.Redis(
        host=environ.get('REDIS_HOST', 'redis'),
        port=environ.get('REDIS_PORT', 6379),
        password=environ.get('REDIS_PASSWORD', None),
        decode_responses=True
    )

    while True:

        try:
            user_input = input(todo['prompt'])
        except EOFError:
            print('')
            break        

        if not user_input.strip(): continue
        
        input_strings = user_input.lower().split()
        command = input_strings[0]

        try:

            if len(input_strings) == 1:

                if command in ('exit', 'quit'):
                    break

                if command == 'reset':
                    pprint(helpers.reset(r))
                    continue

                raise AssertionError    

            if len(input_strings) == 2:

                assert command in ['str','hash','list','set','zet']                
                importlib.reload(todo['queries'])
                param = input_strings[1]

                if param == 'all': 
                    helpers.run_all(r, command)
                    continue
            
                '''
                for example:
                - user input: 'str 1'
                - command: 'str', param: '1'
                - [todo] function: str_1
                - feedback [function]: str_1_fb   
                '''

                func_name = f'{command}_{param}'
                fb_name = f'{func_name}_fb'

                function = getattr(todo['queries'],func_name)
                feedback = getattr(helpers, fb_name) \
                           if hasattr(helpers, fb_name) else None

                pprint(function(r))                            
                if feedback: helpers.fbprint(feedback(r))

                continue

            raise AssertionError

        except AssertionError:
            print('Usage:{ {str|hash|list|set|zet} {<int>|all} | reset | exit | quit }')
            
        except Exception as err:
            print(err)
            # traceback.print_exc()

if __name__ == '__main__':

    load_dotenv()
    set_config()
    repl()
