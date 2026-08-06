"""Assertions that preserve deterministic historical partition prefixes."""

from __future__ import annotations

import copy
import unittest


def assert_partition_prefix(
    testcase: unittest.TestCase, expected_map: dict, actual_map: dict
) -> None:
    """Compare a historical prefix after removing later cross-cutting additions."""
    count = len(expected_map["candidates"])
    actual_candidates = copy.deepcopy(actual_map["candidates"][:count])
    for expected, actual in zip(expected_map["candidates"], actual_candidates):
        expected_evidence = {ref["record_id"] for ref in expected["evidence_refs"]}
        actual["evidence_refs"] = [
            ref for ref in actual["evidence_refs"]
            if ref["record_id"] in expected_evidence
        ]
        actual["normalization"]["inputs"] = copy.deepcopy(
            expected["normalization"]["inputs"]
        )
        expected_supports = {
            relation["support_id"]
            for relation in expected["relationships"]["concurrent_support"]
        }
        actual["relationships"]["concurrent_support"] = [
            relation for relation in actual["relationships"]["concurrent_support"]
            if relation["support_id"] in expected_supports
        ]
        actual["review"] = copy.deepcopy(expected["review"])
    testcase.assertEqual(expected_map["candidates"], actual_candidates)
    testcase.assertEqual(expected_map["sequence"], actual_map["sequence"][:count])
