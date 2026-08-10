"""Outcome-fit reviews for current A1 candidates 68-81."""

REVIEWS = {
    "lesson_candidate.agree_to_a_simple_request": ("fits_a1_boundary", "support_only_review", ["cross_cutting_support", "micro_move"], "Agreement is valid A1 interaction language but belongs inside request and task outcomes."),
    "lesson_candidate.accept_a_simple_offer": ("fits_a1_boundary", "support_only_review", ["cross_cutting_support", "micro_move"], "Offer acceptance is valid A1 interaction language but belongs inside service and social outcomes."),
    "lesson_candidate.open_and_close_a_basic_social_exchange": ("fits_a1_boundary", "standalone_plausible", [], "The full greeting-to-farewell exchange is a coherent A1 social outcome."),
    "lesson_candidate.respond_politely_to_an_introduction": ("fits_a1_boundary", "support_only_review", ["cross_cutting_support", "micro_move"], "The fixed response is essential but should be controlled inside introduction and social-exchange tasks."),
    "lesson_candidate.deliver_a_rehearsed_formal_introduction": ("fits_a1_with_scope_revision", "merge_review", ["overlap_likely", "prepared_text_support_contradiction"], "A rehearsed A1 introduction is valid, but the prepared text versus no-complete-model support rule conflicts and overlaps introducing another person."),
    "lesson_candidate.use_basic_everyday_polite_forms": ("fits_a1_boundary", "support_only_review", ["cross_cutting_support"], "Please, thanks, and apology are level-wide social control, not one real-life lesson outcome."),
    "lesson_candidate.state_how_a_simple_work_made_them_feel": ("fits_a1_with_scope_revision", "standalone_plausible", ["assessment_channel_ambiguous"], "The A1 personal response is valid, but mastery must choose spoken or written performance rather than a configured alternative."),
    "lesson_candidate.show_basic_sympathy_during_a_problem_or_disagreement": ("fits_a1_boundary", "merge_review", ["cross_cutting_support", "micro_move"], "Sympathy is valid A1 facilitation language best integrated into a simple problem or social exchange."),
    "lesson_candidate.invite_input_and_check_understanding_in_a_simple_task": ("fits_a1_with_scope_revision", "merge_review", ["compound_scope", "overlap_likely"], "The three facilitation moves fit A1 but need one bounded task owner alongside adjacent collaboration moves."),
    "lesson_candidate.show_interest_and_welcome_an_idea": ("fits_a1_boundary", "merge_review", ["cross_cutting_support", "overlap_likely"], "Welcoming an idea is useful A1 collaboration support rather than a full independent lesson alone."),
    "lesson_candidate.share_an_idea_and_ask_what_others_think": ("fits_a1_boundary", "standalone_plausible", [], "One prepared idea plus an opinion invitation creates a coherent A1 collaborative outcome."),
    "lesson_candidate.follow_short_written_everyday_instructions": ("fits_a1_boundary", "standalone_plausible", [], "Following several ordered written steps is a coherent practical A1 reception outcome."),
    "lesson_candidate.understand_outline_of_an_illustrated_short_story": ("fits_a1_boundary", "standalone_plausible", [], "Main situation and basic sequence with illustrations fit A1 leisure reading complexity."),
    "lesson_candidate.translate_simple_written_phrases_with_a_dictionary": ("fits_a1_with_scope_revision", "support_only_review", ["ambiguous_language_direction", "generic_strategy_not_context_owned"], "Dictionary-assisted mediation is valid A1 support, but language direction and a practical context must be owned elsewhere."),
}
