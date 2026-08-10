"""Small helpers for the reviewed A1 final-decision catalog."""


def cid(short_id: str) -> str:
    return f"lesson_candidate.{short_id}"


def owner_id(value: str) -> str:
    return value if "." in value else cid(value)


def decision(short_id: str, code: str, owners: tuple[str, ...], rationale: str,
             outcome: str | None = None, mastery: str | None = None) -> dict:
    roles = {
        "keep": "learner_lesson", "revise": "learner_lesson", "merge": "merged_source",
        "support_only": "cross_cutting_support", "split": "split_source",
    }
    final_owners = [owner_id(item) for item in owners]
    return {
        "candidate_id": cid(short_id),
        "decision": code,
        "architecture_role": roles[code],
        "survives_as_learner_lesson": code in ("keep", "revise"),
        "final_owner_ids": final_owners,
        "primary_transfer_owner_id": final_owners[0],
        "rationale": rationale,
        "revised_outcome_statement": outcome,
        "mastery_action": mastery or (
            "Retain the current fresh mastery construct." if code == "keep"
            else "Assess the capability under its named final owner, not as a separate lesson."
        ),
    }


def keep(short_id: str, rationale: str) -> dict:
    return decision(short_id, "keep", (short_id,), rationale)


def revise(short_id: str, rationale: str, outcome: str, mastery: str) -> dict:
    return decision(short_id, "revise", (short_id,), rationale, outcome, mastery)
