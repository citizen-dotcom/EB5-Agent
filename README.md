# EB-5 Agent

The EB‑5 Agent automates the creation of flow‑of‑funds compliance artifacts for EB‑5 cases at our firm. It pulls transactions and assets from our case database, builds a Lucidchart flow diagram, and generates a Flow of Funds DOCX with dates, amounts, and bank account last‑4 digits where available. It can optionally extract the passport name via OCR if the name isn’t indexed.

This tool is designed for coworkers in our legal/compliance workflows. It expects certain preprocessed data and follows our internal Windows folder conventions.

---

## What the EB-5 Agent produces

- Flow of Funds DOCX (narrative)
- Lucidchart flow diagram (optional; requires API key)
  - Employment/Business Income → Green
  - Loan → Yellow/Orange
  - Gift → Purple
  - Escrow/Combined → White (no fill)
  - All other/unknown categories → White (no fill, “no color”)

---

## Preprocessed data expectations (workplace standards)

The EB‑5 Agent expects the following data to be available in our case database (pre-ingested by internal tooling or manual entry):

- `transactions` table:
  - Required: `case_id`, `date`, `amount`, `origin`, `destination`
  - Preferred: `origin_suffix` and `destination_suffix` (last 4 digits)
  - Optional: `category` (employment_income, business_income, loan, gift, combined), `memo`, `address` (institution/destination), `doc_id`
- `assets` table:
  - Required: `case_id`
  - Preferred: `address`, `type` (house, land, business), `source` (indexed, ocr, user_input), `doc_id`
- `passports` table:
  - Preferred: `case_id`, `name` (government name), `doc_id`
- `documents_raw` table:
  - Optional: `case_id`, `doc_id`, `type`, `storage_uri`, `ocr_text`, `parsed_fields` (JSON as text)

If a required value is missing (e.g., property address), the EB‑5 Agent can:
- Attempt extraction from available documents.
- Prompt the user to provide it and remember that fact for the case.

---

## Windows client folders and file search

The EB‑5 Agent automatically searches your Windows computer for client files; you don’t need to manually provide file paths.

- Folder convention:
  - Each client has a folder named after them (e.g., `John_Doe`).
  - Place all case files (passport scans, mortgage docs, bank statements) inside this folder.

- Supported locations:
  - Local: `C:\Users\<YourName>\Documents\eb5\<ClientName>\`
  - Dropbox (synced locally): `C:\Users\<YourName>\Dropbox\eb5\<ClientName>\`

- File detection:
  - Passport: filenames containing `passport` (jpg, jpeg, png, pdf)
  - Mortgage/property: filenames containing `mortgage`, `property`, or `deed`
  - Bank statements: filenames containing `bank`, `statement`, or `account`

The agent indexes discovered files (as needed) into the database and uses them for the diagram and DOCX.

---

## Getting started on Windows

1. Install Python 3.10+ from python.org.
2. Clone or download this repository to your computer.
3. Open a terminal (PowerShell) in the project folder.
4. Install dependencies:


## Initializing the database on Windows

The EB‑5 Agent uses Python’s built‑in sqlite3 library, so you don’t need the sqlite3.exe tool.

To initialize the schema:

1. Run the helper script: