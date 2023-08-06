"""Main module."""

import hashlib
import json
import logging
import os
from typing import Dict, Generator, List

import boto3
import requests

from ecs_dns import METADATA_URL
from ecs_dns.models import ECSTaskMetadata

log = logging.getLogger("ecs-dns")
log.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))


def find_private_ips(container_name=None) -> Generator[str, None, None]:
    """Invoke the metadata endpoint to get the private IPs for all containers in a running task."""
    raw_metadata = requests.get(METADATA_URL).text
    log.debug(f"Got metadata: {raw_metadata}")

    metadata = ECSTaskMetadata(**json.loads(raw_metadata))
    for container in metadata.Containers:
        if container_name and container_name != container.Name:
            continue
        for network in container.Networks:
            yield from network.IPv4Addresses


def _get_network_info(private_ip: str, result_key: str) -> Generator[str, None, None]:
    """Accept a private IP and yield the `result_key` value from each NetworkInterface's Association object.

    NOTE: If there is no public IP associated with the private IP, the private IP is yielded as a fallback.
    """
    client = boto3.client("ec2")
    filters = [{"Name": "addresses.private-ip-address", "Values": [private_ip]}]
    response = client.describe_network_interfaces(Filters=filters)
    log.debug(f"_get_network_info response: {response}")
    for interface in response["NetworkInterfaces"]:
        if "Association" in list(interface.keys()):
            yield interface["Association"][result_key]
        else:
            yield interface["PrivateIpAddress"]


def find_public_dns_names(private_ip: str) -> List[str]:
    """Find the public DNS names associated with a private IP."""
    return list(_get_network_info(private_ip, "PublicDnsName"))


def find_public_ips(private_ip: str) -> List[str]:
    """Find the public IPs associated with a private IP."""
    return list(_get_network_info(private_ip, "PublicIp"))


def create_dns_record(public_ip: str, dns_name: str, healthcheck_id: str):
    """Create a Route53 multi-value A record with healthcheck."""
    client = boto3.client("route53")

    # set identifiers are used in multi-value record sets to uniquely id a record
    hash_str = f"{public_ip}/{dns_name}".encode("utf-8")
    set_identifier = hashlib.md5(hash_str).hexdigest()

    record_set = {
        "Name": dns_name,
        "Type": "A",
        "SetIdentifier": set_identifier,
        "MultiValueAnswer": True,
        # when using a health check, AWS recommends a TTL of 60 seconds or less.
        "TTL": 30,
        "ResourceRecords": [
            {"Value": public_ip},
        ],
        "HealthCheckId": healthcheck_id,
    }

    # get the domain's hosted zone id
    zone_name = ".".join(dns_name.split(".")[-2:])
    resp = client.list_hosted_zones_by_name(DNSName=zone_name)
    zone_id = resp["HostedZones"][0]["Id"].split("/")[-1]

    resp = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "Created on container startup by ecs_dns.",
            "Changes": [{"Action": "UPSERT", "ResourceRecordSet": record_set}],
        },
    )


def create_health_check(
    public_ip: str,
    dns_name: str,
    port: int = 80,
    protocol: str = "HTTP",
    path: str = "/",
    interval: int = 30,
    failure_threshold: int = 3,
) -> str:
    """Create a Route53 healthcheck and return its ID.

    Args:
        public_ip: str
        dns_name: str
        port: int = 80
        protocol: str = "HTTP" - Can be 'HTTP'|'HTTPS'|'HTTP_STR_MATCH'|'HTTPS_STR_MATCH'|'TCP'|'CALCULATED'|'CLOUDWATCH_METRIC'|'RECOVERY_CONTROL'
        path: str = "/" - Ignored if type does not match HTTP*
        interval: int = 30
        failure_threshold: int = 3
    """
    client = boto3.client("route53")
    # caller reference is a unique string that identifies the request and that allows you to retry a failed
    # CreateHealthCheck request without the risk of creating two identical health checks
    hash_str = f"{public_ip}/{dns_name}".encode("utf-8")
    caller_reference = hashlib.md5(hash_str).hexdigest()

    config = {
        "IPAddress": public_ip,
        "Port": port,
        "Type": protocol,
        "RequestInterval": interval,
        "FailureThreshold": failure_threshold,
    }
    if protocol.startswith("HTTP"):
        config["ResourcePath"] = path

    response = client.create_health_check(
        CallerReference=caller_reference, HealthCheckConfig=config
    )
    return response["HealthCheck"]["Id"]
