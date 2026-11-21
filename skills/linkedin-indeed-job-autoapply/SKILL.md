---
name: linkedin-indeed-job-autoapply
description: Automates finding and applying to Java/Spring Boot backend developer jobs posted in the last 24 hours on Indeed and LinkedIn, tailoring the resume and job description per job and saving them to Google Drive in a per-job folder, then staging both Easy Apply (in-platform) and external company-site applications for a single batch approval before final submit. Use this whenever the user asks to find/apply to Java, Spring Boot, or backend developer jobs, mentions running a job search automatically on a schedule, or references "job autoapply" / "job application pipeline". Always use this skill instead of ad-hoc browser automation for recurring job-search/apply requests.
---

# Java/Spring Boot Job Auto-Apply

Finds fresh (last 24h) Java/Spring Boot backend jobs on Indeed and LinkedIn, tailors application
materials per job, and stages applications for one quick human approval before final submission.

## Why the approval checkpoint exists

Clicking "Submit application" is irreversible and externally visible — it puts the user's name in
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

## Workflow

0. **Isolate the browser session.** Before navigating anywhere, call `tabs_create_mcp` to open a
   fresh dedicated tab/window for this run, and do all subsequent navigation inside that tab group.
   A sibling routine (naukri-job-autoapply) may be driving the same Chrome extension concurrently —
   never reuse or take over a tab you didn't just create, so the two runs don't collide on the same
   window. Capture the returned `tabId` and pass it explicitly on every subsequent `navigate`/
   `find`/`computer` call — never rely on the "active tab" default once more than one tab exists.

