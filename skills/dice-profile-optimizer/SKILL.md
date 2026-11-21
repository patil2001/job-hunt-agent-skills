---
name: dice-profile-optimizer
description: Audit and optimize the user's Dice profile so recruiters searching Dice for their target role find and contact them, using keywords mined from the latest postings on Dice and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my dice profile", "dice keywords", or wants more recruiter calls from Dice.
---

# Dice Profile Optimizer

Goal: rank in the searches recruiters run on Dice for the target role, with every claim backed by the resume.

Region: US (tech)

## Inputs
- Signed-in Dice account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.dice.com/dashboard/profile`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
US tech recruiters (many staffing firms) search Dice by skills, title, work authorization, and 'last updated'. Very high recruiter volume.

## Step 1 — Mine the latest postings on Dice
Open: `https://www.dice.com/jobs?q={role}&location={location}&filters.postedDate=ONE` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Mine 20 Dice postings; tally skills and 'Employment type'. Note which staffing firms post repeatedly — they search the database daily.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Profile visibility | Searchable on; set work authorization correctly (filter). |
| Desired title | Exact posting title. |
| Skills with years | Dice ranks heavily on skills + years — list each with years and last used. |
| Resume | ATS version; Dice parses it into searchable text. |
| Preferences | Employment type (FTE/contract/C2C), remote, relocation, pay. |
| Freshness | Update profile weekly; recruiters sort by last updated. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
'Easy apply', posted today, direct employer (not 3rd party) or recruiter with phone listed.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
