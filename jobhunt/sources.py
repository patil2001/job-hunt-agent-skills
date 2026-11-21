"""Fetch recent postings. Uses JobSpy (https://github.com/speedyapply/JobSpy) for the sites it supports.

Sites without a stable public scraper (Wellfound, Instahyre, foundit, hirist, Cutshort, Dice) are covered by the
browser-driven skills in skills/<site>-profile-optimizer instead; asking for them here raises a clear error.
"""
from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

from .score import Job

JOBSPY_SITES = ("linkedin", "indeed", "glassdoor", "zip_recruiter", "google", "naukri")
BROWSER_ONLY = ("wellfound", "instahyre", "foundit", "hirist", "cutshort", "dice")
ALIASES = {"ziprecruiter": "zip_recruiter"}


def normalize_sites(sites: list[str]) -> list[str]:
    out = []
    for s in sites:
        s = ALIASES.get(s.lower(), s.lower())
        if s in BROWSER_ONLY:
            raise ValueError(f"{s}: no scraper; use the {s}-profile-optimizer skill (browser) instead")
        if s not in JOBSPY_SITES:
            raise ValueError(f"unknown site {s!r}; supported: {', '.join(JOBSPY_SITES)}")
        out.append(s)
    return out


def fetch(sites: list[str], role: str, location: str, hours: int, per_site: int, country: str) -> pd.DataFrame:
    from jobspy import scrape_jobs  # imported here so scoring/tests don't need network deps

    return scrape_jobs(
        site_name=normalize_sites(sites),
        search_term=role,
        google_search_term=f"{role} jobs near {location} since yesterday",
        location=location,
        results_wanted=per_site,
        hours_old=hours,
        country_indeed=country,
        linkedin_fetch_description=True,
        description_format="markdown",
    )


def _hours_old(date_posted, now: datetime) -> float | None:
    if date_posted is None or (isinstance(date_posted, float) and pd.isna(date_posted)):
        return None
    d = pd.Timestamp(date_posted)
    if pd.isna(d):
        return None
    if d.tzinfo is None:
        d = d.tz_localize(timezone.utc)
    return max(0.0, (now - d.to_pydatetime()).total_seconds() / 3600)


def _txt(v) -> str:
    return "" if v is None or (isinstance(v, float) and pd.isna(v)) else str(v)


def to_job(row: dict, now: datetime) -> Job:
    url_direct = _txt(row.get("job_url_direct"))
    salary = any(_txt(row.get(k)) for k in ("min_amount", "max_amount"))
    exp = _txt(row.get("experience_range"))  # naukri only
    min_years = None
    if exp:
        head = exp.split("-")[0].strip().split()[0]
        min_years = float(head) if head.replace(".", "").isdigit() else None
    return Job(
        title=_txt(row.get("title")),
        description=f"{_txt(row.get('description'))}\n{_txt(row.get('skills'))}",
        hours_old=_hours_old(row.get("date_posted"), now),
        easy_apply=not url_direct,  # no external redirect => applies in-platform
        direct=bool(url_direct) and "linkedin" not in url_direct and "indeed" not in url_direct,
        salary_shown=salary,
        min_years=min_years,
    )
