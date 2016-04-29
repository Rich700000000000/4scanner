#!/usr/bin/env python3

import argparse
from scanner import chan_info
import json
import logging
import os
import sys
import re
import time
import urllib
import http.client
import requests
import threading


def load(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def add_to_downloaded_log(img_filename, tmp_log):
    f = open(tmp_log, "a")
    f.write("{0}\n".format(img_filename))
    f.close()


def was_downloaded(img_filename, tmp_log):
    if os.path.isfile(tmp_log):
        f = open(tmp_log, "r")
        if str(img_filename) in f.read():
            f.close()
            return True
        else:
            return False
    else:
        return False


def download_thread(thread_nb, board, chan, output_folder, folder, is_quiet):

    # Getting info about the chan URL
    chan_url_info = chan_info.get_chan_info(chan)
    if not chan_url_info:
        print("{0} does not exist or is not supported.".format(chan))
        exit(1)
    base_url = chan_url_info[0]
    image_url = chan_url_info[3]
    thread_subfolder = chan_url_info[1]
    image_subfolder = chan_url_info[2]

    thread_url = "{0}{1}{2}{3}.json".format(base_url,
                                            board,
                                            thread_subfolder,
                                            thread_nb)
    image_url = "{0}{1}{2}".format(image_url, board, image_subfolder)

    tmp_log = ("/tmp/4scanner_tmp_{0}_{1}"
               .format(os.getpid(), threading.current_thread().name))

    directory = os.path.join(output_folder, 'downloads', chan, board,
                             folder + "/")
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:  # folder may have been created by other threads
            if e.errno != 17:
                raise
            pass

    while True:
        try:
            thread_json = json.loads(load(thread_url))
            for post in thread_json["posts"]:
                if 'filename' in post:
                    if not was_downloaded(post["tim"], tmp_log):
                        try:
                            pic_url = "{0}{1}{2}".format(image_url,
                                                         post["tim"],
                                                         post["ext"])
                            out_pic = "{0}{1}{2}".format(directory,
                                                         post["tim"],
                                                         post["ext"])
                            urllib.request.urlretrieve(pic_url, out_pic)
                        except urllib.error.HTTPError as err:
                            pass
                        add_to_downloaded_log(post["tim"], tmp_log)
                        time.sleep(2)
                # Some imageboards allow more than 1 picture per post
                if 'extra_files' in post:
                    for picture in post["extra_files"]:
                        if not was_downloaded(post["tim"], tmp_log):
                            try:
                                pic_url = "{0}{1}{2}".format(image_url,
                                                             picture["tim"],
                                                             post["ext"])
                                out_pic = "{0}{1}{2}".format(directory,
                                                             picture["tim"],
                                                             picture["ext"])
                                urllib.request.urlretrieve(pic_url, out_pic)
                            except urllib.error.HTTPError as err:
                                pass
                            add_to_downloaded_log(picture["tim"], tmp_log)
                            time.sleep(2)
            if not is_quiet:
                print('.')
            time.sleep(20)
        except requests.exceptions.HTTPError as err:
            if not is_quiet:
                print('thread 404\'d')
            os.unlink(tmp_log)
            exit(0)
