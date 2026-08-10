"""Aggregate the three reviewed A1 final-decision partitions."""

from scripts.a1_final_decisions_01_identity_routines import DECISIONS as PART_1
from scripts.a1_final_decisions_02_places_services import DECISIONS as PART_2
from scripts.a1_final_decisions_03_media_social import DECISIONS as PART_3
from scripts.a1_final_decisions_03_media_social import TRANSFER_OVERRIDES


DECISIONS = PART_1 + PART_2 + PART_3
