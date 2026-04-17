"""
FOMAD - Episode 3 (Automation Playlist)
Automated Invoice Generator + Email Sender

What it does:
  1. Takes invoice data from a simple Python dict (no database, no UI)
  2. Generates a professional PDF invoice using reportlab
  3. Automatically emails it to the client as an attachment
  4. Logs every sent invoice to a local CSV file

Requirements:
  pip install reportlab python-dotenv rich certifi
"""

import os
import csv
import smtplib
import ssl
import certifi
from email.mime.multipart import MIMEMultipart
from email.mime.text     import MIMEText
from email.mime.base     import MIMEBase
from email               import encoders
from datetime            import datetime, date, timedelta
from reportlab.lib.pagesizes  import A4
from reportlab.lib            import colors
from reportlab.lib.units      import cm
from reportlab.platypus       import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles     import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums      import TA_RIGHT, TA_LEFT
from dotenv                   import load_dotenv
from rich.console             import Console
from rich.rule                import Rule
from rich.panel               import Panel
from rich import box as rich_box
from rich.table               import Table as RichTable

console = Console()
load_dotenv()

# ─────────────────────────────────────────────
#  CONFIG — update these every time you send
# ─────────────────────────────────────────────

INVOICE = {
    "number":      "INV-0001",
    "date":        date.today().strftime("%d %b %Y"),
    "due_date":    (date.today() + timedelta(days=14)).strftime("%d %b %Y"),
    "currency":    "€",

    # Your details
    "from": {
        "name":    "Your Name / Company",
        "email":   "you@yourdomain.com",
        "address": "123 Your Street, City, Country",
        "website": "yourwebsite.com",
    },

    # Client details
    "to": {
        "name":    "Client Company Ltd",
        "email":   "client@clientdomain.com",
        "address": "456 Client Ave, Client City",
    },

    # Line items
    "items": [
        {"description": "Lead Generation Script (custom)",  "qty": 1, "rate": 200.00},
        {"description": "PDF to Excel Automation Tool",     "qty": 1, "rate": 150.00},
        {"description": "Setup & Handover Call (1 hour)",   "qty": 1, "rate":  75.00},
    ],

    "notes": "Payment due within 14 days. Bank transfer preferred.",
}

# Email sending credentials — stored in .env
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")    # your Gmail address
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Gmail App Password (not your login password)
SMTP_HOST      = "smtp.gmail.com"
SMTP_PORT      = 465

LOG_FILE = "invoice_log.csv"


# ─────────────────────────────────────────────
#  STEP 1 — CALCULATE TOTALS
# ─────────────────────────────────────────────

def calculate_totals(items: list[dict]) -> tuple[float, float, float]:
    subtotal = sum(i["qty"] * i["rate"] for i in items)
    tax      = round(subtotal * 0.0, 2)   # set your tax rate here, e.g. 0.23 for 23%
    total    = round(subtotal + tax, 2)
    return round(subtotal, 2), tax, total


# ─────────────────────────────────────────────
#  STEP 2 — GENERATE PDF INVOICE
# ─────────────────────────────────────────────

