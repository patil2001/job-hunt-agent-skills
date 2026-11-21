---
name: foundit-profile-optimizer
description: Audit and optimize the user's foundit (formerly Monster India) profile so recruiters searching foundit (formerly Monster India) for their target role find and contact them, using keywords mined from the latest postings on foundit (formerly Monster India) and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my foundit profile", "foundit keywords", or wants more recruiter calls from foundit (formerly Monster India).
---

# foundit (formerly Monster India) Profile Optimizer

Goal: rank in the searches recruiters run on foundit (formerly Monster India) for the target role, with every claim backed by the resume.

Region: India, Gulf, SEA

## Inputs
- Signed-in foundit (formerly Monster India) account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.foundit.in/seeker/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Recruiters use foundit resume database (keyword + experience + location + 'modified date'). Profile headline and key skills are indexed.

## Step 1 — Mine the latest postings on foundit (formerly Monster India)
Open: `https://www.foundit.in/srp/results?query={role}&locations={location}&sort=1` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Mine 15-20 foundit postings for your role; rank skills and titles. Cross-check with Naukri keyword list (same recruiter pool).
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Profile headline | Title | YOE | top keywords | notice. |
| Key skills | 20-30 exact-phrase posting skills. |
| Employment + projects | Bullets with tech + metric; projects add keyword surface. |
| Desired job | Roles, industry, locations, expected CTC, notice period. |
| Freshness | Re-save weekly; recruiters sort by last modified. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
Postings < 3 days, 'Quick apply', recruiter name shown, applicant count low.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
