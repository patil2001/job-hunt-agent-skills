---
name: ziprecruiter-profile-optimizer
description: Audit and optimize the user's ZipRecruiter profile so recruiters searching ZipRecruiter for their target role find and contact them, using keywords mined from the latest postings on ZipRecruiter and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my ziprecruiter profile", "ziprecruiter keywords", or wants more recruiter calls from ZipRecruiter.
---

# ZipRecruiter Profile Optimizer

Goal: rank in the searches recruiters run on ZipRecruiter for the target role, with every claim backed by the resume.

Region: US, UK, CA

## Inputs
- Signed-in ZipRecruiter account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.ziprecruiter.com/candidate/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
AI ('Phil') matches profiles to jobs and invites you to apply; employers see a match rating and can 'invite' you.

## Step 1 — Mine the latest postings on ZipRecruiter
Open: `https://www.ziprecruiter.com/jobs-search?search={role}&location={location}&days=1` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. Or run the bundled scraper: `jobhunt scrape --sites zip_recruiter --role "<role>" --location "<loc>" --hours 72 --keywords-report`.

## Step 2 — Study how strong candidates present themselves
Mine postings; ZipRecruiter shows a 'Great Match' label — note which keywords appear on postings you match well.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Title + summary | Target title and keywords from postings. |
| Resume | ATS version — ZipRecruiter's match is resume-text driven. |
| Skills | Posting spelling. |
| Preferences | Pay, location, remote; enable 'Let employers find me'. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
'1-Click Apply' + 'Great Match' + employer invitation + posted < 24h.
Rank with the scraper's callback score: `jobhunt scrape --sites zip_recruiter --role ... --skills ... --years N --top 25`.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
