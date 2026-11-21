---
name: recruiter-cold-email
description: Scrapes the internet for recruiter and HR contacts at top MNCs, product-based companies, and startups in Bangalore, then sends personalized cold emails via Gmail to surface Java/Spring Boot backend opportunities. Uses resume from Downloads, tracks all sent emails to avoid duplicates, and respects daily send caps (30 morning / 20 evening). Use this skill whenever the user asks to cold email recruiters, reach out to HR contacts, send job-outreach emails, run the recruiter email routine, or mentions "recruiter emails", "cold outreach", or "recruiter-cold-email". Always use this skill for any recruiter/HR outreach automation instead of doing it ad-hoc.
---

# Recruiter Cold Email

Finds HR/Talent Acquisition contacts at Bangalore tech companies, composes personalized cold
emails with the user's resume, previews a batch for approval, then sends via Gmail and logs
every send to avoid re-contacting the same person.

## Safety rules — read first

- **Never send without explicit user approval in the current session.** Always show a preview
  batch (at least 5 sample emails) and wait for a yes before bulk sending. If running on a
  schedule with no one watching, leave emails queued/drafted in Gmail rather than auto-sending,
  and surface a pending-approval notification.
- **30-day cooldown**: skip any recruiter already in `sent_log.json` with a `sent_at` within
  the last 30 days.
- **Daily caps**: morning session stops at 30 sends or 12:00 PM IST, whichever comes first.
  Evening session stops at 20 sends or 5:00 PM IST.

---

## Inputs

- **Resume**: Google Drive link `<YOUR_RESUME_LINK>`
  (shared publicly; include at end of each email body).
- **Gmail account**: `<YOUR_EMAIL>` — driven via Chrome MCP (Chrome must be open
  and logged into Gmail).
- **Contact**: `<YOUR_EMAIL> | <YOUR_PHONE>` (used in email signature)
- **Recruiter targets**: Individual recruiter patterns (firstname.lastname@company.com) preferred over company-level addresses
- **Daily cap**: passed in by the scheduled task prompt (`MORNING_CAP=30` or `EVENING_CAP=20`).

---

## State files

```
~/.claude/skills/recruiter-cold-email/
├── recruiter_pool.json   # cached contacts, refreshed if older than 7 days
└── sent_log.json         # all-time send history keyed by email address
```

---

## Workflow

### Step 1 — Parse resume

Read the PDF and extract into a structured profile:
- Full name, current/last company, total years of experience
- Top 6–8 skills (e.g. Java, Spring Boot, Microservices, Kafka, AWS, Docker)
- One-line career summary for the email opening

Keep this profile in memory; don't re-read the PDF on every email.

### Step 2 — Build / refresh recruiter pool

Check `recruiter_pool.json`. If it's missing or older than 7 days, run a fresh scrape.
Spawn **3 parallel subagents**, each covering one company tier. Each subagent must call
`tabs_create_mcp` to open its own dedicated browser tab and pass that `tabId` explicitly on
every subsequent Chrome MCP call — never share tabs between subagents, and always use `find`
+ `ref`-based interaction rather than screenshot pixel coordinates (background tabs don't have
a reliable screenshot).

**Subagent A — Top MNCs (Bangalore offices)**
Google, Microsoft, Amazon/AWS, Oracle, SAP, IBM, Accenture, Capgemini, Cognizant, Infosys,
Wipro, HCL, DXC Technology

**Subagent B — Product-based companies**
Flipkart, PhonePe, Razorpay, Swiggy, Meesho, CRED, Zepto, Freshworks, Zoho, Atlassian,
Unacademy, BigBasket, Urban Company

**Subagent C — Funded Bangalore startups**
BrowserStack, Chargebee, LeadSquared, CleverTap, Postman, Darwinbox, Setu, Multiplier,
Exotel, Healthplix, Apna, Jar, Open Financial, Slice, Jupiter Money

