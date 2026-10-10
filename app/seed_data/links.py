"""Further-reading links for the example entries. Every URL was checked live
(scripts/check_seed_sources.py); add new ones only after running that check."""


def medlineplus(slug: str, topic: str) -> dict[str, str]:
    return {
        "label": f"MedlinePlus (NIH, englisch): {topic}",
        "url": f"https://medlineplus.gov/{slug}.html",
    }


def who(slug: str, topic: str) -> dict[str, str]:
    return {
        "label": f"WHO-Faktenblatt (englisch): {topic}",
        "url": f"https://www.who.int/news-room/fact-sheets/detail/{slug}",
    }


def gesundheit_gv(path: str, topic: str) -> dict[str, str]:
    return {
        "label": f"Gesundheitsportal Österreich: {topic}",
        "url": f"https://www.gesundheit.gv.at/krankheiten/{path}.html",
    }
