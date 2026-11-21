---
name: cutshort-profile-optimizer
description: Audit and optimize the user's Cutshort profile so recruiters searching Cutshort for their target role find and contact them, using keywords mined from the latest postings on Cutshort and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my cutshort profile", "cutshort keywords", or wants more recruiter calls from Cutshort.
---

# Cutshort Profile Optimizer

Goal: rank in the searches recruiters run on Cutshort for the target role, with every claim backed by the resume.

Region: India startups + remote

## Inputs
- Signed-in Cutshort account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://cutshort.io/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
AI matching + recruiter search; your profile gets a match score per job. Recruiters see verified skills and 'open to' flags.

## Step 1 — Mine the latest postings on Cutshort
Open: `https://cutshort.io/jobs/{role_slug}-jobs` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Mine postings for your role; note required skills and which ones carry 'must have'.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Headline + about | Title, YOE, what you build, one metric. |
| Skills with proficiency | Rate honestly; take Cutshort skill tests for your top 3 to get verified badges. |
| Projects / GitHub | Link GitHub — Cutshort shows activity. |
| Preferences | Salary, notice, locations, remote. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
Jobs where your match score is high and posting is < 7 days; apply with a short note.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