def generate_pdf(invoice: dict, output_path: str):
    """Build a professional A4 PDF invoice using reportlab."""
    doc    = SimpleDocTemplate(output_path, pagesize=A4,
                               topMargin=1.5*cm, bottomMargin=1.5*cm,
                               leftMargin=2*cm,  rightMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    cur = invoice["currency"]
    subtotal, tax, total = calculate_totals(invoice["items"])

    # ── Styles ──────────────────────────────
    style_title  = ParagraphStyle("title",  fontSize=22, textColor=colors.HexColor("#111111"),
                                  spaceAfter=2)
    style_sub    = ParagraphStyle("sub",    fontSize=9,  textColor=colors.HexColor("#888888"),
                                  spaceAfter=2)
    style_label  = ParagraphStyle("label",  fontSize=8,  textColor=colors.HexColor("#888888"),
                                  spaceBefore=8)
    style_value  = ParagraphStyle("value",  fontSize=10, textColor=colors.HexColor("#111111"))
    style_right  = ParagraphStyle("right",  fontSize=10, alignment=TA_RIGHT)
    style_note   = ParagraphStyle("note",   fontSize=8,  textColor=colors.HexColor("#555555"),
                                  spaceBefore=6)

    # ── Header: INVOICE + number/date block ─
    header_data = [
        [Paragraph("<b>INVOICE</b>", style_title),
         Paragraph(f"<b>#{invoice['number']}</b>", style_right)],
        [Paragraph(invoice["from"]["name"], style_sub),
         Paragraph(f"Date:     {invoice['date']}<br/>Due: {invoice['due_date']}", style_right)],
    ]
    header_table = Table(header_data, colWidths=[10*cm, 7*cm])
    header_table.setStyle(TableStyle([
        ("VALIGN",      (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.4*cm))

    # ── Divider ──────────────────────────────
    divider = Table([[""]], colWidths=[17*cm], rowHeights=[1])
    divider.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 1, colors.HexColor("#DDDDDD"))]))
    story.append(divider)
    story.append(Spacer(1, 0.4*cm))

    # ── From / To block ─────────────────────
    from_block = (
        f"<b>FROM</b><br/>"
        f"{invoice['from']['name']}<br/>"
        f"{invoice['from']['address']}<br/>"
        f"{invoice['from']['email']}<br/>"
        f"{invoice['from']['website']}"
    )
    to_block = (
        f"<b>TO</b><br/>"
        f"{invoice['to']['name']}<br/>"
        f"{invoice['to']['address']}<br/>"
        f"{invoice['to']['email']}"
    )
    from_to = Table(
        [[Paragraph(from_block, style_note), Paragraph(to_block, style_note)]],
        colWidths=[8.5*cm, 8.5*cm]
    )
    from_to.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(from_to)
    story.append(Spacer(1, 0.6*cm))

    # ── Items table ─────────────────────────
    item_header = ["Description", "Qty", "Rate", "Amount"]
    item_rows   = [item_header]

    for item in invoice["items"]:
        amount = item["qty"] * item["rate"]
        item_rows.append([
            item["description"],
            str(item["qty"]),
            f"{cur}{item['rate']:,.2f}",
            f"{cur}{amount:,.2f}",
        ])

    # Subtotal / Tax / Total rows
    item_rows.append(["", "", "Subtotal",  f"{cur}{subtotal:,.2f}"])
    if tax > 0:
        item_rows.append(["", "", "Tax",   f"{cur}{tax:,.2f}"])
    item_rows.append(["", "", "TOTAL DUE", f"{cur}{total:,.2f}"])

    col_widths = [10*cm, 1.5*cm, 2.5*cm, 3*cm]
    items_table = Table(item_rows, colWidths=col_widths, repeatRows=1)

    n_items     = len(invoice["items"])
    total_rows  = len(item_rows)

    items_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",    (0, 0), (-1, 0),  colors.HexColor("#111111")),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  8),
        ("TOPPADDING",    (0, 0), (-1, 0),  8),
        # Item rows
        ("FONTSIZE",      (0, 1), (-1, n_items), 9),
        ("ROWBACKGROUNDS",(0, 1), (-1, n_items), [colors.white, colors.HexColor("#F9F9F9")]),
        ("BOTTOMPADDING", (0, 1), (-1, n_items), 6),
        ("TOPPADDING",    (0, 1), (-1, n_items), 6),
        # Summary rows (subtotal / tax / total)
        ("FONTSIZE",      (0, n_items+1), (-1, -1), 9),
        ("FONTNAME",      (0, total_rows-1), (-1, -1), "Helvetica-Bold"),
        ("TOPPADDING",    (0, n_items+1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, n_items+1), (-1, -1), 4),
        # Align amounts right
        ("ALIGN",         (1, 0), (-1, -1), "RIGHT"),
        # Total row highlight
        ("BACKGROUND",    (0, total_rows-1), (-1, -1), colors.HexColor("#F0F0F0")),
        ("LINEABOVE",     (0, total_rows-1), (-1, -1), 1, colors.HexColor("#CCCCCC")),
        # Outer border
        ("BOX",           (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("INNERGRID",     (0, 0), (-1, -1), 0.25, colors.HexColor("#E5E5E5")),
    ]))

    story.append(items_table)
    story.append(Spacer(1, 0.5*cm))

    # ── Notes ───────────────────────────────
    if invoice.get("notes"):
        story.append(Paragraph(f"<b>Notes:</b> {invoice['notes']}", style_note))

    doc.build(story)
    console.print(f"  [green]✔  PDF generated:[/green] [bold]{output_path}[/bold]")


# ─────────────────────────────────────────────
#  STEP 3 — SEND EMAIL WITH PDF ATTACHMENT
# ─────────────────────────────────────────────

