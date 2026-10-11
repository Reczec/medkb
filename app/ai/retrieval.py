"""Bounded lexical normalization for questions and topic-preserving followups."""

import re

from app.ai.schemas import AskRequest

QUESTION_WORDS = frozenset(
    "was wie warum wann wo wer welche welcher welches ist sind ein eine einer einem einen "
    "der die das den dem des von zu zur zum und oder bei für mit ohne nach als es sie er "
    "ich man mir mich kann können wird werden hat haben gibt tun bitte erkläre erklären "
    "diese dieser dieses dazu dabei dagegen davon symptome symptom ursachen ursache "
    "warnzeichen therapie behandlung behandelt behandeln diagnostik diagnostiziert".split()
)


def terms(text: str) -> list[str]:
    return [word for word in re.findall(r"[^\W_]+", text.lower()) if word not in QUESTION_WORDS][
        :10
    ]


def query(body: AskRequest) -> str:
    focus = terms(body.question)
    if not focus:
        for message in reversed(body.history):
            if message.role == "user" and (focus := terms(message.content)):
                break
    # Do not turn punctuation/empty generic questions into an unfiltered database dump.
    return " ".join(focus)[:200]
