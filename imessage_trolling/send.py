import time
from imsg import send_message, stacker, keep, convert, caser

from dotenv import load_dotenv
import argparse
import os

load_dotenv()
NUMBER = os.getenv('NUMBER')
SPACER = os.getenv('SPACER')
REPEATS = os.getenv('REPEATS')
INTERVAL = os.getenv('INTERVAL')
STACK = [keep]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "hi bro")
    parser.add_argument('message', type = str, help = 'bum')
    parser.add_argument('--num', type = str, default = NUMBER, help = 'wdyt bro')
    parser.add_argument('--spacer', type = str, default = SPACER, help = 'hi')
    parser.add_argument('--rep', type = int, default = REPEATS, help = 'h')
    parser.add_argument('--inter', type = int, default = INTERVAL, help = 'h')
    parser.add_argument('--font', default = False, action = 'store_true', help = 'hi bro :3')
    parser.add_argument('--cap', default = False, action = 'store_true', help = 'capitalize first letter of all words')

    args = parser.parse_args()    
    if args.cap:
        STACK.append(caser)
    if args.font:
        STACK.append(convert)

    for _ in range(args.rep):
        send_message(args.num, stacker(args.spacer.join([c for c in args.message]), *STACK))
        time.sleep(args.inter)


