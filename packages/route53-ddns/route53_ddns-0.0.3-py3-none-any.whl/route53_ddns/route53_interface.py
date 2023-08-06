import logging
from time import sleep
from typing import Optional

import boto3

route53 = boto3.client("route53")

logger = logging.getLogger(__name__)


def get_hosted_zone_id(zone_name: str) -> str:
    """Gets the ZoneId of the required zone, by iterating over all list zones and checking the zone name.

    Args:
        zone_name (str): The DNS name of the zone, like `mydomain.com`

    Returns:
        str: the id of the zone as returned by Route53, like `/hostedzone/XXXXXXXXXXX`
    """
    zones = route53.list_hosted_zones()
    logger.debug(f"list_hosted_zones output: {zones}")
    if not zones["HostedZones"]:
        logger.fatal(f"No zone found in the account. Please check if you have the right AWS credentials in place.")
        raise KeyError(f"No zone found in the account")

    for zone in zones["HostedZones"]:
        if zone["Name"].startswith(zone_name):
            logger.info(f"Found zone {zone['Id']} with name {zone['Name']} matching the expected {zone_name}")
            return zone["Id"]

    raise ValueError(f"No zone found matching {zone_name}")


def wait_for_change_completion(change_id: str, wait_time: int = 5) -> None:
    """Wait for the change to be propagated.

    This is simply a wrappe around boto3.get_change, calling it every
    `wait_time` seconds until the change result `INSYNC`.

    Note:
        Route53 API documentation set the only possible values of a change to be either `PENDING` or `INSYNC`.

    Args:
        change_id (str): the ID of the change to track, returned by any route53 API that returns a `ChangeInfo`
        wait_time (:obj:`int`, optional): the number of seconds between checks of the change status, defaults to 5
    """
    change_status = None
    while True:  # TODO: add a limit of the iterations
        # Get the curret status
        response = route53.get_change(Id=change_id)
        change_status = response["ChangeInfo"]["Status"]
        logger.debug(f"get_change output: {response}")

        if change_status == "INSYNC":
            logger.info(f"Change {change_id} has completed with status {change_status}")
            return

        logger.info(f"Status of change {change_id} is still pending. Waiting {wait_time} seconds")
        sleep(wait_time)


def get_current_ip(zone_id: str, record_name: str) -> Optional[str]:
    logger.info("Checking current records")
    zone_records = route53.list_resource_record_sets(HostedZoneId=zone_id)

    matched = None
    for record in zone_records["ResourceRecordSets"]:
        logger.info(f"Found record of type {record['Type']} with ttl {record['TTL']} named {record['Name']}")

        if record["Name"] == f"{record_name}.":
            matched = record
            break

    if matched:
        logger.info(f"Found matching record for {record_name}: {record}")
        if matched["Type"] != "A":
            raise ValueError(
                f"The current record for {record_name} is of type {matched['Type']}! Use a different record."
            )
        resource_record = record["ResourceRecords"]
        if len(resource_record) > 1:
            raise ValueError(
                f"The current A record for {record_name} has {len(resource_record)} entries: "
                f"{', '.join(i['Value'] for i in resource_record)}. "
                f"This operations is unsafe, please use a different record name, or remove the existing entry manually."
            )
        current_dns_ip = resource_record[0]["Value"]
        logger.info(f"The current target for {record_name} is {current_dns_ip}")
        return current_dns_ip
    else:
        logger.info(f"No records found matching {record_name}. A new 'A' record would be created.")
        return None


def update_record(zone_name: str, record_name: str, target_ip: str, dryrun: bool = False) -> None:
    zone_id = get_hosted_zone_id(zone_name=zone_name)

    current_ip = get_current_ip(zone_id=zone_id, record_name=record_name)
    if current_ip == target_ip:
        logger.info(f"The current value of {record_name} matches the current IP, nothing to do.")
        return
    else:
        logger.info(f"The current value of {record_name} points to {current_ip}. Will update to {target_ip}")

    if dryrun:
        logger.info("Running in dryrun mode, not updating Route53")
        return

    logger.info(f"Submitting the change for {record_name} to point to {target_ip}")
    update_response = route53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": f"Updating record to {target_ip}",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": "A",
                        "TTL": 60,
                        "ResourceRecords": [{"Value": target_ip}],
                    },
                }
            ],
        },
    )

    change_id = update_response["ChangeInfo"]["Id"]
    wait_for_change_completion(change_id=change_id)
    logger.info("Update completed")
