#!/usr/bin/env python3
"""Clean-room onboarding smoke test (static simulation, NOT an independent agent run).

Proves a fresh process can locate source, choose in-flight lesson, and fail closed
on unresolved coverage. Does not prove a humanless new agent can teach correctly.
"""
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
script=ROOT/"interactive-content-production/tools/production_status.py"
spec=importlib.util.spec_from_file_location("production_status",script)
queue=importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)


class ColdAgentHandoffTest(unittest.TestCase):
    def test_six_status_files_are_source_aligned(self):
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            queue.validate()
        data=json.loads(captured.getvalue())
        self.assertEqual({x: data['levels'][x]['lessons'] for x in ['A1','A2','B1','B2']},
                         {'A1':62,'A2':83,'B1':85,'B2':95})

    def test_a_fresh_agent_stops_on_an_active_earlier_lesson(self):
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            queue.next_lesson("A1")
        data=json.loads(captured.getvalue())
        self.assertEqual(data['state'],'IN_FLIGHT_REVIEW')
        self.assertEqual(data['lesson']['id'],'U1-L01')
        self.assertEqual(data['lesson']['status'],'in-progress')
        self.assertIn('/englishlive/pull/54',data['lesson']['evidence'])
        self.assertFalse(data['delivery_authorized_in_manifest'])

    def test_coverage_is_structurally_valid_but_release_is_deliberately_blocked(self):
        tool=ROOT/'interactive-content-production/tools/coverage_gate.py'
        check=subprocess.run([sys.executable,str(tool),'check','A1','U1-L01'],
                             capture_output=True,text=True,check=True)
        data=json.loads(check.stdout)
        self.assertTrue(data['structuralValid'])
        self.assertEqual(data['canonicalItems'],36)
        self.assertFalse(data['ready'])
        self.assertGreaterEqual(len(data['blockers']),12)
        ready=subprocess.run([sys.executable,str(tool),'ready','A1','U1-L01'],
                             capture_output=True,text=True)
        self.assertNotEqual(ready.returncode,0)
        self.assertIn('NOT READY',ready.stderr)

    def test_all_registered_coverage_runs_not_only_hardcoded_A1(self):
        tool=ROOT/'interactive-content-production/tools/coverage_gate.py'
        result=subprocess.run([sys.executable,str(tool),'check-all'],
                              capture_output=True,text=True,check=True)
        # Every registered level/lesson coverage file must be checked; adding
        # U1-L02 must not require incrementing a hard-coded single-lesson count.
        expected_count=len(list((ROOT/'interactive-content-production/coverage').glob('*/*.json')))
        self.assertGreaterEqual(expected_count,2)
        marker=result.stdout.rfind('{"coverageMapsChecked":')
        self.assertGreaterEqual(marker,0, "missing final aggregate coverage audit")
        summary=json.loads(result.stdout[marker:].strip())
        self.assertEqual(summary['coverageMapsChecked'],expected_count)
        self.assertEqual(summary['structuralResult'],'PASS')
        self.assertIn('"lessonId": "U1-L02"',result.stdout)

    def test_source_and_review_gates_are_discoverable(self):
        instructions=(ROOT/'interactive-content-production/AGENTS.md').read_text()
        self.assertIn('coverage_gate.py check',instructions)
        self.assertIn('IN_FLIGHT_REVIEW',instructions)
        self.assertIn('gemini-tts',instructions)
        self.assertIn('FRAME_QA.md',instructions)
        spec=(ROOT/'interactive-content-production/coverage/A1/U1-L01.json')
        data=json.loads(spec.read_text())
        self.assertEqual(len(data['items']),36)
        self.assertGreater(len([i for i in data['items'] if i['review']=='needs-review']),0)
        self.assertNotEqual(data['qualityGates']['ownerAcceptance'],'accepted')


if __name__ == '__main__':
    unittest.main()
