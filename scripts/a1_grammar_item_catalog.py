"""Combined reviewed A1 grammar item catalog."""

from scripts.a1_grammar_items_01_foundations import ITEMS as FOUNDATIONS
from scripts.a1_grammar_items_02_verbs_time import ITEMS as VERBS_TIME
from scripts.a1_grammar_items_03_nouns_modifiers import ITEMS as NOUNS_MODIFIERS
from scripts.a1_grammar_items_04_linking_location import ITEMS as LINKING_LOCATION


ITEMS = FOUNDATIONS + VERBS_TIME + NOUNS_MODIFIERS + LINKING_LOCATION
