# Job Hunt Agent Skills

Agent skills (`SKILL.md`) that run a job search for you: optimize your LinkedIn and Naukri profiles for recruiter search, scrape fresh postings, stage applications, and draft recruiter outreach. Works with Claude Code, Codex CLI, Cursor, Gemini CLI and any agent that reads the open SKILL.md standard.

Every irreversible step (saving a profile edit, submitting an application, sending an email) stops for your explicit approval. On a schedule with nobody watching, the skills stage work and report what is pending; they never submit by default.

## Skills

| Skill | What it does |
|---|---|
| [`linkedin-recruiter-optimizer`](skills/linkedin-recruiter-optimizer/SKILL.md) | Mines current JDs for your target role, then rewrites headline, About, top skills, experience bullets and Open-to-work so LinkedIn Recruiter searches surface you. |
| [`naukri-profile-optimizer`](skills/naukri-profile-optimizer/SKILL.md) | Same for Naukri.com: resume headline, key skills, IT skills table, summary, career profile, daily freshness save. |
| [`job-scraper-excel`](skills/job-scraper-excel/SKILL.md) | Pulls the latest postings (last 24h) from LinkedIn and Naukri into a dated Excel file. |
| [`linkedin-indeed-job-autoapply`](skills/linkedin-indeed-job-autoapply/SKILL.md) | Finds last-24h jobs on LinkedIn and Indeed, filters by stack and seniority, scores match, fills Easy Apply and company-site forms up to submit, then asks for batch approval. |
| [`naukri-job-autoapply`](skills/naukri-job-autoapply/SKILL.md) | Same pipeline for Naukri.com. |
| [`recruiter-cold-email`](skills/recruiter-cold-email/SKILL.md) | Builds a recruiter contact pool, drafts personalized cold emails, previews a batch, sends via Gmail with daily caps and a 30-day cooldown. |

## Install

Claude Code:

```bash
git clone https://github.com/patil2001/job-hunt-agent-skills
cp -r job-hunt-agent-skills/skills/* ~/.claude/skills/
```

Other agents: copy each `skills/<name>/` folder wherever your agent loads skills from.

## Configure

Defaults target **Java / Spring Boot backend roles, 2-4 years, India**. To retarget, edit the role keywords, locations and experience filters near the top of each `SKILL.md`, or just tell the agent ("target React frontend roles in Berlin").

Placeholders to fill in `recruiter-cold-email`: `<YOUR_EMAIL>`, `<YOUR_PHONE>`, `<YOUR_RESUME_LINK>`.

Requirements:
- A browser the agent can drive (Claude in Chrome, or Claude Code's built-in browser), signed in to LinkedIn / Naukri / Indeed / Gmail yourself.
- Your resume PDF in `~/Downloads`.
- `job-scraper-excel` uses Apify actors; the others need only the browser.

## Usage

```
optimize my linkedin for senior backend roles
run the naukri autoapply
scrape jobs
run recruiter cold email, morning batch
```

Schedule the auto-apply or scrape skills (e.g. Claude Code `/schedule`) to run every few hours; they track seen jobs so nothing is processed twice.

## Responsible use

Respect each site's terms of service and rate limits. Never let an agent invent skills, experience or metrics: these skills only use what is in your resume. Review every batch before it goes out.

## License

MIT
