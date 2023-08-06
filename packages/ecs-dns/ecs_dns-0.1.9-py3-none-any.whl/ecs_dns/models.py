"""Data models for ECS CNAME."""

from dataclasses import dataclass, fields
from typing import Dict, List


@dataclass(init=False, order=True)
class ECSNetworkMetadata:
    """ECS container network metadata."""

    NetworkMode: str
    IPv4Addresses: List[str]

    # doing this because AWS sends us keys we super don't care about
    def __init__(self, **kwargs):  # noqa: D107
        keys = set([field.name for field in fields(self)])
        for k, v in kwargs.items():
            if k in keys:
                setattr(self, k, v)


@dataclass(init=False, order=True)
class ECSContainerMetadata:
    """ECS container metadata."""

    DockerId: str
    Name: str
    DockerName: str
    Image: str
    ImageID: str
    Labels: Dict[str, str]
    DesiredStatus: str
    KnownStatus: str
    Limits: Dict[str, int]
    CreatedAt: str
    StartedAt: str
    Type: str
    Networks: List[ECSNetworkMetadata]

    # doing this because AWS sends us keys we super don't care about
    def __init__(self, **kwargs):  # noqa: D107
        keys = set([field.name for field in fields(self)])
        for k, v in kwargs.items():
            if k == "Networks":
                setattr(self, k, [ECSNetworkMetadata(**network) for network in v])
            elif k in keys:
                setattr(self, k, v)


@dataclass(init=False, order=True)
class ECSTaskMetadata:
    """ECS task metadata response object."""

    Cluster: str
    TaskARN: str
    Family: str
    Revision: str
    DesiredStatus: str
    KnownStatus: str
    Containers: List[ECSContainerMetadata]
    PullStartedAt: str
    PullStoppedAt: str
    AvailabilityZone: str

    # doing this because AWS sends us keys we super don't care about
    def __init__(self, **kwargs):  # noqa: D107
        keys = set([field.name for field in fields(self)])
        for k, v in kwargs.items():
            if k == "Containers":
                setattr(self, k, [ECSContainerMetadata(**container) for container in v])
            elif k in keys:
                setattr(self, k, v)
