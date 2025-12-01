# Purpose: Orchestrate the EB-5 Agent (Files → SQL → Lucidchart → DOCX) and handle OCR/memory prompts.
import os
from .config import settings
from .db import connect, fetch_transactions, fetch_assets, fetch_passport_name, upsert_passport_name
from .lucid import create_document, add_shape, add_connector
from .flow import build_label, infer_category
from .docx_gen import generate_flow_doc
from .ocr import extract_passport_name
from .memory import memory
from .files import find_client_files, find_passport_file

def _group_sources(transactions):
    """Create source summaries (amount totals and date ranges) grouped by category."""
    by_cat = {}
    for t in transactions:
        cat = t.get("category") or infer_category(t)
        by_cat.setdefault(cat, []).append(t)
    sources = []
    for cat, txns in by_cat.items():
        label = cat.replace("_", " ").title()
        amt = sum([x["amount"] for x in txns])
        dates = [x["date"] for x in txns if x.get("date")]
        dr = (min(dates), max(dates)) if dates else None
        sources.append({"label": label, "source_type": cat, "target_amount": amt, "date_range": dr})
    return sources

def run(case_id: str, client_name: str, project_name: str):
    """Run EB-5 Agent for a case: find files, fetch data, build diagram, generate DOCX, OCR/memory as needed."""
    # 1) Connect DB
    conn = connect(settings.DB_PATH)

    # 2) Auto-find client files on Windows (Documents\\eb5 and Dropbox\\eb5)
    files = find_client_files(client_name)

    # 3) Passport name with OCR fallback (only if not indexed and a passport file is found)
    passport_name, doc_id = fetch_passport_name(conn, case_id)
    if not passport_name:
        passport_file = find_passport_file(files)
        if passport_file:
            name, ocr_text = extract_passport_name(passport_file)
            upsert_passport_name(conn, case_id, name, doc_id="PASS_"+case_id, storage_uri=passport_file, ocr_text=ocr_text)
            passport_name = name

    # 4) Fetch transactions and assets
    transactions = fetch_transactions(conn, case_id)
    assets = fetch_assets(conn, case_id)

    # 5) Build Lucidchart flow (optional: only if API key is set)
    doc_id = None
    if settings.LUCID_API_KEY:
        doc_id = create_document(f"{case_id} – Flow of Funds")
        x, y = 100, 100
        source_shape_ids = []
        for t in transactions:
            base = f"{t['origin']} → {t['destination']} (${t['amount']:,})"
            suffix = t.get("destination_suffix") or t.get("origin_suffix")
            label = build_label(base=base, suffix=suffix, address=t.get("address"))
            cat = infer_category(t)
            sid = add_shape(doc_id, label, cat, x=x, y=y)
            source_shape_ids.append(sid)
            y += 130

        # Escrow node (white/no fill). Store escrow address in your DB if available.
        escrow_address = None
        if transactions:
            escrow_address = transactions[0].get("escrow_address")
        escrow_id = add_shape(doc_id, build_label("EB-5 Escrow Account", address=escrow_address), "combined", x=480, y=300)

        for sid in source_shape_ids:
            add_connector(doc_id, sid, escrow_id)
        print(f"Lucidchart diagram created: https://lucidchart.com/documents/view/{doc_id}")
    else:
        print("No Lucidchart API key provided. Skipping diagram creation.")

    # 6) Generate Flow of Funds DOCX
    sources = _group_sources(transactions)
    docx_path = generate_flow_doc(case_id, client_name, project_name, sources, transactions)
    print(f"Flow of Funds DOCX generated: {docx_path}")

    # 7) Memory prompts for missing asset addresses (simple example)
    case_facts = memory.get_case(case_id)
    known_addresses = case_facts.get("asset_addresses")
    if not known_addresses and not assets:
        print("Missing asset addresses. Please provide any property/asset addresses for this case.")
    elif assets:
        memory.upsert_case_fact(case_id, "asset_addresses", [a["address"] for a in assets if a.get("address")])

if __name__ == "__main__":
    # Simple env-driven CLI; replace with argparse for more control if desired
    case_id = os.getenv("CASE_ID", "SampleCase")
    client_name = os.getenv("CLIENT_NAME", "John_Doe")
    project_name = os.getenv("PROJECT_NAME", "Example Project")
    run(case_id, client_name, project_name)