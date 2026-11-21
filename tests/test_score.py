from datetime import datetime, timezone

import pandas as pd

from jobhunt.cli import keywords_report, rank
from jobhunt.score import Job, Profile, parse_min_years, score
from jobhunt.sources import normalize_sites

P = Profile(skills=("java", "spring boot", "kafka", "aws"), years=3)


def test_fresh_matching_junior_job_scores_high():
    s, d = score(Job("Java Developer", "Java, Spring Boot, Kafka on AWS. 2-4 years", hours_old=5,
                     easy_apply=True, salary_shown=True), P)
    assert d["matched_skills"] == ["java", "spring boot", "kafka", "aws"]
    assert s == 30 + 30 + 15 + 10 + 5 + 0 + 5


def test_senior_old_job_scores_low():
    s, _ = score(Job("Senior Java Architect", "Java. 8+ years", hours_old=400), P)
    assert s < 20


def test_skill_match_is_word_bounded():
    _, d = score(Job("JavaScript Developer", "javascript only"), P)
    assert "java" not in d["matched_skills"]


def test_parse_min_years():
    assert parse_min_years("Need 3-5 years of experience") == 3
    assert parse_min_years("5+ yrs") == 5
    assert parse_min_years("no number here") is None


def test_browser_only_site_rejected():
    try:
        normalize_sites(["wellfound"])
    except ValueError as e:
        assert "profile-optimizer" in str(e)
    else:
        raise AssertionError("expected ValueError")


def test_rank_orders_and_dedupes():
    now = datetime(2026, 11, 21, tzinfo=timezone.utc)
    df = pd.DataFrame([
        {"site": "indeed", "title": "Java Developer", "company": "A", "description": "java spring boot kafka aws",
         "date_posted": "2026-11-21", "job_url_direct": None},
        {"site": "linkedin", "title": "Java Developer", "company": "A", "description": "dup",
         "date_posted": "2026-11-21", "job_url_direct": None},
        {"site": "naukri", "title": "Lead Engineer", "company": "B", "description": "php",
         "date_posted": "2026-10-01", "job_url_direct": "https://b.example/apply"},
    ])
    out = rank(df, P, now)
    assert list(out["company"]) == ["A", "B"]
    assert out.iloc[0]["callback_score"] > out.iloc[1]["callback_score"]


def test_keywords_report_counts():
    df = pd.DataFrame([{"title": "Java dev", "description": "Kafka and AWS"}, {"title": "Java", "description": "Docker"}])
    assert dict(keywords_report(df))["java"] == 2
