"""Combined exact A1 lexical-set and chunk catalog."""

from scripts.a1_lexical_chunks_01_identity_social import ITEMS as C1
from scripts.a1_lexical_chunks_02_routines_description import ITEMS as C2
from scripts.a1_lexical_chunks_03_travel_services import ITEMS as C3
from scripts.a1_lexical_chunks_04_media_mediation import ITEMS as C4
from scripts.a1_lexical_words_01_personal_time import ITEMS as W1
from scripts.a1_lexical_words_02_routines_leisure import ITEMS as W2
from scripts.a1_lexical_words_03_home_objects import ITEMS as W3
from scripts.a1_lexical_words_04_travel_services import ITEMS as W4
from scripts.a1_lexical_words_05_health_media_tasks import ITEMS as W5
from scripts.a1_lexical_words_06_extended_core import ITEMS as W6


ITEMS = W1 + W2 + W3 + W4 + W5 + W6 + C1 + C2 + C3 + C4
