#!/usr/bin/env python3

import time
import json
import os
import re
from scanner import download, chan_info
import subprocess
import urllib.request
import threading


def get_catalog_json(board, chan):
    chan_base_url = chan_info.get_chan_info(chan)[0]
    catalog = urllib.request.urlopen(
              "{0}{1}/catalog.json".format(chan_base_url, board))
    return json.loads(catalog.read().decode("utf8"))


def scan_thread(keyword, catalog_json):
    # Check each thread, threads who contains the keyword are returned
    matched_threads = []
    for i in range(len(catalog_json)):
        for thread in catalog_json[i]["threads"]:
            regex = r'\b{0}\b'.format(keyword)
            # Search thread title
            if 'sub' in thread:
                if re.search(regex, str(thread["sub"]), re.IGNORECASE):
                    matched_threads.append(thread["no"])

            # Search OPs post body
            if 'com' in thread:
                if re.search(regex, str(thread["com"]), re.IGNORECASE):
                    matched_threads.append(thread["no"])

    return matched_threads


def download_thread(thread_id, chan, board, folder, output):
    t = threading.Thread(target=download.download_thread, args=(thread_id,
                                                                board,
                                                                chan,
                                                                output,
                                                                folder,
                                                                True))
    t.daemon = True
    t.start()


def add_to_downloaded(id, log_file, output):
    download_log = open("{0}/{1}".format(output, log_file), "a")
    download_log.write("{0}\n".format(id))


def scan(keywords_file, output, log_file):
    while True:
        curr_time = time.strftime('%d/%b/%Y-%H:%M')
        print("{0} Searching threads...".format(curr_time))

        dl_log = open("{0}/{1}".format(output, log_file), "a")
        dl_log.write(time.strftime('Execution date {0}\n'.format(curr_time)))
        dl_log.close()

        json_file = json.load(open(keywords_file))

        for search in json_file["searches"]:
            if 'imageboard' in search:
                chan = search["imageboard"]
                if not chan_info.get_chan_info(chan):
                    print("{0} is not supported.".format(chan))
                    exit(1)
            else:
                # default
                chan = "4chan"

            folder_name = search["folder_name"]
            board = search["board"]
            keywords = search["keywords"]
            try:
                catalog_json = get_catalog_json(board, chan)

                for keyword in keywords:
                    threads_id = scan_thread(keyword, catalog_json)

                    dl_log = open("{0}/{1}".format(output, log_file)).read()
                    for thread_id in list(set(threads_id)):
                        if str(thread_id) not in dl_log:
                            download_thread(thread_id, chan, board,
                                            folder_name,
                                            output)
                            add_to_downloaded(thread_id, log_file, output)
            except urllib.error.HTTPError as err:
                print("Error while opening {0} catalog page. "
                      "Retrying during next scan.".format(board))
                pass

        active_downloads = threading.active_count()-1
        print("{0} threads currently downloading.".format(active_downloads))
        print("Searching again in 5 minutes!")
        time.sleep(300)
