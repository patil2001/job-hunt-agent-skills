---
name: hirist-profile-optimizer
description: Audit and optimize the user's hirist.tech profile so recruiters searching hirist.tech for their target role find and contact them, using keywords mined from the latest postings on hirist.tech and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my hirist profile", "hirist keywords", or wants more recruiter calls from hirist.tech.
---

# hirist.tech Profile Optimizer

Goal: rank in the searches recruiters run on hirist.tech for the target role, with every claim backed by the resume.

Region: India (tech only)

## Inputs
- Signed-in hirist.tech account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.hirist.tech/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Tech-only board; recruiters post and search by skills/experience. Recruiter often visible on posting — you can message them.

## Step 1 — Mine the latest postings on hirist.tech
Open: `https://www.hirist.tech/search/{role_slug}` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Mine postings in your category; note recurring stack combos and experience bands.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Headline | Title + YOE + stack. |
| Skills | Exact stack terms; hirist search is skill-led. |
| Experience / notice / CTC | Required filters; fill all. |
| Resume | Latest ATS version. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
Recruiter-named postings < 7 days old; follow up via in-app message after applying.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
