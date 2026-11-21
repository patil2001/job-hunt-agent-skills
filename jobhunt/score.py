"""Callback-likelihood scoring. Pure functions: same job + profile in, same score out.

Signals (weights sum to 100):
  recency      30  newer postings get far more callbacks; applicant pool is small
  skill_match  30  share of your skills found in title + description
  experience   15  posting's minimum years within reach of yours
  seniority    10  title not above your level (Senior/Lead/Principal... penalised for juniors)
  easy_apply    5  one-click / direct apply path
  direct        5  direct employer link rather than an aggregator/staffing redirect
  salary        5  salary shown (employers who publish pay respond more)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

SENIOR_WORDS = ("senior", "sr.", "sr ", "lead", "principal", "staff", "architect", "manager", "head", "director", "vp")

YEARS_RE = re.compile(r"(\d{1,2})\s*(?:\+|-|to|–)?\s*(\d{1,2})?\s*(?:\+)?\s*(?:yrs?|years?)", re.I)


@dataclass(frozen=True)
class Profile:
    skills: tuple[str, ...]
    years: float
    allow_senior: bool = False


@dataclass
class Job:
    title: str
    description: str = ""
    hours_old: float | None = None
    easy_apply: bool = False
    direct: bool = False
    salary_shown: bool = False
    min_years: float | None = None
    extra: dict = field(default_factory=dict)


def recency_points(hours_old: float | None) -> float:
    if hours_old is None:
        return 10.0
    if hours_old <= 24:
        return 30.0
    if hours_old <= 72:
        return 20.0
    if hours_old <= 168:
        return 10.0
    return 0.0


def skill_match_points(text: str, skills: tuple[str, ...]) -> tuple[float, list[str]]:
    if not skills:
        return 0.0, []
    low = text.lower()
    hits = [s for s in skills if re.search(r"(?<![a-z0-9])" + re.escape(s.lower()) + r"(?![a-z0-9])", low)]
    return 30.0 * len(hits) / len(skills), hits


def parse_min_years(text: str) -> float | None:
    m = YEARS_RE.search(text or "")
    return float(m.group(1)) if m else None


def experience_points(min_years: float | None, years: float) -> float:
    if min_years is None:
        return 10.0
    gap = min_years - years
    if gap <= 0:
        return 15.0
    if gap <= 1:
        return 8.0
    return 0.0


def seniority_points(title: str, allow_senior: bool) -> float:
    if allow_senior:
        return 10.0
    t = f" {title.lower()} "
    return 0.0 if any(w in t for w in SENIOR_WORDS) else 10.0


def score(job: Job, profile: Profile) -> tuple[float, dict]:
    match, hits = skill_match_points(f"{job.title}\n{job.description}", profile.skills)
    min_years = job.min_years if job.min_years is not None else parse_min_years(job.description)
    parts = {
        "recency": recency_points(job.hours_old),
        "skill_match": match,
        "experience": experience_points(min_years, profile.years),
        "seniority": seniority_points(job.title, profile.allow_senior),
        "easy_apply": 5.0 if job.easy_apply else 0.0,
        "direct": 5.0 if job.direct else 0.0,
        "salary": 5.0 if job.salary_shown else 0.0,
    }
    return round(sum(parts.values()), 1), {"parts": parts, "matched_skills": hits, "min_years": min_years}
