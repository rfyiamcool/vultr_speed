#!/usr/bin/env python

import signal
import json
import sys
import subprocess

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)
target_url = "https://www.vultr.com/faq/"


def exit(signum, frame):
    print('stop scan')
    exit()


def get_geo_link():
    try:
        rsp = requests.get(target_url, timeout=5)
    except:
        print('get vultr api error')
        exit()

    soup = BeautifulSoup(rsp.content, "lxml")
    geo_map = []
    for elem in soup.select('#speedtest_v4 > tr'):
        all_tds = elem.findAll('td')
        geo_location = all_tds[0].text.strip()
        ping_url = all_tds[1].findAll("a")[0].text.strip()
        geo_map.append((geo_location, ping_url))
    return geo_map


def fmt_speed(speed):
    if speed < 1024:
        return "%s B/s" % speed
    elif speed < 1024*1024:
        return "%s KB/s" % (speed*1.0/1024)
    else:
        return "%s MB/s" % (speed*1.0/1024/1024)


def speed_test(geo_loc, ping_url):
    cmd = ["ping", "-c 5", ping_url]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip()
    return output


def main():
    try:
        geo_map = get_geo_link()

        print("="*10 + "start speed testing..." + "="*10)
        for geo_info in geo_map:
            geo_loc = geo_info[0]
            geo_addr = geo_info[1]
            speed_out = speed_test(geo_loc, geo_addr)
            print("\ntesting [%s] %s result:\n%s" % (geo_loc, geo_addr, speed_out))

        print("="*10 + "end speed testing..." + "="*10)

    except:
        print("exit")


if __name__ == '__main__':
    main()
