"""Combined exact A1 pronunciation target catalog."""

from scripts.a1_pronunciation_targets_01_sounds import TARGETS as SOUNDS
from scripts.a1_pronunciation_targets_02_word_form import TARGETS as WORD_FORM
from scripts.a1_pronunciation_targets_03_chunks import TARGETS as CHUNKS


TARGETS = SOUNDS + WORD_FORM + CHUNKS