1. **Search, in parallel per site.** Spawn two parallel subagents — one for LinkedIn, one for
   Indeed — each given the role keywords, location, and instructed to call `tabs_create_mcp` itself
   to open its own dedicated tab before navigating (never share a tab between the two subagents, and
   never reuse the tab opened in step 0 for both sites). Each subagent must capture its own `tabId`
   and pass it explicitly on every call it makes for the rest of its work.
   Only one tab is foreground/visible at a time, so a background tab's screenshot will be wrong or
   stale — subagents must interact via `find` (which returns element refs) and click using the
   `ref` parameter, never via screenshot pixel coordinates, since coordinate clicks silently hit the
   wrong tab when it isn't focused. This applies to every subsequent step too (tailoring, staging),
   not just the search step. Each subagent independently:
   - On LinkedIn: uses the Jobs search with the "Past 24 hours" date filter. **Do not** turn on
     the "Easy Apply" filter — search without it so both Easy Apply and "Apply" (external,
     redirects to the company's own site) listings show up.
   - On Indeed: uses the search with the "Last 24 hours" date filter. Indeed similarly mixes
     "Apply on Indeed" and "Apply on company site" listings — keep both.
   - For every result on both sites, record job title, company, location, JD text, apply link,
     and which apply type it is (`applyType: "easy_apply"` or `applyType: "company_site"` —
     Indeed's "Apply on Indeed" counts as `easy_apply` for staging purposes since it's an
     in-platform form).
   Once both subagents return, merge their results into one combined list before continuing.

2. **Filter for relevance — apply ALL of these, they are hard rules:**
   - JD must mention Java and (Spring Boot or Spring Framework) as a core requirement — skip jobs
     where Java is just "a plus" if the primary stack is unrelated (e.g. pure .NET, pure frontend).
   - **Experience level: target ~2–3 years.** REJECT any job whose title contains Senior, Sr., Lead,
     Principal, Staff, or Architect, and any posting whose minimum experience requirement is 4+
     years (e.g. "4-9 yrs", "5-10 yrs"). A "2-5 yrs" range is fine; "4-9 yrs" is not. Check BOTH
     the title and the stated experience range — do not stage a job that fails this, even if the
     JD otherwise matches. (Past runs staged multiple Senior roles; this rule prevents that.)
   - Process up to **50 jobs per run**, worked in small batches (e.g. 10 at a time) so partial
     progress survives interruptions.

3. **Resume tailoring is OFF by default.** Do not rewrite the resume per job and do not create
   per-job Drive folders/PDFs unless the user has explicitly asked, in this run, to tailor the
   resume. By default, apply to every job with the same unmodified base resume.
   - For each relevant job, compute a match score between the base resume and the JD (overlap of
     required skills/keywords like Java, Spring Boot, Kafka, AWS, years of experience match).
   - Log every relevant job to a single Excel sheet (e.g.
     `~/Downloads/job_autoapply_log.xlsx`, append across runs, shared with naukri-job-autoapply)
     with columns: Job Title, Company, Job Link, Apply Type (Easy Apply / Company Site), Match
     Score, Application Status (staged / submitted / manual — needs review).
   - Only if the user explicitly asks for tailoring this run: rewrite the resume summary and
     reorder/emphasize bullets to mirror the JD's keywords without fabricating experience, save
     `Resume_<Company>.pdf` + `JD_<Company>.txt` to a Drive folder named
     `<Company> - <Job Title> - <YYYY-MM-DD>`, and use that tailored resume for the application
     instead of the base resume.

4. **Stage the application.** Branch on `applyType`:

   - **`easy_apply`** (LinkedIn Easy Apply, or Indeed "Apply on Indeed"): open the in-platform
     apply flow and fill in all fields (contact info, resume upload, screening questions) up to —
     but not including — the final submit click.
   - **`company_site`**: click through to the external application page (opens on the same
     isolated tab from step 0) and fill in the equivalent fields there — name, email, phone,
     resume upload, cover letter, and any screening questions — up to but not including the final
     submit/apply-equivalent control. External ATS platforms (Workday, Greenhouse, Lever, iCIMS,
     etc.) vary widely in layout, so use `find` to locate fields by label/placeholder text rather
     than assuming a fixed structure.
     - **Bail out to "manual — needs review" instead of guessing** if: the form requires creating
       a new account/password on the third-party site, presents a CAPTCHA, asks for a document
       beyond resume/cover letter you don't have, or you can't identify the field layout after a
       couple of `find` attempts. Log these in the batch summary with the link so the user can
       finish them by hand — never fabricate account credentials or force through an unfamiliar
       flow.

   For either path, if a screening question requires a judgment call (salary expectation, visa
   status, years of experience), use the user's resume facts; if it's not answerable from the
   resume, leave it flagged in the batch summary rather than guessing.

   **Caution (recurring incident — this has accidentally auto-submitted twice before, both on
   LinkedIn):** before clicking ANY job listing link, Easy Apply control, or external form's
   submit-equivalent button, run `find` fresh (never reuse a ref from an earlier `find` call in
   the same tab) and explicitly check for an already-open apply modal/page in that tab; close or
   back out of it first if found. Search-only steps must not click into a listing in a way that
   can trigger an apply flow. This caution applies equally to `company_site` forms — an external
   site's "Submit Application" is just as irreversible as LinkedIn's Easy Apply submit.

5. **Batch approval.** Once a batch of jobs is staged (or after exhausting the search), present the
   user a short list: company, title, link, apply type (Easy Apply / Company Site / manual —
   needs review), match score, anything flagged. Ask for explicit confirmation before clicking
   submit on each one. Only click submit on jobs the user approves.

6. **Report.** After submitting approved ones, summarize what was applied to (split by Easy Apply
   vs Company Site), what's still staged pending review, what got flagged "manual — needs review"
   and why, and where the Excel log (and any Drive folders, if tailoring was used) are.

## Notes on scheduling

When invoked on a recurring schedule (e.g. every 6 hours via `/schedule`), still do steps 1–4 fully
automatically, but never auto-confirm step 5 on your own — surface a pending-approval notification
each run instead. Track previously-seen job IDs/links (e.g. in a small local file like
`~/.claude/skills/linkedin-indeed-job-autoapply/seen_jobs.json`) so the same listing isn't reprocessed
every run.
