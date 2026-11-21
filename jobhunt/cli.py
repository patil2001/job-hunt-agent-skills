"""python -m jobhunt scrape --sites linkedin indeed naukri --role "Java Developer" --location Bangalore --skills java "spring boot" kafka --years 3"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .score import Profile, score
from .sources import JOBSPY_SITES, fetch, to_job

COMMON_SKILLS = (
    "java", "spring boot", "spring", "microservices", "kafka", "aws", "azure", "gcp", "docker", "kubernetes",
    "sql", "postgresql", "mysql", "mongodb", "redis", "rest api", "hibernate", "jpa", "python", "go", "react",
    "typescript", "javascript", "node.js", "ci/cd", "jenkins", "terraform", "graphql", "junit", "git", "linux",
)


def rank(df: pd.DataFrame, profile: Profile, now: datetime) -> pd.DataFrame:
    rows = []
    for rec in df.to_dict("records"):
        s, detail = score(to_job(rec, now), profile)
        rows.append({**rec, "callback_score": s, "matched_skills": ", ".join(detail["matched_skills"]),
                     **{f"pts_{k}": v for k, v in detail["parts"].items()}})
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = out.drop_duplicates(subset=["company", "title"]).sort_values("callback_score", ascending=False)
    return out


def keywords_report(df: pd.DataFrame, top: int = 30) -> list[tuple[str, int]]:
    c: Counter[str] = Counter()
    for text in (df.get("title", pd.Series(dtype=str)).fillna("") + " " + df.get("description", pd.Series(dtype=str)).fillna("")):
        low = text.lower()
        c.update(s for s in COMMON_SKILLS if re.search(r"(?<![a-z0-9])" + re.escape(s) + r"(?![a-z0-9])", low))
    return c.most_common(top)


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="jobhunt")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scrape", help="fetch recent postings and rank by callback likelihood")
    s.add_argument("--sites", nargs="+", default=["linkedin", "indeed", "naukri"], help=f"any of {', '.join(JOBSPY_SITES)}")
    s.add_argument("--role", required=True)
    s.add_argument("--location", required=True)
    s.add_argument("--country", default="india", help="Indeed/Glassdoor country, e.g. india, usa, uk")
    s.add_argument("--hours", type=int, default=24)
    s.add_argument("--per-site", type=int, default=30)
    s.add_argument("--skills", nargs="*", default=[])
    s.add_argument("--years", type=float, default=3)
    s.add_argument("--allow-senior", action="store_true")
    s.add_argument("--top", type=int, default=50)
    s.add_argument("--out", default="jobs.xlsx", help=".xlsx or .csv")
    s.add_argument("--keywords-report", action="store_true", help="print most frequent skills across postings")
    a = p.parse_args(argv)

    now = datetime.now(timezone.utc)
    df = fetch(a.sites, a.role, a.location, a.hours, a.per_site, a.country)
    ranked = rank(df, Profile(tuple(a.skills), a.years, a.allow_senior), now).head(a.top)
    cols = [c for c in ("callback_score", "site", "title", "company", "location", "date_posted", "matched_skills",
                        "experience_range", "min_amount", "max_amount", "job_url", "job_url_direct") if c in ranked]
    out = Path(a.out)
    (ranked[cols].to_excel if out.suffix == ".xlsx" else ranked[cols].to_csv)(out, index=False)
    print(f"{len(df)} postings fetched, {len(ranked)} ranked -> {out}")
    for r in ranked[cols].head(10).to_dict("records"):
        print(f"{r['callback_score']:5.1f}  {r['site']:<10} {str(r['title'])[:50]:<50} {r['company']}")
    if a.keywords_report:
        print("\nTop skills in these postings:")
        for k, n in keywords_report(df):
            print(f"  {n:3d}  {k}")
