import socket
import logging


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def make_connection(node):
    """
    'socket.connect()' requires a tuple(str, int).
    Can be given to this function as string as well "url:port" and will be turned into the proper tuple().
    """

    node_ = None

    # Make sure port is 'int'.
    # Make tuple.
    if isinstance(node, str):
        ip, port = node.split(":")
    elif isinstance(node, tuple):
        ip, port = node[0], node[1]
    node_ = (ip, int(port))

    # TCP: SOCK_STREAM
    # UDP: SOCK_DGRAM
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        log.info(f"Trying to connect to '{ip}:{port}'.")
        sock.connect(node_)
        log.info(f"Successfully connected to '{ip}:{port}'.")
    finally:
        sock.close()

    return True


def try_to_connect_keep_errors(node) -> bool:
    """Connects to node.

    Errors are reported back to the caller.
    Exceptions are not handled..
    """

    return make_connection(node)


def try_to_connect(node) -> bool:
    """Connects to node.

    In case of an error, 'False is returned.'
    Exceptions are handled.
    """

    try:
        return make_connection(node)
    except Exception as e:
        log.error(str(e))
        return False


if __name__ == "__main__":
    # Monero seed nodes
    seed_nodes = [
        ("198.74.231.92:18080"),
        ("198.74.231.92", 18080),
        ("198.74.231.92", "18080"),
        # ("161.67.132.39", 18080),
        # ("192.110.160.146", 18080),
        # ("212.83.172.165", 18080),
        # ("107.152.130.98", 18080),
        # ("195.154.123.123", 18080),
        # ("212.83.175.67", 18080),
        # ("163.172.182.165", 18080),
        # ("5.9.100.248", 18080),
    ]

    for node in seed_nodes:
        try_to_connect(node)
    for node in seed_nodes:
        try:
            try_to_connect_keep_errors(node)
        except (ConnectionError, socket.timeout, socket.gaierror) as e:
            print(f"Error: '{str(e)}'.")
