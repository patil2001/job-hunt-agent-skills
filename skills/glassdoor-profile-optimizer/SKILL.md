---
name: glassdoor-profile-optimizer
description: Audit and optimize the user's Glassdoor profile so recruiters searching Glassdoor for their target role find and contact them, using keywords mined from the latest postings on Glassdoor and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my glassdoor profile", "glassdoor keywords", or wants more recruiter calls from Glassdoor.
---

# Glassdoor Profile Optimizer

Goal: rank in the searches recruiters run on Glassdoor for the target role, with every claim backed by the resume.

Region: Global (strong US/UK/India)

## Inputs
- Signed-in Glassdoor account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.glassdoor.com/member/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Glassdoor profile is shared with Indeed (same parent); employers mostly see it when you apply. 'Easy Apply' sends the Glassdoor profile + resume.

## Step 1 — Mine the latest postings on Glassdoor
Open: `https://www.glassdoor.com/Job/jobs.htm?sc.keyword={role}&locKeyword={location}&fromAge=1&sortBy=date_desc` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. Or run the bundled scraper: `jobhunt scrape --sites glassdoor --role "<role>" --location "<loc>" --hours 72 --keywords-report`.

## Step 2 — Study how strong candidates present themselves
Read 'Interviews' and 'Salaries' tabs for the target role at each target company: what titles got offers, what skills interviewers probed. Fold those keywords into your profile.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Headline / current title | Target title as recruiters type it. |
| Resume | Upload the ATS version (single column, keyword-matched). Easy Apply attaches this. |
| Experience + skills | Mirror resume; skills in posting spelling. |
| Job preferences | Titles, locations, remote, salary — drives the 'Jobs for you' feed and alerts. |
| Company research | Before applying, read the company's interview reviews for your role; note the questions. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
'Easy Apply' + posted < 24h + company rating ≥ 3.5 + 'Actively hiring'.
Rank with the scraper's callback score: `jobhunt scrape --sites glassdoor --role ... --skills ... --years N --top 25`.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
