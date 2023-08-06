import logging
import time
import random
import argparse
from .login import Login
from .ping import ping


def random_sleep(mean, std):
    time_gap = int(random.gauss(mean, std))
    logging.info("sleep:{} min {:.2f} s".format(time_gap // 60, time_gap % 60))
    time.sleep(time_gap)


def schedule(configs):
    while True:
        if not ping(url='https://www.baidu.com'):
            logging.info("网络异常，尝试登录NBU账号")
            Login(configs.file).try_all()
        random_sleep(300, 60)


def fly():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("/tmp/fly_online.log"),
            logging.StreamHandler()
        ]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='password.txt')
    parser.add_argument('-l', '--login', default=False, action='store_true')
    args = parser.parse_args()
    if args.login:
        Login(args.file).try_all()
    else:
        schedule(args)


if __name__ == '__main__':
    fly()
