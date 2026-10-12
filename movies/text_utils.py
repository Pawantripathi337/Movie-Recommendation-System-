"""
Small text-cleaning helpers (no pandas, no Django needed).
They are used by the preprocessing pipeline AND by the Movie model.
"""
import re


def clean_text(text):
    """
    Make text simple for the computer:
      1. convert to lowercase        ("Avengers!" -> "avengers!")
      2. remove special characters   ("avengers!" -> "avengers")
      3. remove extra spaces
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # keep only letters, digits and spaces
    return re.sub(r"\s+", " ", text).strip()


def squash(name):
    """
    Join a multi-word name into ONE token so it is not split later.
    "Sam Worthington" -> "samworthington"  (so two different 'Sam's don't look similar)
    "Science Fiction" -> "sciencefiction"
    """
    return clean_text(name).replace(" ", "")


def build_tags(overview, genres, keywords, cast, director):
    """
    Combine all useful text of ONE movie into a single 'tags' string.
      overview  : text (cleaned, normal words)
      genres    : list of names   -> each name becomes one token
      keywords  : list of names   -> cleaned, normal words
      cast      : list of names   -> each name becomes one token
      director  : text            -> one token
    """
    parts = [clean_text(overview)]
    parts += [squash(g) for g in genres]
    parts += [clean_text(k) for k in keywords]
    parts += [squash(c) for c in cast]
    parts.append(squash(director))
    return " ".join(p for p in parts if p)