Each subagent's approach:
1. Try Apify actor `apify/linkedin-scraper` or `nix4/contact-info-scraper` to find
   HR / Talent Acquisition / Technical Recruiter contacts at each company in Bangalore.
2. If Apify yields no email (LinkedIn often hides them), use Chrome to Google-search:
   `"[Company]" recruiter OR "talent acquisition" Bangalore email site:linkedin.com`
   and extract any visible email addresses from profiles or company pages.
3. Also check the company's own careers/contact page for a recruiting email alias
   (e.g. `careers@company.com`, `talent@company.com`).
4. Return a list of `{name, title, company, email, source_url}` — skip anyone with no email.

Merge all three lists, de-duplicate by `email`, and save to `recruiter_pool.json` with a
`scraped_at` timestamp.

### Step 3 — Filter candidates

From `recruiter_pool.json`, remove anyone whose `email` appears in `sent_log.json` with a
`sent_at` in the last 30 days. Sort remaining by company tier (MNC → product → startup) for
better variety per batch.

### Step 4 — Compose emails

For each recruiter in the filtered list (up to the session cap), generate a cold email:

**Subject**: `Java/Spring Boot Developer (X yrs exp) — Open to Opportunities at [Company]`

**Body**:
```
Hi [First Name],

I'm [Full Name], a Java/Spring Boot backend developer with [X] years of experience,
currently/recently at [Last Company]. I specialize in [top 3 skills from resume].

I've been following [Company]'s work in [1 relevant sentence about what makes this company
interesting — e.g. "your microservices-at-scale engineering blog posts" for a tech company,
or "your fintech growth story" for a fintech startup]. I'd love to explore backend engineering
opportunities where I can contribute.

I've attached my resume for your reference. Would you be open to a quick 15-minute chat to
see if there's a fit?

Thanks for your time,
[Full Name]
<YOUR_EMAIL> | <YOUR_PHONE>

Resume: <YOUR_RESUME_LINK>
```

Keep the tone warm and concise — 3 short paragraphs max. Never fabricate specific claims about
the company's tech stack that you can't verify.

### Step 5 — Preview & approval

Before sending anything, show the user a formatted preview of the **first 5 emails** in the
batch: recipient name, company, subject, and body. Ask explicitly: "Shall I send all [N]
emails in this batch?" Wait for a yes before proceeding. If the routine is unattended
(scheduled run, no response), save all emails as **Gmail Drafts** instead of sending, and
report how many drafts were created.

### Step 6 — Send via Gmail (Chrome MCP)

For each approved email:
1. Navigate to `https://mail.google.com` in a **dedicated tab** (call `tabs_create_mcp` once
   at the start of this step, reuse that tab for all sends in the session).
2. Click **Compose** using `find("Compose button")` + `ref`.
3. Fill **To**, **Subject**, **Body** fields using `find` + `ref` for each field — never use
   pixel coordinates since other tabs may be open.
4. Attach the resume PDF: click the attachment icon, type the file path.
5. Click **Send** using `find("Send button")` + `ref`.
6. Immediately write to `sent_log.json`:
   ```json
   {"email": "...", "name": "...", "company": "...", "sent_at": "2026-06-27T09:15:00", "status": "sent"}
   ```
7. Wait 5–10 seconds between sends to avoid Gmail rate-limiting.

Stop when the daily cap is hit or the time boundary (noon / 5 PM) is reached.

### Step 7 — Report

Print a summary:
- Emails sent this session
- Emails saved as drafts (if unattended)
- Skipped (30-day cooldown)
- Failed (and why)
- Total in recruiter pool / total contacted to date

---

## Notes on scheduling

When invoked by a scheduled task:
- Morning task sets `SESSION_CAP=30`, time boundary = 12:00 PM IST
- Evening task sets `SESSION_CAP=20`, time boundary = 5:00 PM IST
- Both run Mon–Fri only
- Always fall back to Gmail Drafts if no human approves within the session — never
  auto-send on a schedule
