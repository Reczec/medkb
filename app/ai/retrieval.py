"""Bounded lexical normalization for questions and topic-preserving followups."""

import re

from sqlalchemy.orm import Session

from app.ai.schemas import AskRequest
from app.models import Document
from app.services import search_documents

MAX_ENTRIES = 5

QUESTION_WORDS = frozenset(
    "was wie warum wann wo wer welche welcher welches ist sind ein eine einer einem einen "
    "der die das den dem des von zu zur zum und oder bei für mit ohne nach als es sie er "
    "ich man mir mich kann können wird werden hat haben gibt tun bitte erkläre erklären "
    "diese dieser dieses dazu dabei dagegen davon symptome symptom ursachen ursache "
    "warnzeichen therapie behandlung behandelt behandeln diagnostik diagnostiziert "
    # everyday question verbs and fillers ("Was hilft gegen …", "was soll ich machen")
    "hilft helfen hilfe gegen soll sollte sollen muss müssen darf dürfen machen mache macht "
    "tun tue kommt bekomme bekommt habe hast gut gute besser schnell am im in auf an "
    "mein meine meinem meinen dein deine wenn weil denn noch auch so sehr viel "
    # English question words and fillers (entries also contain their section names)
    "what which who whom whose when where why how is are was were be been am do does did "
    "a an the of to in on at by for with without from about against and or not no it its "
    "this that these those there here i me my we our you your he she they them can could "
    "should would will shall may might must have has had get gets got help helps helping "
    "treat treats treated treating tell please explain give need needs want symptoms symptom "
    "cause causes therapy treatment diagnostics definition "
    "diagnose diagnosed diagnosis diagnostic".split()
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


def find(db: Session, body: AskRequest) -> list[Document]:
    """Entries for the question: all terms must match; if no entry has them all, the entries
    with the best partial match. A term found in few entries weighs more than a common one,
    so an unknown extra word or a vague one ("gefährlich") cannot hide the obvious entry."""
    q = query(body)
    if not q:
        return []
    documents, _ = search_documents(db, q=q, limit=MAX_ENTRIES)
    if documents or " " not in q:
        return list(documents)
    score: dict[int, float] = {}
    by_id: dict[int, Document] = {}
    for term in q.split():
        matches, total = search_documents(db, q=term, limit=MAX_ENTRIES)
        for document in matches:
            titles = (document.title, document.title_en or "")
            in_title = 2 if any(term in title.lower() for title in titles) else 1  # like the search
            score[document.id] = score.get(document.id, 0.0) + in_title / total
            by_id.setdefault(document.id, document)
    # sorted() is stable: equal scores keep the search's own ranking order.
    ranked = sorted(score, key=lambda doc_id: -score[doc_id])
    return [by_id[doc_id] for doc_id in ranked[:MAX_ENTRIES]]
