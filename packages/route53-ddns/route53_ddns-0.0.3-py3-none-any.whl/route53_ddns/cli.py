#!/usr/bin/env python3

import logging
from ipaddress import ip_address
import logging.handlers
import sys
from typing import List

import click

from route53_ddns.ip_utilities import get_ip, verify_propagation, wait_for_propagation
from route53_ddns.route53_interface import update_record


def _setup_logging(verbose: int = 0, log_file: str = None, quiet: bool = False):
    """Setup the logging for route54-ddns.

    if a `file` is provided, will use a `RotatingFileHandler` with 1MB maximum, with three backups.
    Verbosity currently supports two levels:
    * 1: sends the logs to stdout as well
    * 2: increaste log level to DEBUG (still tells urllib3 to stay at INFO level)

    Arguments:
        verbose (int): set the verbosity level. 1 sends to stdout, 2 enable DEBUG logs
        log_file (:obj:`str`, optional): the path of the log file
        quiet (bool): quiet mode, prevent any log to be emitted
    """
    handlers: List[logging.Handler] = []
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    if quiet:
        # Quiet overrides any other setting.
        handlers.append(logging.NullHandler())
    else:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        handlers.append(stdout_handler)

        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(filename=log_file, maxBytes=1_048_576, backupCount=3)
            file_handler.setFormatter(formatter)
            handlers.append(file_handler)

    logging.basicConfig(level=logging.DEBUG if verbose > 0 else logging.INFO, handlers=handlers)
    # urllib and botocore are very verbose. Forcing it to stay at INFO level
    logging.getLogger("urllib3").setLevel(logging.INFO)
    logging.getLogger("botocore").setLevel(logging.INFO)


@click.command()
@click.option("--zone", required=True, type=str, help="The name of the zone to update, for example 'example.net'")
@click.option("--record", required=True, type=str, help="The record to update, for example 'home'")
@click.option("--ip", required=False, help="Provide the IP to set, rather than detect it from ipify.org")
@click.option("-c", "--check-only", is_flag=True, default=False, help="Only preform a check if DNS entry is correct")
@click.option("-d", "--dryrun", is_flag=True, default=False, help="Doesn't update DNS")
@click.option("-v", "--verbose", count=True, help="Increase logging verbosity")
@click.option("-l", "--log-file", required=False, help="Log file. If not provided no logs file will be produced")
@click.option("-q", "--quiet", is_flag=True, help="Quiet mode, suppresses all logs")
def route53_ddns(
    zone: str, record: str, ip: str, check_only: bool, dryrun: bool, verbose: int, log_file: str, quiet: bool
) -> int:
    """Simple CLI that updated an AWS Route53 A record to point to the current IP.

    If you have a Hosted Zone in your AWS account called `example.com` and you want to have
    `home.example.net` pointing to your public IP address, you can do:

    $ route53-ddns --zone example.com --record home

    $ route53-ddns --zone example.com --record home.example.com

    If the record doesn't end with the zone, it will be automatically appended for you.
    """
    _setup_logging(verbose=verbose, log_file=log_file, quiet=quiet)
    if not record.endswith(zone):
        record = f"{record}.{zone}"
        logging.info(f"Adjusting target record to be {record}")

    if ip:
        try:
            logging.debug(f"Validating ip {ip}")
            ip_address(ip)
            target_ip = ip
        except ValueError as e:
            logging.fatal(f"IP {ip} doesn't appear to be valid: {e}")
            return 1

    else:
        target_ip = get_ip()

    if check_only:
        logging.info(f"Running in check-only mode. Validating propagation of {target_ip}")
        verify_propagation(record=record, target_ip=target_ip)
        return 0

    update_record(zone_name=zone, record_name=record, target_ip=target_ip, dryrun=dryrun)
    wait_for_propagation(record=record, target_ip=target_ip)
    return 0


if __name__ == "__main__":
    sys.exit(route53_ddns())
