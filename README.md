# FOMAD — Automated Invoice Generator + Email Sender

> **Episode 3 — Automation Playlist**
> One command. Invoice written, PDF generated, email sent.

---

## What It Does

- Generates a professional A4 PDF invoice from a simple Python dict
- Automatically emails it to the client as an attachment
- Logs every sent invoice to a local CSV file
- No UI, no database, no friction — just fill in the config and run

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the env file and fill in your credentials
cp .env.example .env
```

Edit `.env`:
```
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

> **Gmail App Password:** Google Account → Security → 2-Step Verification → App Passwords.
> Use that — not your login password.
> Generate one here: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

---

## Usage

Edit the `INVOICE` dict at the top of `invoice_sender.py`:

```python
INVOICE = {
    "number":   "INV-0001",
    "currency": "€",
    "from": {
        "name":    "Your Name",
        "email":   "you@yourdomain.com",
        "address": "Your Address",
        "website": "yoursite.com",
    },
    "to": {
        "name":    "Client Name",
        "email":   "client@email.com",
        "address": "Client Address",
    },
    "items": [
        {"description": "Python Automation Script", "qty": 1, "rate": 200.00},
    ],
    "notes": "Payment due within 14 days.",
}
```

Then run:

```bash
python invoice_sender.py
```

The script will:
1. Generate `invoice_INV-0001_ClientName.pdf`
2. Email it to the client
3. Append a record to `invoice_log.csv`

---

## Output Example

```
╭─────────────────────────────────────────────╮
│ FOMAD Invoice Generator + Sender            │
│ Invoice : INV-0001                          │
│ Client  : Client Company Ltd               │
│ Total   : €700.00                           │
│ Due     : 01 May 2026                       │
╰─────────────────────────────────────────────╯

[1/3] Generating PDF
  ✔  PDF generated: invoice_INV-0001_Client_Company_Ltd.pdf

[2/3] Sending email
  ✔  Email sent → client@clientdomain.com

[3/3] Logging invoice
  ✔  Logged → invoice_log.csv
```

---

## Requirements

| Package        | Purpose                  |
|----------------|--------------------------|
| `reportlab`    | PDF generation           |
| `python-dotenv`| Load email credentials   |
| `rich`         | Terminal output          |

---

## How to Make Money With This

1. **Use it yourself** — stop wasting time writing invoices manually
2. **Sell it** — build a custom-branded version for freelancers or agencies (€100–€200)
3. **Wrap it in a UI** — add a simple web front-end and charge a monthly subscription

---

## 📞 Contact & Support

- **Website:** [fomad.net](https://fomad.net)
- **YouTube:** [FOMAD](https://youtube.com/@fomad)
- **Email:** info@fomad.net

---

## 📄 License

This project is free to use under the MIT License. You can:

- Use it for personal projects
- Use it for commercial projects
- Modify the code
- Distribute it
- Sell services built with it

> ⚠️ **Disclaimer:** This script is provided for educational and automation purposes. You are responsible for ensuring your invoices comply with local tax and legal requirements. The author is not liable for any financial, legal, or business outcomes from using this tool.
