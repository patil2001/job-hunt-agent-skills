"""Generate skills/<platform>-profile-optimizer/SKILL.md from one shared method plus per-platform facts.

Run: python tools/gen_platform_skills.py
Edit PLATFORMS below, then re-run; the generated files are committed.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"

PLATFORMS = {
    "indeed": {
        "title": "Indeed",
        "region": "Global (US, UK, India, CA, AU...)",
        "profile_url": "https://profile.indeed.com/",
        "search_url": "https://www.indeed.com/jobs?q={role}&l={location}&fromage=1&sort=date",
        "recruiter_side": "Indeed Resume Search / Smart Sourcing: employers search resumes by keyword, title, location and 'last active'. Only profiles set to Public or Searchable appear.",
        "sections": [
            ("Resume visibility", "Set to Searchable (or Public). Private profiles never appear in Resume Search."),
            ("Job title / desired titles", "Exact titles from current postings (e.g. 'Backend Engineer', 'Java Developer'), up to the allowed count."),
            ("Summary", "2-3 lines: title + years + 6-8 top posting keywords + domain."),
            ("Work experience", "Bullets: action + tech + metric. Repeat key terms naturally; Indeed matches on resume text."),
            ("Skills", "Every high-frequency posting skill you actually have, each with years of experience."),
            ("Qualifications / assessments", "Take the free Indeed Assessments for your stack; 'Proficient' badges show to employers."),
            ("Job preferences", "Desired pay, job types, remote, relocation. Ready to work = on. Pay filled (blank hides you from pay-filtered searches)."),
            ("Freshness", "Recruiters filter by 'active in last 30 days'. Log in and update one field weekly."),
        ],
        "peer_study": "Indeed hides other candidates. Study instead: (a) postings — titles and 'Qualifications' lists; (b) public resumes via Google X-ray `site:indeed.com/r \"<title>\" \"<city>\"` where still indexed; (c) LinkedIn profiles of people hired into the role.",
        "apply_signal": "'Easily apply' (Indeed Apply) and 'Responsive employer' badges; postings < 24h old with 'Hiring multiple candidates' get most callbacks.",
    },
    "glassdoor": {
        "title": "Glassdoor",
        "region": "Global (strong US/UK/India)",
        "profile_url": "https://www.glassdoor.com/member/profile",
        "search_url": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={role}&locKeyword={location}&fromAge=1&sortBy=date_desc",
        "recruiter_side": "Glassdoor profile is shared with Indeed (same parent); employers mostly see it when you apply. 'Easy Apply' sends the Glassdoor profile + resume.",
        "sections": [
            ("Headline / current title", "Target title as recruiters type it."),
            ("Resume", "Upload the ATS version (single column, keyword-matched). Easy Apply attaches this."),
            ("Experience + skills", "Mirror resume; skills in posting spelling."),
            ("Job preferences", "Titles, locations, remote, salary — drives the 'Jobs for you' feed and alerts."),
            ("Company research", "Before applying, read the company's interview reviews for your role; note the questions."),
        ],
        "peer_study": "Read 'Interviews' and 'Salaries' tabs for the target role at each target company: what titles got offers, what skills interviewers probed. Fold those keywords into your profile.",
        "apply_signal": "'Easy Apply' + posted < 24h + company rating ≥ 3.5 + 'Actively hiring'.",
    },
    "wellfound": {
        "title": "Wellfound (AngelList Talent)",
        "region": "Global startups (US, India, EU, remote)",
        "profile_url": "https://wellfound.com/profile/edit/overview",
        "search_url": "https://wellfound.com/role/r/{role_slug}?remote=true",
        "recruiter_side": "Founders search candidates by role, skills, location, salary, and see 'Looking for' + 'Last active'. Startups message you directly; strong profiles get inbound.",
        "sections": [
            ("Primary role + years", "Pick the exact role taxonomy (e.g. 'Backend Engineer'); years per role drive search filters."),
            ("Bio (one-liner)", "What you build + strongest proof (metric or product)."),
            ("What I'm looking for", "Stage (seed/Series A...), company size, remote, tech — founders read this first."),
            ("Achievements", "3-5 one-line wins with numbers; founders scan for shipping velocity and ownership."),
            ("Skills", "Up to the cap, posting spelling, most in-demand first."),
            ("Salary / equity", "Fill minimums honestly; blank = excluded from filtered searches."),
            ("Links", "GitHub, portfolio, LinkedIn. Side projects weigh heavily on Wellfound."),
            ("Availability", "'Actively looking' + 'Ready to interview' — re-confirm weekly so 'Last active' stays fresh."),
        ],
        "peer_study": "Public profiles are at wellfound.com/u/<handle>. Google X-ray `site:wellfound.com/u \"<role>\" \"<skill>\"`; open 10 profiles of people now at funded startups you like. Copy structure (not text): bio pattern, achievement phrasing, which skills they list first.",
        "apply_signal": "Postings showing 'Actively hiring', 'Responds within a week', recent funding, and salary range visible. Apply with a 3-line custom note naming the product.",
    },
    "instahyre": {
        "title": "Instahyre",
        "region": "India",
        "profile_url": "https://www.instahyre.com/candidate/profile/",
        "search_url": "https://www.instahyre.com/search-jobs/?job_functions={role}&locations={location}",
        "recruiter_side": "Recruiter-initiated: employers browse ranked candidate lists and send 'interested' requests; you accept. Ranking uses profile completeness, skill match, last-active, and response rate.",
        "sections": [
            ("Current designation + company", "Target title; employers filter by designation."),
            ("Skills", "All posting skills you have, canonical spelling; top 5 drive match %."),
            ("Experience + CTC", "Accurate total/relevant years, current and expected CTC, notice period — required filters."),
            ("Preferred locations / roles", "Target cities first; role functions matching postings."),
            ("Resume", "Latest ATS resume; employers open it before sending a request."),
            ("Responsiveness", "Accept/decline invites within 24h — response rate affects ranking."),
        ],
        "peer_study": "Candidates aren't visible. Mine postings on Instahyre for your role: count skills across 15-20 listings, note the 'must have' lines and CTC bands.",
        "apply_signal": "Employer-initiated invites (highest callback rate) > 'Apply' on postings < 3 days old with match % ≥ 70.",
    },
    "foundit": {
        "title": "foundit (formerly Monster India)",
        "region": "India, Gulf, SEA",
        "profile_url": "https://www.foundit.in/seeker/profile",
        "search_url": "https://www.foundit.in/srp/results?query={role}&locations={location}&sort=1",
        "recruiter_side": "Recruiters use foundit resume database (keyword + experience + location + 'modified date'). Profile headline and key skills are indexed.",
        "sections": [
            ("Profile headline", "Title | YOE | top keywords | notice."),
            ("Key skills", "20-30 exact-phrase posting skills."),
            ("Employment + projects", "Bullets with tech + metric; projects add keyword surface."),
            ("Desired job", "Roles, industry, locations, expected CTC, notice period."),
            ("Freshness", "Re-save weekly; recruiters sort by last modified."),
        ],
        "peer_study": "Mine 15-20 foundit postings for your role; rank skills and titles. Cross-check with Naukri keyword list (same recruiter pool).",
        "apply_signal": "Postings < 3 days, 'Quick apply', recruiter name shown, applicant count low.",
    },
    "hirist": {
        "title": "hirist.tech",
        "region": "India (tech only)",
        "profile_url": "https://www.hirist.tech/profile",
        "search_url": "https://www.hirist.tech/search/{role_slug}",
        "recruiter_side": "Tech-only board; recruiters post and search by skills/experience. Recruiter often visible on posting — you can message them.",
        "sections": [
            ("Headline", "Title + YOE + stack."),
            ("Skills", "Exact stack terms; hirist search is skill-led."),
            ("Experience / notice / CTC", "Required filters; fill all."),
            ("Resume", "Latest ATS version."),
        ],
        "peer_study": "Mine postings in your category; note recurring stack combos and experience bands.",
        "apply_signal": "Recruiter-named postings < 7 days old; follow up via in-app message after applying.",
    },
    "cutshort": {
        "title": "Cutshort",
        "region": "India startups + remote",
        "profile_url": "https://cutshort.io/profile",
        "search_url": "https://cutshort.io/jobs/{role_slug}-jobs",
        "recruiter_side": "AI matching + recruiter search; your profile gets a match score per job. Recruiters see verified skills and 'open to' flags.",
        "sections": [
            ("Headline + about", "Title, YOE, what you build, one metric."),
            ("Skills with proficiency", "Rate honestly; take Cutshort skill tests for your top 3 to get verified badges."),
            ("Projects / GitHub", "Link GitHub — Cutshort shows activity."),
            ("Preferences", "Salary, notice, locations, remote."),
        ],
        "peer_study": "Mine postings for your role; note required skills and which ones carry 'must have'.",
        "apply_signal": "Jobs where your match score is high and posting is < 7 days; apply with a short note.",
    },
    "dice": {
        "title": "Dice",
        "region": "US (tech)",
        "profile_url": "https://www.dice.com/dashboard/profile",
        "search_url": "https://www.dice.com/jobs?q={role}&location={location}&filters.postedDate=ONE",
        "recruiter_side": "US tech recruiters (many staffing firms) search Dice by skills, title, work authorization, and 'last updated'. Very high recruiter volume.",
        "sections": [
            ("Profile visibility", "Searchable on; set work authorization correctly (filter)."),
            ("Desired title", "Exact posting title."),
            ("Skills with years", "Dice ranks heavily on skills + years — list each with years and last used."),
            ("Resume", "ATS version; Dice parses it into searchable text."),
            ("Preferences", "Employment type (FTE/contract/C2C), remote, relocation, pay."),
            ("Freshness", "Update profile weekly; recruiters sort by last updated."),
        ],
        "peer_study": "Mine 20 Dice postings; tally skills and 'Employment type'. Note which staffing firms post repeatedly — they search the database daily.",
        "apply_signal": "'Easy apply', posted today, direct employer (not 3rd party) or recruiter with phone listed.",
    },
    "ziprecruiter": {
        "title": "ZipRecruiter",
        "region": "US, UK, CA",
        "profile_url": "https://www.ziprecruiter.com/candidate/profile",
        "search_url": "https://www.ziprecruiter.com/jobs-search?search={role}&location={location}&days=1",
        "recruiter_side": "AI ('Phil') matches profiles to jobs and invites you to apply; employers see a match rating and can 'invite' you.",
        "sections": [
            ("Title + summary", "Target title and keywords from postings."),
            ("Resume", "ATS version — ZipRecruiter's match is resume-text driven."),
            ("Skills", "Posting spelling."),
            ("Preferences", "Pay, location, remote; enable 'Let employers find me'."),
        ],
        "peer_study": "Mine postings; ZipRecruiter shows a 'Great Match' label — note which keywords appear on postings you match well.",
        "apply_signal": "'1-Click Apply' + 'Great Match' + employer invitation + posted < 24h.",
    },
}

SCRAPER_SITE = {"indeed": "indeed", "glassdoor": "glassdoor", "ziprecruiter": "zip_recruiter"}

TEMPLATE = """---
name: {slug}-profile-optimizer
description: Audit and optimize the user's {title} profile so recruiters searching {title} for their target role find and contact them, using keywords mined from the latest postings on {title} and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my {slug} profile", "{slug} keywords", or wants more recruiter calls from {title}.
---

