-- Purpose: Canonical schema for transactions, assets, passports, and raw documents.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS transactions (
  txn_id INTEGER PRIMARY KEY,
  case_id VARCHAR(128),
  date DATE,
  amount DECIMAL(12,2),
  currency VARCHAR(8),
  origin TEXT,
  origin_suffix VARCHAR(4),        -- last 4 digits
  destination TEXT,
  destination_suffix VARCHAR(4),   -- last 4 digits
  category TEXT,                   -- employment_income, business_income, loan, gift, combined
  memo TEXT,
  doc_id VARCHAR(64),
  address TEXT                     -- optional: institution/destination address
);

CREATE TABLE IF NOT EXISTS assets (
  asset_id VARCHAR(64) PRIMARY KEY,
  case_id VARCHAR(128) NOT NULL,
  type VARCHAR(64),                -- house, land, business, vehicle
  address TEXT,
  doc_id VARCHAR(64),
  source VARCHAR(64),              -- indexed, ocr, user_input
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS passports (
  case_id VARCHAR(128) PRIMARY KEY,
  name TEXT,
  doc_id VARCHAR(64),
  storage_uri TEXT,
  ocr_text TEXT
);

CREATE TABLE IF NOT EXISTS documents_raw (
  doc_id VARCHAR(64) PRIMARY KEY,
  case_id VARCHAR(128),
  type VARCHAR(64),         -- passport, birth_certificate, visa
  storage_uri TEXT,
  ocr_text TEXT,
  parsed_fields TEXT,       -- JSON as text
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);