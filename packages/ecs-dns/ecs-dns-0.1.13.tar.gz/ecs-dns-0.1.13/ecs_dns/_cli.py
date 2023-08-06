"""Console script for ECS CNAME."""
import sys

import click

from ecs_dns import (
    create_health_check,
    create_dns_record,
    find_private_ips,
    find_public_ips,
)


@click.command()
@click.argument("dns_name")
@click.option(
    "-c",
    "--container-name",
    default=None,
    type=click.STRING,
    help="Container name to create a record for.",
)
@click.option(
    "-p",
    "--port",
    default=80,
    type=click.INT,
    help="Port for the healthcheck to query.",
)
@click.option(
    "--protocol",
    default="HTTP",
    type=click.STRING,
    help="Protocol for the healthcheck to use.",
)
def cli(dns_name: str, container_name: str, port: int, protocol: str):
    """Automatically determine a container's public IP and create a multi-value A record and healthcheck for it.

    If multiple containers with public IPs are found, or if one container has multiple
    public IPs, only the first will be used.
    """
    private_ips = list(find_private_ips(container_name))
    click.echo(f"Found private IPs: {private_ips}")
    public_ip_groups = [find_public_ips(ip) for ip in private_ips]
    public_ips = list(set([i for group in public_ip_groups for i in group]))
    click.echo(f"Search result: {public_ips}")
    ip = public_ips[0]
    if ip not in private_ips:
        click.echo(f"Creating health check...")
        healthcheck = create_health_check(ip, dns_name, port, protocol)
        click.echo(f"Updating Route53...")
        create_dns_record(ip, dns_name, healthcheck)
    else:
        click.echo(f"Updating Route53...")
        create_dns_record(ip, dns_name)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
