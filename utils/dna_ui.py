#!/usr/bin/env python3
import os
import json
import csv
from dna_calculator import DNACalculator, RuleParseError

def ensure_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)

def read_input_file(input_path):
    """
    Reads `toSequence.txt` under data/raw; each line is one DNA string.
    Returns a list of DNA strings (stripped, non-empty).
    """
    dna_list = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s:
                dna_list.append(s)
    return dna_list

def flatten_parsed(rule_name, values_dict, parent_key=''):
    """
    Given nested values_dict, flatten into { 'rule.sub1.sub2': value, ... }.
    Useful for CSV.
    """
    items = {}
    for k, v in values_dict.items():
        new_key = f"{parent_key}.{k}" if parent_key else f"{rule_name}.{k}"
        if isinstance(v, dict):
            items.update(flatten_parsed(rule_name, v, new_key))
        else:
            items[new_key] = v
    return items

def main():
    # Determine file paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    raw_folder = os.path.join(project_root, 'data', 'raw')
    output_folder = os.path.join(project_root, 'data', 'output')
    ensure_folder(output_folder)

    input_file = os.path.join(raw_folder, 'toSequence.txt')
    if not os.path.isfile(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        return

    # Instantiate calculator
    try:
        calculator = DNACalculator(rules_folder=os.path.join(project_root, 'rules'))
    except Exception as e:
        print(f"[ERROR] Could not load rules: {e}")
        return

    # Read DNA strings
    dna_list = read_input_file(input_file)
    if not dna_list:
        print("[WARN] No DNA strings found in toSequence.txt")
        return

    # Prepare outputs
    parsed_json = []
    csv_rows = []
    all_flattened_keys = set()

    for dna_str in dna_list:
        try:
            result = calculator.parse(dna_str)
            entry = {
                'dna': dna_str,
                'rule': result['rule'],
                'parsed': result['values']
            }
            parsed_json.append(entry)

            # Flatten for CSV
            flat = flatten_parsed(result['rule'], result['values'])
            flat['dna'] = dna_str
            flat['rule'] = result['rule']
            csv_rows.append(flat)
            all_flattened_keys.update(flat.keys())

        except RuleParseError as e:
            # On parse error, record as error entry
            parsed_json.append({
                'dna': dna_str,
                'error': str(e)
            })
            # Also put a row in CSV listing error
            flat = {'dna': dna_str, 'error': str(e)}
            csv_rows.append(flat)
            all_flattened_keys.update(flat.keys())

    # 1) Write JSON output
    json_output_path = os.path.join(output_folder, 'toSequence_parsed.json')
    with open(json_output_path, 'w', encoding='utf-8') as jf:
        json.dump(parsed_json, jf, indent=2)

    # 2) Write CSV output
    csv_output_path = os.path.join(output_folder, 'toSequence_parsed.csv')
    fieldnames = sorted(all_flattened_keys)
    with open(csv_output_path, 'w', newline='', encoding='utf-8') as cf:
        writer = csv.DictWriter(cf, fieldnames=fieldnames)
        writer.writeheader()
        for row in csv_rows:
            # Ensure every field in fieldnames
            out = {k: row.get(k, '') for k in fieldnames}
            writer.writerow(out)

    print(f"[OK] Parsed {len(dna_list)} DNA strings.")
    print(f"     JSON → {json_output_path}")
    print(f"     CSV  → {csv_output_path}")

if __name__ == '__main__':
    main()
