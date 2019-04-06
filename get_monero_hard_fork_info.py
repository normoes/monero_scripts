import requests
import re
import os
import logging
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import sys

"""
Goal:
  * Get monero hard fork dates from /src/cryptonote_core/blockchain.cpp.

How to:
  * current master:
    - python get_monero_hard_fork_info.py
    - python get_monero_hard_fork_info.py --branch master
  * It is also possible to set the branch name as environment variable: PROJECT_BRANCH_NAME.
    - PROJECT_BRANCH_NAME=master python get_monero_hard_fork_info.py
  * python get_monero_hard_fork_info.py --branch release-v0.11.0.0
        version 1 ['Apr 18 2014 UTC', '1', '1341378000']
        version 2 ['Mar 20 2016 UTC', '1009827', '1442763710']
        version 3 ['Sep 24 2016 UTC', '1141317', '1458558528']
        version 4 ['Jan 05 2017 UTC', '1220516', '1483574400']
        version 5 ['Apr 15 2017 UTC', '1288616', '1489520158']
        version 6 ['Sep 16 2017 UTC', '1400000', '1503046577'] 
  * python get_monero_hard_fork_info.py --branch release-v0.12
        ...
        version 7 ['Apr 06 2018 UTC', '1546000', '1521303150']
  * python get_monero_hard_fork_info.py --branch release-v0.13
        ...
        version 8 ['Oct 18 2018 UTC', '1685555', '1535889547']
        version 9 ['Oct 19 2018 UTC', '1686275', '1535889548']
        version 10 ['Mar 09 2019 UTC', '1788000', '1549792439']
        version 11 ['Mar 10 2019 UTC', '1788720', '1550225678']
"""


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


BRANCH_NAME = os.environ.get("PROJECT_BRANCH_NAME", None)

parser = argparse.ArgumentParser(description='Get monero hard fork dates from /src/cryptonote_core/blockchain.cpp.')
parser.add_argument('-b', '--branch', nargs='?', default="master", help='Branch to check /src/cryptonote_core/blockchain.cpp. If not given as argument, set PROJECT_BRANCH_NAME.')
args = parser.parse_args()

if not BRANCH_NAME:
    BRANCH_NAME = args.branch

URL = f"https://raw.githubusercontent.com/monero-project/monero/{BRANCH_NAME}/src/cryptonote_core/blockchain.cpp"
BEGINNING = "} mainnet_hard_forks\[\]"
END = "};"
VERSION = "  // (version \d+) (.+)"
DATE = "(\d+)th of (\w+), (\d+)"
INFO = "\d+, \d+, \d+, \d+"

def get_last_and_next_hardfork(url):
    response = requests.get(url)
    log.debug(response.status_code)
    log.debug(response.text)
    if response.status_code != 200:
        log.error(f"received HTTP status code {response.status_code} with {response.text}")
        sys.exit
    code = response.text
    start_line = re.compile(BEGINNING, re.IGNORECASE)
    end_line = re.compile(END, re.IGNORECASE)
    version_line = re.compile(VERSION, re.IGNORECASE)
    date_line = re.compile(DATE, re.IGNORECASE)

    interesting = defaultdict(list)
    interesting_range = False
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if line:
            if start_line.match(line):
                interesting_range = True
            if end_line.match(line) and interesting_range:
                interesting_range = False
                break
  
            if version_line.match(line) and interesting_range:
                groups = list(version_line.finditer(line))
                info = groups[0].group(2)
                date_ = list(date_line.finditer(info))
                
                if date_:
                    day = date_[0].group(1)
                    month = date_[0].group(2)
                    year = date_[0].group(3)
                else:
                    day = "18"
                    month = "April"
                    year = "2014"
                # make sure it has the correct format
                date_string = datetime.strptime(f"{month} {day} {year}", "%B %d %Y").strftime("%b %d %Y ") + str(timezone.utc)

                interesting[groups[0].group(1)].append(date_string)
                fork_info = lines[i+1]
                fork_info = fork_info.translate({ord('{'):None, ord(" "):None, ord("}"): None})
                fork_infos = fork_info[:-1].split(",")
                block = fork_infos[1]
                difficulty = fork_infos[-1]
                interesting[groups[0].group(1)].append(block)
                interesting[groups[0].group(1)].append(difficulty)
    return interesting


if __name__ == "__main__":
    stuff = get_last_and_next_hardfork(url=URL)
    for k, v in stuff.items():
        print(k, v)
