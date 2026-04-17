# FOMAD — Episode 3
## Automated Invoice Generator + Email Sender

**Video title:** "I Built a Python Script That Writes and Sends Invoices Automatically"
**Target length:** 10–14 minutes
**Tone:** Practical, freelancer-focused. Lead with the pain, then the payoff.

---

### [HOOK — 0:00 to 0:20]

> "Every time I finish a project, I used to open a Google Doc,
> copy-paste the last invoice, update the numbers, export to PDF,
> attach it to an email, and send it manually.
>
> That's done.
> One Python script, one command — invoice written, PDF generated, email sent.
> Let me show you."

---

### [THE PROBLEM — 0:20 to 1:00]

Face to camera.

> "If you freelance — even part time — you know this pain.
> Writing invoices isn't hard, it's just annoying and repetitive.
> Every. Single. Time.
>
> And if you're running multiple clients, it stacks up fast.
>
> Today we automate it completely.
> Python generates a professional PDF invoice
> and emails it to the client — in one command."

---

### [THE BUILD — 1:00 to 9:00]

Walk through the script:

1. **INVOICE dict** — show how clean and simple the config is. Just fill it in.
2. **`calculate_totals()`** — qty × rate, subtotal, optional tax, total
3. **`generate_pdf()`** — reportlab layout: header, from/to block, items table, totals
4. **`send_email()`** — Gmail SMTP with SSL, PDF attached, body auto-written
5. **`log_invoice()`** — CSV log so you always have a record
6. **`.env` setup** — Gmail App Password walkthrough (not your login password)

> "The key thing here is the INVOICE dict at the top.
> Every video, every invoice — you just change this block. Everything else runs automatically."

---

### [THE DEMO — 9:00 to 11:30]

Run it live.

> "Let me fill in a real invoice — client name, items, rate — and run it."

Show:
- Terminal output with steps firing
- PDF file opens — clean, professional layout
- Gmail inbox — email arrives with PDF attached

> "That's the full thing. PDF generated, email sent, logged to CSV.
> One command."

---

### [THE SELL — 11:30 to 13:00]

> "Three ways to make money from this:
>
> One — use it yourself. Stop wasting time on invoices.
>
> Two — sell it. Freelancers, consultants, small agencies —
> they will pay €100–€200 for a customised version of this
> with their logo and branding built in.
>
> Three — wrap it in a simple UI, charge a monthly subscription.
> People already pay for invoice tools.
> Yours costs you an afternoon to build."

---

### [ENGAGEMENT — 13:00 to 13:40]

Face to camera. Serious tone — make it feel like a real deal.

> "Before I go — I want to make you a promise.
>
> If this video hits 20,000 likes,
> I will build the full UI version of this tool.
>
> Not a terminal script.
> A proper app — you open it, you add your customer details,
> you hit one button, and the invoice is generated and sent.
>
> And there'll be a full dashboard —
> every customer you've ever billed,
> every invoice you've sent, the amounts, the dates — all in one place.
>
> No code. No terminal. Just a clean tool you can actually hand to someone else.
>
> 20,000 likes. That's the number.
> You decide if this gets built."

Pause. Let it land.

> "Link's in the description. Go."

---

### [CLOSE — 13:40 to 14:00]

> "Time saved. Money made.
> This is FOMAD."

---

## Visuals Guide

| Timestamp   | Visual                                                                              |
| ----------- | ----------------------------------------------------------------------------------- |
| 0:00–0:20   | Screen: manual invoice process in Google Docs — slow and painful                    |
| 0:20–1:00   | Face to camera                                                                      |
| 1:00–9:00   | Code editor live walkthrough — highlight each section                               |
| 9:00–11:30  | Terminal run → PDF opens → email inbox shows received invoice                       |
| 11:30–13:00 | Face to camera — monetisation angles                                                |
| 13:00–13:40 | Face to camera — engagement pitch. Show mockup UI screenshot if available           |
| 13:40–14:00 | Cut to black → "Time saved. Money made." → fomad.net                               |

> **UI mockup tip:** Even a rough Figma or screenshot of what the app would look like on screen during the engagement section makes the promise feel real and drives more likes.
