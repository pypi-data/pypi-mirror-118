import json
import logging
from socket import gaierror, gethostbyname_ex
from time import sleep

import requests

logger = logging.getLogger(__name__)


def get_ip() -> str:
    """Returns the current public IP, using https://www.ipify.org/

    Returns:
        str: the current public IP
    """
    raw_response = requests.get("https://api.ipify.org?format=json")
    logger.debug(f"ipify response: {raw_response} -> {raw_response.content!r}")
    response = json.loads(raw_response.content)
    logger.info(f"Detected IP {response['ip']}")
    return response["ip"]


def verify_propagation(record: str, target_ip: str) -> bool:
    try:
        _, _, ipaddrlist = gethostbyname_ex(record)
        if target_ip in ipaddrlist:
            if len(ipaddrlist) > 1:
                logger.warning(f"Record {record} resolves to multiple IPs: {', '.join(ipaddrlist)}")
                return False
            else:
                logger.info(f"Record {record} points to {target_ip}")
            return True
        else:
            logger.error(f"Record {record} points to {', '.join(ipaddrlist)}, rather than pointing to {target_ip}")
            return False
    except gaierror:
        logger.error(f"Record {record} is not resolvabe")
        return False


def wait_for_propagation(record: str, target_ip: str, wait_time: int = 5) -> None:
    while not verify_propagation(record=record, target_ip=target_ip):  # TODO: add a maz retry
        logger.info(f"Change for {record} to resolve to {target_ip} has not been propagated yet")
        sleep(wait_time)