def send_email(invoice: dict, pdf_path: str):
    """Send the invoice PDF to the client via Gmail SMTP."""
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        console.print("[bold red]✖  EMAIL_SENDER or EMAIL_PASSWORD missing in .env[/bold red]")
        raise SystemExit(1)

    recipient = invoice["to"]["email"]
    subject   = f"Invoice {invoice['number']} from {invoice['from']['name']}"
    body      = (
        f"Hi {invoice['to']['name']},\n\n"
        f"Please find your invoice {invoice['number']} attached.\n\n"
        f"Amount due: {invoice['currency']}{calculate_totals(invoice['items'])[2]:,.2f}\n"
        f"Due date:   {invoice['due_date']}\n\n"
        f"Thank you for your business.\n\n"
        f"Best regards,\n{invoice['from']['name']}\n{invoice['from']['website']}"
    )

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach PDF
    with open(pdf_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(pdf_path)}"')
    msg.attach(part)

    context = ssl.create_default_context(cafile=certifi.where())
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, recipient, msg.as_string())

    console.print(f"  [green]✔  Email sent →[/green] [bold]{recipient}[/bold]")


# ─────────────────────────────────────────────
#  STEP 4 — LOG TO CSV
# ─────────────────────────────────────────────

def log_invoice(invoice: dict, pdf_path: str, total: float):
    """Append a record of this invoice to the local log CSV."""
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "invoice_number", "client", "client_email",
            "currency", "total", "due_date", "pdf_file"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp":      datetime.now().strftime("%Y-%m-%d %H:%M"),
            "invoice_number": invoice["number"],
            "client":         invoice["to"]["name"],
            "client_email":   invoice["to"]["email"],
            "currency":       invoice["currency"],
            "total":          f"{total:.2f}",
            "due_date":       invoice["due_date"],
            "pdf_file":       pdf_path,
        })

    console.print(f"  [green]✔  Logged →[/green] [bold]{LOG_FILE}[/bold]")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    subtotal, tax, total = calculate_totals(INVOICE["items"])
    pdf_filename = f"invoice_{INVOICE['number']}_{INVOICE['to']['name'].replace(' ', '_')}.pdf"

    console.print(Panel(
        f"[bold white]FOMAD Invoice Generator + Sender[/bold white]\n"
        f"[dim]Invoice :[/dim] [cyan]{INVOICE['number']}[/cyan]\n"
        f"[dim]Client  :[/dim] [cyan]{INVOICE['to']['name']}[/cyan]  [dim]({INVOICE['to']['email']})[/dim]\n"
        f"[dim]Total   :[/dim] [cyan]{INVOICE['currency']}{total:,.2f}[/cyan]\n"
        f"[dim]Due     :[/dim] [cyan]{INVOICE['due_date']}[/cyan]",
        border_style="bright_blue",
        padding=(0, 2),
    ))

    # Preview line items in terminal
    console.print(Rule("[bold bright_blue]Invoice Summary[/bold bright_blue]"))
    preview = RichTable(box=rich_box.SIMPLE, show_header=True, header_style="bold white")
    preview.add_column("Description", style="white")
    preview.add_column("Qty",    justify="right", style="cyan")
    preview.add_column("Rate",   justify="right", style="cyan")
    preview.add_column("Amount", justify="right", style="bold green")
    for item in INVOICE["items"]:
        preview.add_row(
            item["description"],
            str(item["qty"]),
            f"{INVOICE['currency']}{item['rate']:,.2f}",
            f"{INVOICE['currency']}{item['qty'] * item['rate']:,.2f}",
        )
    console.print(preview)
    console.print(f"  [dim]Subtotal:[/dim] {INVOICE['currency']}{subtotal:,.2f}")
    if tax > 0:
        console.print(f"  [dim]Tax     :[/dim] {INVOICE['currency']}{tax:,.2f}")
    console.print(f"  [bold white]Total   : {INVOICE['currency']}{total:,.2f}[/bold white]")

    # 1 — Generate PDF
    console.print(Rule("[bold bright_blue][1/3] Generating PDF[/bold bright_blue]"))
    generate_pdf(INVOICE, pdf_filename)

    # 2 — Send email
    console.print(Rule("[bold bright_blue][2/3] Sending email[/bold bright_blue]"))
    send_email(INVOICE, pdf_filename)

    # 3 — Log
    console.print(Rule("[bold bright_blue][3/3] Logging invoice[/bold bright_blue]"))
    log_invoice(INVOICE, pdf_filename, total)

    console.print(
        Panel(
            f"[bold green]Invoice sent![/bold green]\n"
            f"[dim]PDF     :[/dim] [white]{pdf_filename}[/white]\n"
            f"[dim]Log     :[/dim] [white]{LOG_FILE}[/white]",
            border_style="green",
            padding=(0, 2),
        )
    )


if __name__ == "__main__":
    main()
