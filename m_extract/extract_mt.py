import os
import re
import json
import csv
from collections import defaultdict, OrderedDict

# Metadata Stores
tables_metadata = defaultdict(dict)
views_metadata = defaultdict(list)
errors_metadata = defaultdict(list)

# Unique keys tracking
seen_keys = set()

# Default DB and Schema
DEFAULT_DB = "DEFAULT_DB"
DEFAULT_SCHEMA = "DEFAULT_SCHEMA"

# Regex Patterns
create_table_pattern = re.compile(r"CREATE\s+TABLE\s+(\w+)", re.IGNORECASE)
create_view_pattern = re.compile(r"CREATE\s+VIEW\s+(\w+)", re.IGNORECASE)
column_def_pattern = re.compile(r"(\w+)\s+(\w+)(?:\((\d+)\))?\s*(NOT NULL|NULL)?", re.IGNORECASE)
select_from_pattern = re.compile(r"SELECT\s+(.*?)\s+FROM\s+(\w+)", re.IGNORECASE | re.DOTALL)

def create_key(db_name, schema_name, table_name, column_name):
    return f"{db_name}.{schema_name}.{table_name}.{column_name}"

def order_dict(d, field_order):
    """Reorder dictionary based on field order"""
    return OrderedDict((field, d.get(field, "")) for field in field_order)

def save_ordered_json(output_dir, name, data, field_order):
    """Save reordered JSON file"""
    ordered_data = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                ordered_data[key] = {k: order_dict(v, field_order) for k, v in value.items()}
            elif isinstance(value, list):
                ordered_data[key] = [order_dict(item, field_order) for item in value]
            else:
                ordered_data[key] = value
    elif isinstance(data, list):
        ordered_data = [order_dict(item, field_order) for item in data]
    else:
        ordered_data = data

    with open(os.path.join(output_dir, f"{name}.json"), "w") as f:
        json.dump(ordered_data, f, indent=4)

    # Also save as CSV
    if isinstance(ordered_data, dict):
        rows = []
        for key, value in ordered_data.items():
            if isinstance(value, list):
                rows.extend(value)
            else:
                rows.append(value)
    else:
        rows = ordered_data

    if rows:
        csv_file = os.path.join(output_dir, f"{name}.csv")
        with open(csv_file, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_order)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

def process_create_table(statement):
    match = create_table_pattern.search(statement)
    if match:
        table_name = match.group(1).upper()
        body = statement.split('(', 1)[1].rsplit(')', 1)[0]
        lines = body.split(',')
        for line in lines:
            line = line.strip()
            col_match = column_def_pattern.match(line)
            if col_match:
                column_name = col_match.group(1).upper()
                data_type = col_match.group(2).upper()
                data_length = col_match.group(3) or ''
                nullable = 'NO' if col_match.group(4) and 'NOT NULL' in col_match.group(4).upper() else 'YES'
                key = create_key(DEFAULT_DB, DEFAULT_SCHEMA, table_name, column_name)
                value = {
                    'db_name': DEFAULT_DB,
                    'schema_name': DEFAULT_SCHEMA,
                    'table_name': table_name,
                    'column_name': column_name,
                    'data_type': data_type,
                    'data_length': data_length,
                    'nullable': nullable,
                    'primary_key': 'NO'
                }
                if key not in seen_keys:
                    tables_metadata[table_name][column_name] = value
                    seen_keys.add(key)
                else:
                    errors_metadata['tables'].append(value)

def process_create_view(statement):
    match = create_view_pattern.search(statement)
    if match:
        view_name = match.group(1).upper()
        select_match = select_from_pattern.search(statement)
        if select_match:
            select_part = select_match.group(1)
            source_table = select_match.group(2).upper()
            select_columns = [col.strip() for col in select_part.split(',')]
            for col in select_columns:
                if " AS " in col.upper():
                    source_col, alias = re.split(r'\s+AS\s+', col, flags=re.IGNORECASE)
                    source_col = source_col.strip()
                    alias = alias.strip()
                else:
                    source_col = alias = col.strip()
                key = create_key(DEFAULT_DB, DEFAULT_SCHEMA, view_name, alias.upper())
                value = {
                    'db_name': DEFAULT_DB,
                    'schema_name': DEFAULT_SCHEMA,
                    'view_name': view_name,
                    'column_name': alias.upper(),
                    'source_table': source_table,
                    'source_column': source_col.upper()
                }
                if key not in seen_keys:
                    views_metadata[view_name].append(value)
                    seen_keys.add(key)
                else:
                    errors_metadata['views'].append(value)

def resolve_view_metadata():
    resolved_views = defaultdict(list)
    for view_name, columns in views_metadata.items():
        for col in columns:
            source_table = col['source_table']
            source_column = col['source_column']
            metadata = tables_metadata.get(source_table, {}).get(source_column)
            if metadata:
                resolved_col = {
                    **col,
                    'data_type': metadata['data_type'],
                    'data_length': metadata['data_length']
                }
            else:
                resolved_col = {
                    **col,
                    'data_type': 'UNKNOWN',
                    'data_length': ''
                }
            resolved_views[view_name].append(resolved_col)
    return resolved_views

def process_sql_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.sql'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                sql_content = file.read()
                statements = sql_content.split(';')
                for statement in statements:
                    statement = statement.strip()
                    if statement.upper().startswith('CREATE TABLE'):
                        process_create_table(statement)
                    elif statement.upper().startswith('CREATE VIEW'):
                        process_create_view(statement)

def main(folder_path, output_dir):
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    process_sql_files(folder_path)
    resolved_views = resolve_view_metadata()

    # Save outputs
    save_ordered_json(output_dir, "tables_metadata", tables_metadata, config["table_fields_order"])
    save_ordered_json(output_dir, "views_metadata", resolved_views, config["view_fields_order"])
    save_ordered_json(output_dir, "errors_metadata", errors_metadata, config["error_fields_order"])

    print(f"Metadata extraction completed. Files saved to {output_dir}")

if __name__ == "__main__":
    folder = "test_sql_scripts"     # Your SQL files folder
    output = "sample_output"         # Output folder
    main(folder, output)
