from scripts.pilot10_specs.u1_l01 import SPEC as U1_L01
from scripts.pilot10_specs.u1_l02 import SPEC as U1_L02
from scripts.pilot10_specs.u1_l04 import SPEC as U1_L04
from scripts.pilot10_specs.u1_l05 import SPEC as U1_L05
from scripts.pilot10_specs.u1_l06 import SPEC as U1_L06
from scripts.pilot10_specs.u1_l07 import SPEC as U1_L07
from scripts.pilot10_specs.u1_l08 import SPEC as U1_L08
from scripts.pilot10_specs.u1_l09 import SPEC as U1_L09
from scripts.pilot10_specs.u2_l01 import SPEC as U2_L01
from scripts.pilot10_specs.coverage_u1_01_04 import COVERAGE as COVERAGE_01_04
from scripts.pilot10_specs.coverage_u1_05_07 import COVERAGE as COVERAGE_05_07
from scripts.pilot10_specs.coverage_u1_08_u2 import COVERAGE as COVERAGE_08_U2


SPECS = {
    spec["lesson_id"]: spec
    for spec in (
        U1_L01,
        U1_L02,
        U1_L04,
        U1_L05,
        U1_L06,
        U1_L07,
        U1_L08,
        U1_L09,
        U2_L01,
    )
}

for coverage_group in (COVERAGE_01_04, COVERAGE_05_07, COVERAGE_08_U2):
    for lesson_id, target_coverage in coverage_group.items():
        SPECS[lesson_id]["target_coverage"] = target_coverage
