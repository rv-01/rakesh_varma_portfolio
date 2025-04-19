Metadata Extraction Kit

How to Run:
------------
1. Ensure you have Python 3 installed.
2. Install dependencies (if not already installed):
   (no external libraries needed, standard Python modules only)

3. Folder structure:
    ├── config.json
    ├── extract_metadata.py
    ├── test_sql_scripts/
    │     ├── 01_create_table_customer.sql
    │     ├── 02_create_table_orders.sql
    │     ├── 03_create_view_customer_summary.sql
    │     ├── 04_create_table_customer_duplicate.sql

4. Open terminal, navigate to the folder, and run:
   python extract_metadata.py

5. Output:
   After running, outputs will be created in 'sample_output/' folder:
    - tables_metadata.json
    - views_metadata.json
    - errors_metadata.json
    - tables_metadata.csv
    - views_metadata.csv
    - errors_metadata.csv

6. Field Order:
   Configurable via 'config.json'

Notes:
- Duplicates are caught automatically and written to errors_metadata files.
- Both JSON and CSV outputs are generated.
- Field order is strictly controlled based on config.json.

Enjoy!
