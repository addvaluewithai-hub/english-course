#!/usr/bin/env python3
"""A1 U1-L02 scoped editorial regression checks — NOT a learning/release pass."""
from __future__ import annotations
import copy
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFT = ROOT / 'interactive-content-production/drafts/A1/U1-L02/LESSON-v01.CANDIDATE.json'
COVERAGE = ROOT / 'interactive-content-production/coverage/A1/U1-L02.json'
LEDGER = ROOT / 'curriculum/levels/a1/design-review/06-coverage-ledger/generated/coverage-ledger.json'
WORDS = ROOT / 'curriculum/levels/a1/semantic-lock/word-control-decisions.json'
PHRASES = ROOT / 'curriculum/levels/a1/semantic-lock/phrase-control-decisions.json'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

class A1U1L02Editorial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lesson,cls.mapping,cls.ledger,cls.words,cls.phrases=map(read,(DRAFT,COVERAGE,LEDGER,WORDS,PHRASES))

    def test_exact_29_source_rows_and_semantic_roles(self):
        items={x['item_id']:x for x in self.ledger['records'] if 'U1-L02' in x['lifecycle']['introduce']}
        proposed=self.mapping['items']
        self.assertEqual(len(proposed),len(items))
        self.assertEqual(len(items),29)
        self.assertEqual({x['sourceId'] for x in proposed},set(items))
        role={id:g['semantic_role'] for g in self.phrases['role_groups'] for id in g['item_ids']}
        for row in proposed:
            src=items[row['sourceId']]
            self.assertEqual((row['category'],row['label']),(src['category'],src['label']))
            expected=(role.get(src['item_id']) if src['category']=='phrase' else
                      self.words['default_pending_role']['semantic_role'] if src['category']=='word' else
                      'role_requires_explicit_pedagogical_decision')
            self.assertEqual(row['semanticRole'],expected)
            self.assertGreaterEqual(len(row['rationale'].strip()),30)
            self.assertNotEqual(row['approvalRef'],'auto-approved')
        groups={k:len([x for x in proposed if x['category']==k]) for k in ('ability','phrase','grammar','word','pronunciation')}
        self.assertEqual(groups,dict(ability=4,phrase=1,grammar=2,word=21,pronunciation=1))

    def test_13_undeclared_semantic_homes_cannot_be_claimed_taught(self):
        escalated=[x for x in self.mapping['items'] if x['disposition']=='escalate']
        self.assertEqual(len(escalated),13)
        self.assertEqual({x['label'] for x in escalated},
                         set('all because else every his let mile of quarter somebody they we will'.split()))
        self.assertTrue(all(x['review']=='needs-review' and not x['evidence'] for x in escalated))
        self.assertEqual(self.lesson['sourceOwnerGates'],13)
        self.assertFalse(self.lesson['dialogue']['approvedForPaidAudio'])
        self.assertNotEqual(self.mapping['qualityGates']['ownerAcceptance'],'accepted')

    def test_eight_turns_and_20_authored_focus_first_boards(self):
        turns=self.lesson['dialogue']['turns']
        self.assertEqual(len(turns),8)
        self.assertEqual([x['id'] for x in turns],[f't{i:02}' for i in range(1,9)])
        self.assertEqual(self.lesson['dialogue']['wordCount'],
                         sum(len(x['text'].split()) for x in turns))
        text=' '.join(x['text'] for x in turns)
        for target in ('How old are you?','nineteen years old','What about you?','twenty-one'):
            self.assertIn(target,text)
        self.assertNotIn('mile',text)
        self.assertNotIn('quarter',text)
        self.assertEqual(len(self.lesson['scenes']),7)
        beats=[(scene['id'],b) for scene in self.lesson['scenes'] for b in scene['beats']]
        self.assertEqual(len(beats),20)
        self.assertEqual(len({x[0]+'/'+x[1]['id'] for x in beats}),20)
        for _,b in beats:
            self.assertTrue(b['teacherSpeechAr'].strip())
            self.assertTrue(b['boardStateId'].strip())
            self.assertTrue(b['board']['head'].strip())
            self.assertTrue(b['board']['relationship'].strip())
        targets={(scene_id,b['id']) for scene_id,b in beats}
        for row in self.mapping['items']:
            for e in row['evidence']:
                self.assertIn((e['sceneId'],e['beatId']),targets)
                self.assertTrue(e.get('plannedNotObserved'))

    def test_six_real_mc_branches_balanced_and_no_gist_leak(self):
        qs=[s['assessment'] for s in self.lesson['scenes'] if s['assessment']['kind']=='deterministic-mc']
        self.assertEqual(len(qs),6)
        positions=[]
        for q in qs:
            ids=[x['id'] for x in q['options']]
            self.assertEqual(len(ids),len(set(ids)))
            self.assertEqual(len(ids),3)
            self.assertIn(q['correctId'],ids)
            self.assertTrue(q['correctFeedbackAr'] and q['wrongFeedbackAr'])
            self.assertTrue(q['answerHiddenBeforeAttempt'])
            self.assertTrue(all(o['misconception'] for o in q['options']))
            positions.append(ids.index(q['correctId']))
        self.assertEqual(positions,[1,0,2,0,2,1])
        first=self.lesson['scenes'][0]
        self.assertEqual(first['id'],'listen-first')
        before=first['beats'][0]['teacherSpeechAr']+' '+str(first['beats'][0]['board'])
        for spoiler in ('class card','age','nineteen','بيكتبوا','كلاس','سن'):
            self.assertNotIn(spoiler,before.lower())
        age=next(s for s in self.lesson['scenes'] if s['id']=='age-meaning')
        self.assertEqual(age['assessment']['id'],'q-age-listening')
        self.assertTrue(age['assessment']['evidence']['requireAudio'])
        self.assertEqual(age['assessment']['correctId'],'19')

    def test_phone_message_real_audio_gate_and_word_stress(self):
        msg=self.lesson['supplementaryRecordedMessage']
        self.assertEqual(''.join(msg['spokenDigits']),'50268368')
        self.assertEqual(msg['status'],'SCRIPT_ONLY_NOT_RECORDED')
        self.assertTrue(msg['playbackRequiresActualAuditedWAV'])
        phone=next(s for s in self.lesson['scenes'] if s['id']=='voicemail')
        self.assertEqual(phone['assessment']['correctId'],'68')
        self.assertTrue(phone['assessment']['evidence']['mustUseActualRecordedMessage'])
        self.assertTrue(any(b.get('requireSeparateRecordedVoice') for b in phone['beats']))
        stress=next(s for s in self.lesson['scenes'] if s['id']=='number-patterns')
        actual=' '.join(b['teacherSpeechAr'] for b in stress['beats'])
        self.assertIn('thirTEEN',actual)
        self.assertIn('THIRty',actual)
        for clip in self.lesson['clips']:
            self.assertIsNone(clip['startMs'])
            self.assertIsNone(clip['endMs'])
            self.assertFalse(clip['approved'])
        self.assertEqual(self.lesson['qualityGates']['sourceWav'],'NOT_COMMISSIONED')
        self.assertEqual(self.lesson['qualityGates']['phoneMessageWav'],'NOT_COMMISSIONED')

    def test_locked_phrase_production_not_fake_listen_completion(self):
        final=self.lesson['scenes'][-1]
        self.assertEqual(final['id'],'fresh-speaking')
        self.assertEqual(final['assessment']['kind'],'gemini-live-speaking')
        self.assertIn('oxford.phrase.online.0748',
                      [x['sourceId'] for x in final['assessment']['sourcePhraseEvidence']])
        self.assertIn('okay only',final['assessment']['falsePassExamples'])
        self.assertTrue(all(g!='accepted' for g in self.mapping['qualityGates'].values()))

if __name__=='__main__':
    unittest.main()
