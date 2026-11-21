---
name: wellfound-profile-optimizer
description: Audit and optimize the user's Wellfound (AngelList Talent) profile so recruiters searching Wellfound (AngelList Talent) for their target role find and contact them, using keywords mined from the latest postings on Wellfound (AngelList Talent) and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my wellfound profile", "wellfound keywords", or wants more recruiter calls from Wellfound (AngelList Talent).
---

# Wellfound (AngelList Talent) Profile Optimizer

Goal: rank in the searches recruiters run on Wellfound (AngelList Talent) for the target role, with every claim backed by the resume.

Region: Global startups (US, India, EU, remote)

## Inputs
- Signed-in Wellfound (AngelList Talent) account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://wellfound.com/profile/edit/overview`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Founders search candidates by role, skills, location, salary, and see 'Looking for' + 'Last active'. Startups message you directly; strong profiles get inbound.

## Step 1 — Mine the latest postings on Wellfound (AngelList Talent)
Open: `https://wellfound.com/role/r/{role_slug}?remote=true` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Public profiles are at wellfound.com/u/<handle>. Google X-ray `site:wellfound.com/u "<role>" "<skill>"`; open 10 profiles of people now at funded startups you like. Copy structure (not text): bio pattern, achievement phrasing, which skills they list first.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Primary role + years | Pick the exact role taxonomy (e.g. 'Backend Engineer'); years per role drive search filters. |
| Bio (one-liner) | What you build + strongest proof (metric or product). |
| What I'm looking for | Stage (seed/Series A...), company size, remote, tech — founders read this first. |
| Achievements | 3-5 one-line wins with numbers; founders scan for shipping velocity and ownership. |
| Skills | Up to the cap, posting spelling, most in-demand first. |
| Salary / equity | Fill minimums honestly; blank = excluded from filtered searches. |
| Links | GitHub, portfolio, LinkedIn. Side projects weigh heavily on Wellfound. |
| Availability | 'Actively looking' + 'Ready to interview' — re-confirm weekly so 'Last active' stays fresh. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
Postings showing 'Actively hiring', 'Responds within a week', recent funding, and salary range visible. Apply with a 3-line custom note naming the product.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
