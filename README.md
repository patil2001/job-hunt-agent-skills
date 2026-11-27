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

### Profile optimizers for every major job platform

Each one mines the latest postings on that platform, studies how strong candidates present themselves there, then rewrites your profile section by section (with your approval).

| Platform | Region | Skill |
|---|---|---|
| LinkedIn | Global | [`linkedin-recruiter-optimizer`](skills/linkedin-recruiter-optimizer/SKILL.md) |
| Naukri | India | [`naukri-profile-optimizer`](skills/naukri-profile-optimizer/SKILL.md) |
| Indeed | Global | [`indeed-profile-optimizer`](skills/indeed-profile-optimizer/SKILL.md) |
| Glassdoor | Global | [`glassdoor-profile-optimizer`](skills/glassdoor-profile-optimizer/SKILL.md) |
| Wellfound (AngelList) | Startups, global | [`wellfound-profile-optimizer`](skills/wellfound-profile-optimizer/SKILL.md) |
| Instahyre | India | [`instahyre-profile-optimizer`](skills/instahyre-profile-optimizer/SKILL.md) |
| foundit (Monster) | India, Gulf, SEA | [`foundit-profile-optimizer`](skills/foundit-profile-optimizer/SKILL.md) |
| hirist.tech | India tech | [`hirist-profile-optimizer`](skills/hirist-profile-optimizer/SKILL.md) |
| Cutshort | India startups | [`cutshort-profile-optimizer`](skills/cutshort-profile-optimizer/SKILL.md) |
| Dice | US tech | [`dice-profile-optimizer`](skills/dice-profile-optimizer/SKILL.md) |
| ZipRecruiter | US, UK, CA | [`ziprecruiter-profile-optimizer`](skills/ziprecruiter-profile-optimizer/SKILL.md) |

The nine generic ones are generated from [`tools/gen_platform_skills.py`](tools/gen_platform_skills.py): edit the platform facts there and re-run.

## `jobhunt`: scrape recent jobs, ranked by callback likelihood

A small Python library + CLI on top of [JobSpy](https://github.com/speedyapply/JobSpy). It pulls the newest postings from **LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs and Naukri**, de-duplicates them, and ranks each one by how likely you are to get a callback:

| Signal | Points |
|---|---|
| Posted < 24h (72h: 20, 7d: 10) | 30 |
| Your skills found in the posting | 30 |
| Minimum experience within your reach | 15 |
| Title not above your level (no Senior/Lead/Principal unless `--allow-senior`) | 10 |
| Easy / in-platform apply | 5 |
| Direct employer apply link | 5 |
| Salary shown | 5 |

```bash
pip install git+https://github.com/patil2001/job-hunt-agent-skills
jobhunt scrape --sites linkedin indeed naukri --role "Java Developer" --location Bangalore \
  --skills java "spring boot" microservices kafka aws --years 3 --hours 24 --top 50 \
  --out jobs.xlsx --keywords-report
```

Output: `jobs.xlsx` sorted by `callback_score`, with matched skills and the per-signal breakdown, plus the most frequent skills across all postings (feed that into the profile optimizers). Use `--country usa` (or `uk`, ...) for Indeed/Glassdoor outside India.

Naukri's API often answers `406 recaptcha required` to scrapers; when it does, the run continues with the other sites and the `naukri-job-autoapply` skill covers Naukri in the browser. Wellfound, Instahyre, foundit, hirist, Cutshort and Dice block plain scrapers; their skills collect postings in the browser and score them with the same weights.

## Install skills

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
