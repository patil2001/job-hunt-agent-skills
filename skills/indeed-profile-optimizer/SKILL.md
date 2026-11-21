---
name: indeed-profile-optimizer
description: Audit and optimize the user's Indeed profile so recruiters searching Indeed for their target role find and contact them, using keywords mined from the latest postings on Indeed and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my indeed profile", "indeed keywords", or wants more recruiter calls from Indeed.
---

# Indeed Profile Optimizer

Goal: rank in the searches recruiters run on Indeed for the target role, with every claim backed by the resume.

Region: Global (US, UK, India, CA, AU...)

## Inputs
- Signed-in Indeed account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://profile.indeed.com/`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Indeed Resume Search / Smart Sourcing: employers search resumes by keyword, title, location and 'last active'. Only profiles set to Public or Searchable appear.

## Step 1 — Mine the latest postings on Indeed
Open: `https://www.indeed.com/jobs?q={role}&l={location}&fromage=1&sort=date` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. Or run the bundled scraper: `jobhunt scrape --sites indeed --role "<role>" --location "<loc>" --hours 72 --keywords-report`.

## Step 2 — Study how strong candidates present themselves
Indeed hides other candidates. Study instead: (a) postings — titles and 'Qualifications' lists; (b) public resumes via Google X-ray `site:indeed.com/r "<title>" "<city>"` where still indexed; (c) LinkedIn profiles of people hired into the role.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Resume visibility | Set to Searchable (or Public). Private profiles never appear in Resume Search. |
| Job title / desired titles | Exact titles from current postings (e.g. 'Backend Engineer', 'Java Developer'), up to the allowed count. |
| Summary | 2-3 lines: title + years + 6-8 top posting keywords + domain. |
| Work experience | Bullets: action + tech + metric. Repeat key terms naturally; Indeed matches on resume text. |
| Skills | Every high-frequency posting skill you actually have, each with years of experience. |
| Qualifications / assessments | Take the free Indeed Assessments for your stack; 'Proficient' badges show to employers. |
| Job preferences | Desired pay, job types, remote, relocation. Ready to work = on. Pay filled (blank hides you from pay-filtered searches). |
| Freshness | Recruiters filter by 'active in last 30 days'. Log in and update one field weekly. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
'Easily apply' (Indeed Apply) and 'Responsive employer' badges; postings < 24h old with 'Hiring multiple candidates' get most callbacks.
Rank with the scraper's callback score: `jobhunt scrape --sites indeed --role ... --skills ... --years N --top 25`.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
