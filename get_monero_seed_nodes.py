"""
Goal:
  * Get monero seed nodes from /src/p2p/net_node.inl.

How to:
  * for default values and how to use the tool
    - python get_monero_seed_nodes.py --help
  * current master:
    - python get_monero_seed_nodes.py
    - python get_monero_seed_nodes.py --branch master
  * It is also possible to set the branch name as environment variable: PROJECT_BRANCH_NAME.
    - PROJECT_BRANCH_NAME=master python get_monero_seed_nods.py
  * python get_monero_seed_nodes.py --branch release-v0.11.0.0
        testnet ['212.83.175.67:28080', '5.9.100.248:28080', '163.172.182.165:28080', '195.154.123.123:28080', '212.83.172.165:28080', '195.154.123.123:28080', '212.83.172.165:28080']
        mainnet ['107.152.130.98:18080', '212.83.175.67:18080', '5.9.100.248:18080', '163.172.182.165:18080', '161.67.132.39:18080', '198.74.231.92:18080']
  * python get_monero_seed_nodes.py --branch release-v0.15
        testnet ['212.83.175.67:28080', '5.9.100.248:28080', '163.172.182.165:28080', '195.154.123.123:28080', '212.83.172.165:28080', '192.110.160.146:28080']
        stagenet ['162.210.173.150:38080', '162.210.173.151:38080', '192.110.160.146:38080']
        mainnet ['107.152.130.98:18080', '212.83.175.67:18080', '5.9.100.248:18080', '163.172.182.165:18080', '161.67.132.39:18080', '198.74.231.92:18080', '195.154.123.123:18080', '212.83.172.165:18080', '192.110.160.146:18080']
  * It is possible to select the Monero network (mainnet, testnet, stagenet)
    - python get_monero_seed_nodes.py --network stagenet
"""

import re
import os
import logging
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import sys

import requests
from requests.exceptions import RequestException


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

NETWORK_MODES = ["mainnet", "stagenet", "testnet"]
ALL_NETWORK_MDOES = "all"

BRANCH_NAME = os.environ.get("PROJECT_BRANCH_NAME", None)
MONERO_NETWORK = os.environ.get("MONERO_NETWORK", None)
DAEMON_HOST = os.environ.get("DAEMON_HOST", None)

if MONERO_NETWORK and MONERO_NETWORK not in NETWORK_MODES:
    log.error(f"This is no known monero network mode: '{MONERO_NETWORK}'.")
    sys.exit(1)

TIMEOUT = 10

DAEMON_P2P_PORTS = {
    NETWORK_MODES[0]: 18080,
    NETWORK_MODES[1]: 38080,
    NETWORK_MODES[2]: 28080,
}

DAEMON_PORT_NETWORK_MAP = {
    18080: NETWORK_MODES[0],
    38080: NETWORK_MODES[1],
    28080: NETWORK_MODES[2],
}

URL_DEFAULT = "https://raw.githubusercontent.com/monero-project/monero/{branch_name}/src/p2p/net_node.inl"
URL = None
if BRANCH_NAME:
    URL = URL_DEFAULT.format(branch_name=BRANCH_NAME)
DAEMON_ADDRESS_DEFAULT = "http://{daemon_host}:{daemon_port}/json_rpc"
DAEMON_ADDRESS = None
if DAEMON_HOST and MONERO_NETWORK:
    DAEMON_ADDRESS = DAEMON_ADDRESS_DEFAULT.format(
        daemon_host=DAEMON_HOST, daemon_port=DAEMON_P2P_PORTS[MONERO_NETWORK]
    )

# Make 'flake8' ignore [W605 invalid escape sequence] - escape sequence necessary for regular expression.
# noqa: W605
START = "::get_seed_nodes\("
SEED_NODES_COMPLETE = 'full_addrs\.insert\("(.*):([0-9]{2,5})"\);'
END = "return full_addrs;"


def get_seed_nodes(
    url=URL,
    # daemon_address=DAEMON_ADDRESS,
    monero_network=MONERO_NETWORK,
    timeout=TIMEOUT,
):
    if (
        monero_network not in NETWORK_MODES
        and not monero_network == ALL_NETWORK_MDOES
    ):
        log.error(f"This is no known monero network mode '{monero_network}'.")
        sys.exit(1)

    lines = []
    interesting = defaultdict(list)
    try:
        response = requests.get(url, timeout=timeout)

        log.debug(response.status_code)
        log.debug(response.text)
        if response.status_code != 200:
            log.error(
                f"Received HTTP status code '{response.status_code}' for '{url}' with '{response.text}'."
            )
            sys.exit(1)
        code = response.text
        start_line = re.compile(START, re.IGNORECASE)
        seed_node_line = re.compile(SEED_NODES_COMPLETE, re.IGNORECASE)
        end_line = re.compile(END, re.IGNORECASE)

        interesting_range = False
        lines = code.split("\n")
    except (RequestException) as e:
        log.error(f"Cannot get information from '{url}', because: '{str(e)}'.")

    for i, line in enumerate(lines):
        line = line.strip()
        if line:
            if start_line.search(line):
                interesting_range = True
            if end_line.match(line) and interesting_range:
                interesting_range = False
                break
            if interesting_range:
                seed_node_match = seed_node_line.match(line)
                if seed_node_match:
                    seed_node_info = seed_node_match.groups()
                    seed_node = seed_node_info[0]
                    node_port = int(seed_node_info[1])
                    network_mode = DAEMON_PORT_NETWORK_MAP.get(
                        node_port, "undefined"
                    )
                    interesting[network_mode].append(
                        f"{seed_node}:{node_port}"
                    )

    if monero_network == ALL_NETWORK_MDOES:
        return interesting
    else:
        return {monero_network: interesting[monero_network]}


def main():
    parser = argparse.ArgumentParser(
        description="Get monero seed nodes from /src/p2p/net_node.inl.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-b",
        "--branch",
        nargs="?",
        default="master",
        help="Branch to check /src/p2p/net_node.inl. If not given as argument, set PROJECT_BRANCH_NAME.",
    )
    parser.add_argument(
        "-n",
        "--network",
        nargs="?",
        default=ALL_NETWORK_MDOES,
        help="Monero network to check (mainnet, stagenet, testnet). If not given as argument, set MONERO_NETWORK.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show debug info."
    )

    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    if BRANCH_NAME:
        branch_name = BRANCH_NAME
    else:
        branch_name = args.branch

    if MONERO_NETWORK:
        monero_network = MONERO_NETWORK
    else:
        monero_network = args.network

    url = URL_DEFAULT.format(branch_name=branch_name)
    log.info(url)

    stuff = get_seed_nodes(url=url, monero_network=monero_network)
    for k, v in stuff.items():
        print(k, v)


if __name__ == "__main__":
    sys.exit(main())
