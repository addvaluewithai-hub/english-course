def evidence(role: str, video_anchor: str, activity_ids: list[str], mastery_use: str) -> dict:
    return {
        "role": role,
        "video_anchor": video_anchor,
        "post_video_activity_ids": activity_ids,
        "mastery_evidence": mastery_use,
    }
