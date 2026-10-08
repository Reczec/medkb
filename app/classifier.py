"""Rule-based classification and keyword extraction for German medical text.

How it works (kept deliberately simple and explainable):

1. Every medical category has a vocabulary of word stems with a weight (1 = general term,
   2 = specific term). A stem is matched anywhere in the lower-cased text, so compound words
   like "Rückenschmerzen" or "Vernichtungskopfschmerz" are found. A leading "^" restricts the
   match to the start of a word (to avoid false hits such as "Drachen" for "rachen").
2. Score per category = sum over stems of weight * hits, where hits are the occurrences in the
   content (capped, so repetition cannot dominate) plus a bonus if the stem is in the title.
3. The category with the highest score wins. Below MIN_SCORE (or without any hit) the entry
   falls back to "Allgemeinmedizin". Ties go to the more specific category.
4. Keywords are the real words from the text that contain the matched stems (most important
   first), topped up with frequent nouns.

This is a classical keyword/scoring approach, not machine learning. It is transparent and has
no dependencies, but it cannot understand context or negation ("kein Fieber").
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

DEFAULT_CATEGORY = "Allgemeinmedizin"
MIN_SCORE = 3
MAX_KEYWORDS = 8
TITLE_BONUS_HITS = 2  # a stem in the title counts like two extra occurrences
MAX_COUNTED_OCCURRENCES = 3  # per stem, in the content

# Category -> {stem: weight}. Order matters for ties: specific categories first,
# the general fallback category last.
# fmt: off
VOCABULARY: dict[str, dict[str, int]] = {
    "HNO": {
        "tinnitus": 2, "ohrgeräusch": 2, "ohrenschmerz": 2, "ohrensausen": 2, "hörsturz": 2,
        "hörverlust": 2, "schwerhörig": 1, "mittelohr": 2, "otitis": 2, "trommelfell": 2,
        "gehörgang": 2, "nasenbluten": 1, "nasennebenhöhl": 2, "sinusitis": 2, "rhinitis": 2,
        "schnupfen": 1, "^rachen": 1, "pharyngitis": 2, "mandel": 1, "tonsill": 2,
        "kehlkopf": 2, "laryngitis": 2, "heiserkeit": 1, "stimmband": 2, "halsschmerz": 1,
        "schluckbeschwerd": 1, "geruchssinn": 1, "polypen": 1, "^hno": 2,
    },
    "Neurologie": {
        "kopfschmerz": 1, "migräne": 2, "epilepsie": 2, "krampfanfall": 2, "schlaganfall": 2,
        "lähmung": 1, "taubheitsgefühl": 1, "kribbeln": 1, "parkinson": 2,
        "multiple sklerose": 2, "demenz": 2, "alzheimer": 2, "neuropath": 2, "nerven": 1,
        "gedächtnis": 1, "sprachstörung": 1, "sehstörung": 1, "schwindel": 1, "tremor": 1,
        "bewusstlos": 1, "meningitis": 2, "hirn": 1, "gangunsicherheit": 1, "neurolog": 2,
    },
    "Innere Medizin": {
        "diabetes": 2, "blutzucker": 2, "insulin": 2, "hba1c": 2, "stoffwechsel": 1,
        "cholesterin": 1, "schilddrüse": 2, "hashimoto": 2, "^magen": 1, "^darm": 1,
        "sodbrennen": 2, "reflux": 2, "speiseröhre": 1, "gastritis": 2, "durchfall": 1,
        "verstopfung": 1, "übelkeit": 1, "erbrechen": 1, "bauchschmerz": 1, "^leber": 1,
        "^gallen": 1, "^niere": 1, "pankreas": 1, "colitis": 2, "crohn": 2, "anämie": 2,
        "eisenmangel": 2, "^gicht": 1, "asthma": 2, "bronchitis": 2, "lungenentzündung": 2,
        "pneumonie": 2, "^copd": 2,
    },
    "Kardiologie": {
        "herzinfarkt": 2, "herzrasen": 2, "herzklopfen": 1, "herzrhythm": 2,
        "herzinsuffizienz": 2, "herzschwäche": 2, "herzklappe": 2, "herzschmerz": 1,
        "herzfrequenz": 1, "vorhofflimmern": 2, "angina pectoris": 2, "brustschmerz": 1,
        "bluthochdruck": 2, "hypertonie": 2, "hypotonie": 1, "blutdruck": 1, "ekg": 2,
        "koronar": 2, "arteriosklerose": 2, "thrombose": 1, "embolie": 1, "kardio": 2,
        "^herz": 1,
    },
    "Dermatologie": {
        "hautausschlag": 2, "ausschlag": 1, "juckreiz": 1, "ekzem": 2, "neurodermitis": 2,
        "psoriasis": 2, "schuppenflechte": 2, "^akne": 2, "nesselsucht": 2, "urtikaria": 2,
        "melanom": 2, "muttermal": 1, "gürtelrose": 2, "^herpes": 1, "sonnenbrand": 1,
        "dermat": 2, "^haut": 1, "pilzinfektion": 1, "krätze": 2, "hautarzt": 2,
    },
    "Orthopädie": {
        "knochen": 1, "knochenbruch": 2, "fraktur": 2, "gelenk": 1, "arthrose": 2,
        "arthritis": 2, "rückenschmerz": 2, "bandscheibe": 2, "hexenschuss": 2,
        "knieschmerz": 2, "schulterschmerz": 2, "hüftgelenk": 2, "osteoporose": 2,
        "^sehnen": 1, "meniskus": 2, "kreuzband": 2, "wirbelsäule": 2, "skoliose": 2,
        "muskel": 1, "muskul": 1, "verstauchung": 2, "prellung": 1, "fersensporn": 2,
        "karpaltunnel": 2, "orthopäd": 2, "knorpel": 1,
    },
    "Pädiatrie": {
        "säugling": 2, "kleinkind": 2, "^kinder": 1, "kindesalter": 1, "neugeboren": 2,
        "^baby": 1, "pädiat": 2, "kinderarzt": 2, "masern": 2, "windpocken": 2, "röteln": 2,
        "mumps": 2, "scharlach": 2, "keuchhusten": 2, "dreitagefieber": 2, "^krupp": 2,
        "kinderkrankheit": 2, "wachstumsstörung": 1, "entwicklungsverzögerung": 2,
        "schreibaby": 2,
    },
    "Psychiatrie": {
        "depress": 2, "antriebslos": 1, "stimmung": 1, "angststörung": 2, "panikattacke": 2,
        "panik": 1, "burnout": 2, "schizophren": 2, "psychose": 2, "bipolar": 2,
        "zwangsstörung": 2, "posttraumatisch": 2, "suizid": 2, "essstörung": 2, "anorexie": 2,
        "bulimie": 2, "^adhs": 2, "psychisch": 2, "psychiat": 2, "psychotherap": 2,
        "halluzination": 2, "wahnvorstellung": 2, "schlafstörung": 1,
    },
    DEFAULT_CATEGORY: {
        "erkältung": 1, "grippal": 1, "grippe": 1, "infekt": 1, "fieber": 1, "husten": 1,
        "halskratzen": 1, "müdigkeit": 1, "abgeschlagen": 1, "vorsorge": 1, "impfung": 1,
        "impfplan": 1, "allgemeinbefinden": 1, "gliederschmerz": 1, "hausarzt": 1,
        "allgemeinmedizin": 2,
    },
}
# fmt: on

CATEGORIES: list[str] = list(VOCABULARY)

_WORD_RE = re.compile(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß-]*[A-Za-zÄÖÜäöüß]")
_WORD_START = r"(?<![a-zäöüß])"

# Frequent but uninformative nouns that should not become keywords on their own.
_GENERIC_WORDS = frozenset(
    """
    beschwerden betroffene betroffener untersuchung untersuchungen behandlung erkrankung
    erkrankungen patienten patient symptome ursachen ursache zusätzlich besonders wichtig
    medikamente häufig meistens regelmäßig bedarf verlauf verläufe empfohlen
    """.split()
)


@dataclass(frozen=True)
class _Rule:
    category: str
    stem: str
    weight: int
    pattern: re.Pattern[str]


def _compile_rules() -> tuple[_Rule, ...]:
    rules: list[_Rule] = []
    for category, terms in VOCABULARY.items():
        for raw, weight in terms.items():
            word_start = raw.startswith("^")
            stem = raw.lstrip("^")
            prefix = _WORD_START if word_start else ""
            rules.append(_Rule(category, stem, weight, re.compile(prefix + re.escape(stem))))
    return tuple(rules)


_RULES = _compile_rules()


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    confidence: float  # share of the winning score in the total score, 0.0 on fallback
    fallback: bool  # True if no category reached MIN_SCORE
    scores: dict[str, int]  # only categories with a score > 0, best first
    matched_terms: list[str]  # stems that triggered, most important first
    keywords: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def classify(title: str, content: str) -> ClassificationResult:
    """Suggest a category and keywords for a document."""
    title_n = _normalize(title)
    content_n = _normalize(content)

    scores: dict[str, int] = {category: 0 for category in VOCABULARY}
    hit_rules: list[tuple[_Rule, int]] = []

    for rule in _RULES:
        content_hits = min(len(rule.pattern.findall(content_n)), MAX_COUNTED_OCCURRENCES)
        title_hits = TITLE_BONUS_HITS if rule.pattern.search(title_n) else 0
        hits = content_hits + title_hits
        if hits:
            scores[rule.category] += rule.weight * hits
            hit_rules.append((rule, hits))

    # First maximum wins, so earlier (more specific) categories win ties.
    best_category, best_score = DEFAULT_CATEGORY, 0
    for category, score in scores.items():
        if score > best_score:
            best_category, best_score = category, score

    fallback = best_score < MIN_SCORE
    category = DEFAULT_CATEGORY if fallback else best_category
    total = sum(scores.values())
    confidence = 0.0 if fallback or total == 0 else round(best_score / total, 2)

    hit_rules.sort(key=lambda rh: (rh[0].category != category, -rh[0].weight, -rh[1]))
    ranked_stems = [rule.stem for rule, _ in hit_rules]

    return ClassificationResult(
        category=category,
        confidence=confidence,
        fallback=fallback,
        scores=dict(sorted(((c, s) for c, s in scores.items() if s > 0), key=lambda kv: -kv[1])),
        matched_terms=ranked_stems,
        keywords=_extract_keywords(f"{title}\n{content}", ranked_stems),
    )


def _extract_keywords(text: str, ranked_stems: list[str]) -> list[str]:
    tokens = _WORD_RE.findall(text)
    counts = Counter(token.lower() for token in tokens)
    first_form: dict[str, str] = {}
    for token in tokens:
        first_form.setdefault(token.lower(), token)

    keywords: list[str] = []
    seen: set[str] = set()

    def add(word: str) -> bool:
        key = word.lower()
        if key not in seen:
            seen.add(key)
            keywords.append(word)
        return len(keywords) >= MAX_KEYWORDS

    # 1) The actual words that triggered a rule (one form per stem, most frequent form).
    for stem in ranked_stems:
        if " " in stem:
            if add(stem.title()):
                return keywords
            continue
        forms = [word for word in counts if stem in word]
        if forms:
            best = min(forms, key=lambda word: (-counts[word], word))
            if add(first_form[best]):
                return keywords

    # 2) Top up with frequent, capitalised (noun-like) words.
    candidates = [
        word
        for word, count in counts.items()
        if count >= 2
        and len(word) >= 7
        and word not in _GENERIC_WORDS
        and first_form[word][0].isupper()
    ]
    for word in sorted(candidates, key=lambda w: (-counts[w], w)):
        if add(first_form[word]):
            break
    return keywords