# {title} Profile Optimizer

Goal: rank in the searches recruiters run on {title} for the target role, with every claim backed by the resume.

Region: {region}

## Inputs
- Signed-in {title} account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `{profile_url}`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
{recruiter_side}

## Step 1 — Mine the latest postings on {title}
Open: `{search_url}` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. {scrape_hint}

## Step 2 — Study how strong candidates present themselves
{peer_study}
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
{section_rows}

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
{apply_signal}
{rank_hint}

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
"""


def render(slug: str, p: dict) -> str:
    rows = "\n".join(f"| {name} | {rule} |" for name, rule in p["sections"])
    site = SCRAPER_SITE.get(slug)
    if site:
        scrape_hint = f'Or run the bundled scraper: `jobhunt scrape --sites {site} --role "<role>" --location "<loc>" --hours 72 --keywords-report`.'
        rank_hint = f"Rank with the scraper's callback score: `jobhunt scrape --sites {site} --role ... --skills ... --years N --top 25`."
    else:
        scrape_hint = "No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool)."
        rank_hint = "Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5."
    return TEMPLATE.format(slug=slug, section_rows=rows, scrape_hint=scrape_hint, rank_hint=rank_hint, **{k: v for k, v in p.items() if k != "sections"})


def main() -> None:
    for slug, p in PLATFORMS.items():
        d = ROOT / f"{slug}-profile-optimizer"
        d.mkdir(parents=True, exist_ok=True)
        (d / "SKILL.md").write_text(render(slug, p), encoding="utf-8")
        print("wrote", d / "SKILL.md")


if __name__ == "__main__":
    main()
