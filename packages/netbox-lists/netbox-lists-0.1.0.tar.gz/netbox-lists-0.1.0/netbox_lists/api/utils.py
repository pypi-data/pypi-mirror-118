from netaddr import IPNetwork


def as_cidr(ipn: IPNetwork) -> str:
    return str(ipn.ip) + "/32" if ipn.version == 4 else str(ipn.ip) + "/128"
