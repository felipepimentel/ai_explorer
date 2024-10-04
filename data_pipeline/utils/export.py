import json
import csv
import pickle

def export_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def export_csv(data, file_path):
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def export_pickle(data, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

def export_data(data, file_path, format='json'):
    if format == 'json':
        export_json(data, file_path)
    elif format == 'csv':
        export_csv(data, file_path)
    elif format == 'pickle':
        export_pickle(data, file_path)
    else:
        raise ValueError(f"Unsupported export format: {format}")