#!/usr/bin/env python3

import logging
import sys
from typing import List

import click

from route53_ddns.ip_utilities import get_ip, verify_propagation, wait_for_propagation
from route53_ddns.route53_interface import update_record


def _setup_logging(verbose: int = 0, log_file: str = None):
    handlers: List[logging.StreamHandler] = []
    if log_file:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(filename=log_file)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    if verbose > 0:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        handlers.append(stdout_handler)

    logging.basicConfig(level=logging.DEBUG if verbose > 1 else logging.INFO, handlers=handlers)


@click.command()
@click.option("--zone", required=True, type=str, help="The name of the zone to update, for example 'example.net'")
@click.option("--record", required=True, type=str, help="The record to update, for example 'home'")
@click.option("-c", "--check-only", is_flag=True, default=False, help="Only preform a check if DNS entry is correct")
@click.option(
    "-d", "--dryrun", is_flag=True, default=False, help="Doens't update any record, only tell what it would do."
)
@click.option("-v", "--verbose", count=True, help="Increase verbosity. Once logs to stdout, two set level to DEBUG.")
@click.option("-l", "--log-file", required=False, default="/tmp/route53-ddns.log", help="Log file")
def route53_ddns(zone: str, record: str, check_only: bool, dryrun: bool, verbose: int, log_file: str):
    """Simple CLI that updated an AWS Route53 A record to point to the current IP.

    If you have a Hosted Zone in your AWS account called `example.com` and you want to have
    `home.example.net` pointing to your public IP address, you can do:

    $ route53-ddns --zone example.com --record home

    $ route53-ddns --zone example.com --record home.example.com

    If the record doesn't end with the zone, it will be automatically appended for you.
    """
    _setup_logging(verbose=verbose, log_file=log_file)
    if not record.endswith(zone):
        record = f"{record}.{zone}"
        logging.info(f"Adjusting target record to be {record}")

    target_ip = get_ip()

    if check_only:
        logging.info(f"Running in check-only mode. Validating propagation of {target_ip}")
        verify_propagation(record=record, target_ip=target_ip)
        return

    update_record(zone_name=zone, record_name=record, target_ip=target_ip, dryrun=dryrun)
    wait_for_propagation(record=record, target_ip=target_ip)


if __name__ == "__main__":
    route53_ddns()
