#!/usr/bin/env bash
set -euo pipefail

mkdir -p data
rm -f data/bluexprice_demo.db

sqlite3 data/bluexprice_demo.db < sql/01_setup_demo.sql
sqlite3 data/bluexprice_demo.db < sql/02_analysis_views.sql
sqlite3 data/bluexprice_demo.db < sql/export_outputs.sql

printf '%s\n' "SQL analysis complete: data/*.csv"

