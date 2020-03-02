import socket


def try_to_connect(node) -> bool:
    """
    'socket.connect()' requires a tuple(str, int).
    Can be given to this function as string as well "url:port" and will be turned into the proper tuple().
    """

    node_ = None

    if isinstance(node, str):
        node_parts = node.split(":")
        node_ = (node_parts[0], int(node_parts[1]))
    elif isinstance(node, tuple):
        node_ = node

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect(node_)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    # Monero seed nodes
    seed_nodes = [
        ("198.74.231.92:18080"),
        ("198.74.231.92", 18080),
        ("161.67.132.39", 18080),
        ("192.110.160.146", 18080),
        ("212.83.172.165", 18080),
        ("107.152.130.98", 18080),
        ("195.154.123.123", 18080),
        ("212.83.175.67", 18080),
        ("163.172.182.165", 18080),
        ("5.9.100.248", 18080),
    ]

    for node in seed_nodes:
        try_to_connect(node)
