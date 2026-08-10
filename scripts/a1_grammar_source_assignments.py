"""Combined source-disposition catalogs for A1 grammar."""

from scripts.a1_grammar_egp_assignments_01 import ASSIGNMENTS as EGP_01
from scripts.a1_grammar_egp_assignments_02 import ASSIGNMENTS as EGP_02
from scripts.a1_grammar_gse_assignments import ASSIGNMENTS as GSE


EGP_ASSIGNMENTS = EGP_01 + EGP_02
GSE_ASSIGNMENTS = GSE
