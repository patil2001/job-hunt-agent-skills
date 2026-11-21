---
name: linkedin-recruiter-optimizer
description: Audit and optimize the user's live LinkedIn profile (headline, About, top skills, experience bullets, open-to-work) so LinkedIn Recruiter keyword searches for their target role surface it, then apply approved edits in the browser. Use when the user says "optimize my linkedin", "linkedin headline/about", "linkedin keywords", or wants more recruiter InMails. Companion to naukri-profile-optimizer; reuses resume-ats-optimizer, job-description-analyzer, resume-bullet-writer, resume-quantifier and linkedin-profile-optimizer methods.
---

# LinkedIn Recruiter Optimizer

Goal: profile ranks for the exact phrases recruiters type into LinkedIn Recruiter, and every claim is backed by the resume.

## Inputs
- Live profile in the built-in browser (user signed in; never sign out or touch settings beyond the profile).
- Resume: newest resume PDF in the user's Downloads folder.
- Target role (default: Java / Spring Boot backend engineer).

## Step 1 - Read the profile
Background tabs don't render LinkedIn's lazy sections: front the tab first. Reliable direct URLs:
- Experience: `/in/<id>/details/experience/` (edit links: `find "Edit <title> at <company>"`)
- Skills: `/in/<id>/details/skills/`
- About + top skills editor: `/in/<id>/edit/forms/summary/new/`
- Headline/intro editor: `/in/<id>/edit/intro/`

## Step 2 - Keyword list (job-description-analyzer method)
Pull titles + skills from 5-10 current target JDs (in.linkedin.com/jobs/<role>-jobs, open a few full JDs). Rank by frequency. Keep only keywords also in the resume; list the rest as gaps to learn.

## Step 3 - Section rules
| Section | Rule |
|---|---|
| Headline (220 chars) | `Target title | 5-7 top JD keywords | YOE @ Company (client) | niche edge | Open to <roles>`. Lead with the title recruiters search, not an internal job title. |
| About (2600 chars) | First person. Line 1 = title + YOE + domain. 4-6 "What I've delivered" bullets with numbers from the resume. A "Tech stack" line with exact keyword spellings. Side project link. Target roles, locations, notice period. No buzzword filler. |
| Top skills (5) | The 5 highest-frequency JD skills you actually have (e.g. Java, Spring Boot, Microservices, Apache Kafka, Kubernetes). |
| Experience | 4-7 bullets per role: action + tech + metric; strongest metric first. Stack line at the end. Attach skills to each role. |
| Skills section | 30-50 skills; pin JD keywords; remove vague ones ("Server Side", "Software Construction"). |
| Open to work | Recruiters-only, correct titles, locations, work types. |
| Featured | Portfolio / GitHub / best post. |

## Step 4 - Apply
Show a before/after draft; editing the profile needs the user's yes. LinkedIn editors are contenteditable divs: focus, select all (Range API), then type with real keystrokes - setting `.value`/`innerText` does not persist. Insert at start via a collapsed Range then type. Click Save, dismiss the "next action" upsell, re-read to verify.

## Step 5 - Keep it fresh
Post or comment weekly on stack topics; recruiters see activity. Re-run monthly against new JDs.
