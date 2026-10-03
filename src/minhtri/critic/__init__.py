"""External critic boundary for blind, packet-hash-bound review.

The manual channel is intentionally network-free. API providers are not enabled here.
"""

from .packet import CriticPacketError, build_critic_packet, verify_packet_hash
from .provider_manual import ManualExternalCritic
from .verdict_schema import (
    CRITIC_DEFECT_FOUND,
    CRITIC_NO_MATERIAL_DEFECT_FOUND,
    CriticResult,
    CriticSchemaError,
)

__all__ = [
    "CRITIC_DEFECT_FOUND",
    "CRITIC_NO_MATERIAL_DEFECT_FOUND",
    "CriticPacketError",
    "CriticResult",
    "CriticSchemaError",
    "ManualExternalCritic",
    "build_critic_packet",
    "verify_packet_hash",
]
