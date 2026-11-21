---
name: naukri-job-autoapply
description: Automates finding and applying to Java/Spring Boot backend developer jobs posted in the last 24 hours on Naukri.com, tailoring the resume and job description per job and saving them to Google Drive in a per-job folder, then staging Naukri "Apply" applications for a single batch approval before final submit. Use this whenever the user asks to find/apply to Java, Spring Boot, or backend developer jobs on Naukri, mentions running a Naukri job search automatically on a schedule, or references "naukri autoapply" / "naukri job application pipeline". Always use this skill instead of ad-hoc browser automation for recurring Naukri job-search/apply requests.
---

# Naukri Job Auto-Apply

Finds fresh (last 24h) Java/Spring Boot backend jobs on Naukri.com, tailors application
materials per job, and stages applications for one quick human approval before final submission.

## Why the approval checkpoint exists

Clicking "Apply" on Naukri is irreversible and externally visible — it puts the user's name in
front of a real employer. Never click the final submit/apply button without an explicit go-ahead
in the current conversation. Do everything else (search, tailor, fill the form) automatically, then
present a batch summary and wait for a yes before clicking submit on each one. If running on an
unattended schedule and no one responds to the approval prompt, leave applications staged/unsubmitted
and report what's pending — do not submit by default.

## Inputs needed

- **Base resume**: ask the user for the file path if not already known, or check
  `~/Downloads` for a recent resume PDF. Read it once and keep the parsed content (skills,
  experience bullets, education) in memory for the rest of the run.
- **Target role keywords**: default to "Java Developer", "Spring Boot Developer", "Backend
  Developer (Java)" unless the user specifies otherwise.
- **Location**: search **all of India** (plus remote), not just one city — do not restrict to Pune
  unless the user explicitly asks for a single city this run.
- **Naukri login**: the user must already be logged into Naukri.com in the Chrome profile being
  driven (Naukri requires an account for both search filters and applying). If not logged in,
  pause and ask the user to log in manually before continuing.

## Workflow

0. **Isolate the browser session.** Before navigating anywhere, call `tabs_create_mcp` to open a
   fresh dedicated tab/window for this run, and do all subsequent navigation inside that tab group.
   A sibling routine (linkedin-indeed-job-autoapply) may be driving the same Chrome extension
   concurrently — never reuse or take over a tab you didn't just create, so the two runs don't
   collide on the same window. Capture the returned `tabId` and pass it explicitly on every
   subsequent `navigate`/`find`/`computer` call — never rely on the "active tab" default once more
   than one tab exists.

1. **Search, in parallel per role keyword.** Naukri only has one site to search, so parallelize
   across the target role keywords instead (e.g. "Java Developer", "Spring Boot Developer",
   "Backend Developer (Java)"). Spawn one subagent per keyword, each instructed to call
   `tabs_create_mcp` itself to open its own dedicated tab before navigating (never share a tab
   between subagents, and never reuse the tab opened in step 0 for more than one keyword search).
   Each subagent must capture its own `tabId` and pass it explicitly on every call it makes for the
   rest of its work.
   Only one tab is foreground/visible at a time, so a background tab's screenshot will be wrong or
   stale — subagents must interact via `find` (which returns element refs) and click using the
   `ref` parameter, never via screenshot pixel coordinates, since coordinate clicks silently hit the
   wrong tab when it isn't focused. This applies to every subsequent step too (tailoring, staging),
   not just the search step. Each subagent independently:
   - Uses the Naukri search bar with its assigned keyword and the location, then applies the
     "Last 1 day" freshness filter (under "Filter By" → "Freshness").
   - Collects job title, company, location, JD text, and the job's Naukri apply link for each
     result, and returns that list back to you.
   Once all subagents return, merge their results into one combined list and de-duplicate by job
   link before continuing.

2. **Filter for relevance — apply ALL of these, they are hard rules:**
   - JD must mention Java and (Spring Boot or Spring Framework) as a core requirement — skip jobs
     where Java is just "a plus" if the primary stack is unrelated (e.g. pure .NET, pure frontend).
   - **Experience level: target ~2–3 years.** REJECT any job whose title contains Senior, Sr., Lead,
     Principal, Staff, or Architect, and any posting whose minimum experience requirement is 4+
     years (e.g. "4-9 yrs", "5-10 yrs", "7-9 yrs"). A "2-5 yrs" range is fine; "4-9 yrs" is not.
     This check runs on BOTH the title and the experience range shown on the listing card — do not
     stage a job that fails it, even if the JD otherwise matches. (Past runs staged multiple
     Senior/4-9yr roles; that is exactly the failure this rule exists to prevent.)
   - Process up to **50 jobs per run**, worked through in small batches (e.g. 10 at a time) rather
     than one giant pass, so partial progress survives interruptions.

3. **Resume tailoring is OFF by default.** Do not rewrite the resume per job and do not create
   per-job Drive folders/PDFs unless the user has explicitly asked, in this run, to tailor the
   resume (e.g. "tailor my resume for these jobs"). By default, apply to every job with the same
   unmodified base resume. This avoids the prior failure mode where "tailoring" silently degraded
   to untouched copies of the resume (no LaTeX/PDF tooling on this machine).
   - For each relevant job, compute a match score between the base resume and the JD (e.g. overlap
     of required skills/keywords like Java, Spring Boot, Kafka, AWS, years of experience match).
   - Log every relevant job to a single Excel sheet (e.g.
     `~/Downloads/naukri_autoapply_log.xlsx`, append across runs) with columns: Job Title, Company,
     Job Link, Match Score, Application Status.
   - Only if the user explicitly asks for tailoring this run: rewrite the resume summary and
     reorder/emphasize bullets to mirror the JD's keywords without fabricating experience, save
     `Resume_<Company>.pdf` + `JD_<Company>.txt` to a Drive folder named
     `<Company> - <Job Title> - <YYYY-MM-DD>`, and use that tailored resume for the application
     instead of the base resume.

4. **Stage the application.** Use Chrome to open the job's Naukri apply flow. Note that many Naukri
   listings are "1-click apply" using the profile already on file — for those, do not click Apply
   yet; just confirm the profile resume on file is the one being used (the base resume by default,
   or the tailored one only if tailoring was explicitly requested for that job). For listings with a
   custom application form, fill in all fields (contact info, resume upload, screening questions) up
   to — but not including — the final submit/apply click. If a screening question requires a
   judgment call (salary expectation, notice period, years of experience), use the user's resume
   facts; if it's not answerable from the resume, leave it flagged in the batch summary rather than
   guessing.

5. **Batch approval.** Once a batch of jobs is staged (or after exhausting the search), present the
   user a short list: company, title, link, match score, anything flagged. Ask for explicit
   confirmation before clicking submit/apply on each one. Only click submit on jobs the user
   approves.

6. **Report.** After submitting approved ones, summarize what was applied to, what's still staged
   pending review, and where the Excel log (and any Drive folders, if tailoring was used) are.

## Notes on scheduling

When invoked on a recurring schedule (e.g. every 6 hours via `/schedule`), still do steps 1–4 fully
automatically, but never auto-confirm step 5 on your own — surface a pending-approval notification
each run instead. Track previously-seen job IDs/links (e.g. in a small local file like
`~/.claude/skills/naukri-job-autoapply/seen_jobs.json`) so the same listing isn't reprocessed
every run.
