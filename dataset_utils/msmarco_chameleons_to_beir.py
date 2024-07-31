import os
import json
import pandas as pd

base_path = os.getcwd()
datasets = ["Lesser(common6)", "Pygmy(common5)", "Veiled(common4)"]
datasets_path = os.path.join(base_path, "dataset_utils", "Chameleons", "datasets")
output_path = os.path.join(base_path, "dataset_utils", "beir_data")

if not os.path.exists(datasets_path):
    raise FileNotFoundError(f"Dataset path not found: {datasets_path}")

os.makedirs(output_path, exist_ok=True)

def load_and_concatenate_tsvs(directory, prefix):
    all_data = pd.DataFrame()
    for file_name in os.listdir(directory):
        if file_name.startswith(prefix):
            file_path = os.path.join(directory, file_name)
            print(f"Reading file: {file_path}")
            data = pd.read_csv(file_path, sep='\t', header=None, names=['id', 'text'])
            data['doc_id'] = data['id'].apply(lambda x: x.split('|')[1] if '|' in str(x) else x)
            print(f"Loaded {len(data)} rows from {file_name}")
            all_data = pd.concat([all_data, data], ignore_index=True)
    return all_data

def convert_to_beir(dataset_path):
    beir_data = {
        "corpus": {},
        "queries": {},
        "qrels": {}
    }

    doc_data = load_and_concatenate_tsvs(dataset_path, "")
    if not doc_data.empty:
        for _, row in doc_data.iterrows():
            doc_id = str(row['doc_id'])
            beir_data["corpus"][doc_id] = {
                'title': '',
                'text': row['text']
            }
        print(f"Loaded {len(beir_data['corpus'])} documents from {dataset_path}")
    else:
        print(f"No documents loaded from {dataset_path}")

    query_data = load_and_concatenate_tsvs(dataset_path, "")
    if not query_data.empty:
        for _, row in query_data.iterrows():
            query_id = str(row['doc_id'])
            beir_data["queries"][query_id] = row['text']
        print(f"Loaded {len(beir_data['queries'])} queries from {dataset_path}")
    else:
        print(f"No queries loaded from {dataset_path}")

    qrels_data = load_and_concatenate_tsvs(dataset_path, "")
    if not qrels_data.empty:
        for _, row in qrels_data.iterrows():
            query_id = str(row['id'])
            doc_id = str(row['doc_id'])
            relevance = 1 
            if query_id not in beir_data["qrels"]:
                beir_data["qrels"][query_id] = {}
            beir_data["qrels"][query_id][doc_id] = relevance
        print(f"Loaded qrels for {len(beir_data['qrels'])} queries from {dataset_path}")
    else:
        print(f"No qrels loaded from {dataset_path}")

    return beir_data

def save_beir_format(output_path, dataset_name, beir_data):
    dataset_output_path = os.path.join(output_path, f"{dataset_name}.json")
    with open(dataset_output_path, 'w') as file:
        json.dump(beir_data, file, indent=4)
    print(f"Saved BEIR format data to {dataset_output_path}")

for dataset_name in datasets:
    dataset_path = os.path.join(datasets_path, dataset_name)
    print(f"Processing dataset: {dataset_name}")
    beir_data = convert_to_beir(dataset_path)
    save_beir_format(output_path, dataset_name, beir_data)
