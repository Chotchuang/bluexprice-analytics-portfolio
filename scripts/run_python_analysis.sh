#!/usr/bin/env bash
set -euo pipefail

bash scripts/run_sql_analysis.sh
python -m python_analysis.run_analysis
python scripts/build_python_notebook.py

printf '%s\n' "Python analysis complete: notebooks/ and reports/python/"

