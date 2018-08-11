#!/usr/bin/env python

import json
import sys
import subprocess

import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


target_url = "https://www.vultr.com/faq/"


def get_geo_link():
    rsp = requests.get(target_url)
    soup = BeautifulSoup(rsp.content, "html.parser")
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
    geo_map = get_geo_link()

    print("="*10 + "start speed testing..." + "="*10)

    for geo_info in geo_map:
        geo_loc = geo_info[0]
        geo_addr = geo_info[1]
        speed_out = speed_test(geo_loc, geo_addr)
        print
        print("testing [%s] %s result: %s \n" % (geo_loc, geo_addr, speed_out))
        print

    print("="*10 + "end speed testing..." + "="*10)


if __name__ == '__main__':
    main()
