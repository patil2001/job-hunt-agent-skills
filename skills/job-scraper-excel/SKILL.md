---
name: job-scraper-excel
description: >
  Scrapes the latest 50 job listings for Java/Spring Boot backend developer roles
  from web startups, product-based companies, and top MNCs across India. Saves results
  to a timestamped Excel file under ~/job-scrapes/<datetime>\jobs.xlsx.
  Auto-picks the most recently modified resume PDF from ~/Downloads/.
  Use this skill whenever the user asks to: scrape jobs, find latest job listings,
  log jobs to Excel, run the morning/evening job scrape, check what jobs are out today,
  or mentions "job-scrapes", "job scraper", or "scrape jobs". Also use when a scheduled
  routine fires for the 6 AM or 7 PM job scan.
---

# Job Scraper → Excel Skill

Scrape the latest 50 Java/Spring Boot backend developer jobs from web startups,
product companies, and top MNCs in India. Log them to a datetime-stamped Excel
file. Auto-select the freshest resume from Downloads for reference.

---

## Step 1: Pick the Latest Resume

Scan `~/Downloads/` for PDF files. Pick the one with the most recent
last-modified timestamp. Note its filename — you'll log it as the "Resume Used"
in the Excel header row / sheet metadata.

Use PowerShell to find it:
```powershell
Get-ChildItem "~/Downloads/*.pdf" |
  Sort-Object LastWriteTime -Descending |
  Select-Object -First 1 -ExpandProperty FullName
```

---

## Step 2: Create the Output Folder

Timestamp format: `YYYY-MM-DD_HH-MM` (24h, IST).

```powershell
$ts = Get-Date -Format "yyyy-MM-dd_HH-mm"
$folder = "~/job-scrapes/$ts"
New-Item -ItemType Directory -Force -Path $folder
```

Output file: `$folder\jobs.xlsx`

---

## Step 3: Scrape Jobs

### Sources & Scraping Approach

Scrape from **LinkedIn** and **Naukri** using dedicated Apify actors. Target 25 jobs
from each source to reach 50 total. Deduplicate by URL before writing.

**Filters on every source:**
- Posted: last 24 hours
- Location: India (all cities)
- Experience: 1–4 years (include jobs whose range overlaps 1–4)
- **Exclude titles containing**: Senior, Lead, Principal, Staff, Architect, Manager, Head, VP

---

### Source A — LinkedIn

Use `mcp__Apify__apify--rag-web-browser` with this URL (returns up to 60 listings
on one page, filter experience client-side):

```
https://www.linkedin.com/jobs/search/?keywords=Java+Spring+Boot+Kafka+Microservices+AWS&location=India&f_TPR=r86400&f_E=3,4
```

Extract from the markdown response: Job Title, Company, Location, Date Posted, Job URL.
Filter out any title containing Senior / Lead / Principal / Staff / Architect / Manager /
Head / VP. Keep jobs whose posted time is within 24 hours.

---

### Source B — Naukri

> **Do NOT use `apify/rag-web-browser` for Naukri.** Naukri is a React SPA —
> the RAG browser only receives the JS loading splash screen, returning a blank
> placeholder image with no jobs. Use the dedicated actor below instead.

Use `mcp__Apify__call-actor` with actor **`valig/naukri-jobs-scraper`**:

```json
{
  "keywords": "java spring boot microservices kafka aws",
  "jobAge": "1",
  "sort": "f",
  "limit": 30
}
```

Field mapping from actor output:
- `title` → Job Title
- `company.name` → Company
- `locations.label` → Location
- `experience.text` → Experience (e.g. "2-4 Yrs")
- `experience.minimum` / `experience.maximum` → for filtering
- `createdDateText` → Date Posted
- `url` → Job URL

**Experience filter (client-side):** keep only rows where `experience.minimum <= 4`.
This captures jobs posted for 1–4 year ranges even when the max extends slightly beyond.

Backup actor if `valig` fails: **`muhammetakkurtt/naukri-job-scraper`**
(requires `maxJobs >= 50`; use `freshness: "1"`, `sortBy: "date"`, `experience: "all"`).

---

### Indeed India

Indeed India (in.indeed.com) returns HTTP 500 errors with Apify's RAG browser.
**Skip Indeed** — fill the 50-job target from LinkedIn + Naukri instead.
Log "Indeed: skipped (HTTP 500)" in the Summary sheet.

---

For each job collected, record:
- **Job Title**
- **Company Name**
- **Location** (city/remote)
- **Experience Required**
- **Date Posted** (or "Today" / hours ago)
- **Job URL** (direct link)
- **Job Type** (startup / product / MNC — infer from company name)
- **Source** (LinkedIn / Naukri)

Collect up to 50 unique jobs (deduplicate by URL). If fewer than 50 are found after
both sources, log the actual count — do not pad with duplicates.

---

## Step 4: Write the Excel File

Use the `anthropic-skills:xlsx` skill to create the Excel file at the output path.

### Sheet: "Jobs"

| Column | Header |
|--------|--------|
| A | # |
| B | Job Title |
| C | Company |
| D | Location |
| E | Experience |
| F | Date Posted |
| G | Job Type |
| H | Source |
| I | Job URL |

**Formatting:**
- Header row: bold, blue background (#1F4E79), white text
- Freeze top row
- Auto-fit column widths
- Alternate row shading (light grey every other row)
- Column I (Job URL): make cells hyperlinks
- Add a summary row at top (above header, merged A1:I1):
  `"Scraped: <datetime> | Resume: <resume filename> | Total: <N> jobs"`

### Sheet: "Summary"

| Row | Content |
|-----|---------|
| 1 | Scrape Date |
| 2 | Resume Used |
| 3 | Total Jobs Found |
| 4 | Startups |
| 5 | Product Companies |
| 6 | MNCs |
| 7 | Sources Breakdown |

---

## Step 5: Report Back

Tell the user:
- How many jobs were found (total, by category, by source)
- Where the file was saved (full path)
- Which resume was auto-selected
- Any scrape errors or sources that returned 0 results

Example:
```
Scraped 50 jobs → ~/job-scrapes/2026-07-01_18-00\jobs.xlsx
Resume used: Firstname_Lastname_Resume.pdf
Breakdown: 18 startups | 14 product | 18 MNCs
Sources: LinkedIn (22) | Naukri (18) | Indeed (10)
```

---

## Notes

- Skip any job with "Senior", "Lead", "Principal", "Staff", "Architect", "Manager",
  "Head", or "VP" in the title — these are out of scope.
- If a source is blocked or returns 0 results, log the error in the Summary sheet
  and continue with the remaining sources.
- If fewer than 50 unique jobs are found after all sources, log what was found —
  do not pad with duplicates.
- The `job-scrapes` root folder is `~/job-scrapes/` — create it if it
  doesn't exist yet.
