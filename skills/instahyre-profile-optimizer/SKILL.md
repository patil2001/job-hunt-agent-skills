---
name: instahyre-profile-optimizer
description: Audit and optimize the user's Instahyre profile so recruiters searching Instahyre for their target role find and contact them, using keywords mined from the latest postings on Instahyre and patterns from strong peer profiles, then apply approved edits in the browser. Use when the user says "optimize my instahyre profile", "instahyre keywords", or wants more recruiter calls from Instahyre.
---

# Instahyre Profile Optimizer

Goal: rank in the searches recruiters run on Instahyre for the target role, with every claim backed by the resume.

Region: India

## Inputs
- Signed-in Instahyre account in the browser the agent drives (user signs in; never sign out or change credentials). Profile editor: `https://www.instahyre.com/candidate/profile/`
- Resume: newest resume PDF in `~/Downloads` (or ask).
- Target role + location (ask if unknown; e.g. "Backend Engineer, Bangalore").

## How recruiters find you here
Recruiter-initiated: employers browse ranked candidate lists and send 'interested' requests; you accept. Ranking uses profile completeness, skill match, last-active, and response rate.

## Step 1 — Mine the latest postings on Instahyre
Open: `https://www.instahyre.com/search-jobs/?job_functions={role}&locations={location}` (fill role/location; newest first, last 1-3 days).
Collect 15-25 postings: title, required skills, experience band, salary if shown. Open 5 full descriptions for "must have" lines.
Rank skills and titles by frequency. No stable public scraper for this site: collect postings in the browser (read the result cards with the page text tool).

## Step 2 — Study how strong candidates present themselves
Candidates aren't visible. Mine postings on Instahyre for your role: count skills across 15-20 listings, note the 'must have' lines and CTC bands.
Write down 3 patterns worth copying (structure and ordering only — never copy text).

## Step 3 — Gap analysis
Keyword in postings AND resume but missing from profile → add. In postings but NOT in resume → list as a skill gap; do not add. Never invent skills, titles or metrics.

## Step 4 — Section rules
| Section | Rule |
|---|---|
| Current designation + company | Target title; employers filter by designation. |
| Skills | All posting skills you have, canonical spelling; top 5 drive match %. |
| Experience + CTC | Accurate total/relevant years, current and expected CTC, notice period — required filters. |
| Preferred locations / roles | Target cities first; role functions matching postings. |
| Resume | Latest ATS resume; employers open it before sending a request. |
| Responsiveness | Accept/decline invites within 24h — response rate affects ranking. |

## Step 5 — Apply
Show a before/after table. Editing the profile changes the user's account: get an explicit yes, then edit each section in the browser, save, and re-read the page to verify. Report what changed.

## Step 6 — Where to apply for the best callback odds
Employer-initiated invites (highest callback rate) > 'Apply' on postings < 3 days old with match % ≥ 70.
Score each collected posting with the same weights as `jobhunt/score.py`: recency 30, skill match 30, experience fit 15, not-above-level 10, easy apply 5, direct employer 5, salary shown 5.

## Step 7 — Keep it fresh
Re-run monthly against new postings; update one field weekly so "last active / last updated" stays recent.
