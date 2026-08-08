import pandas as pd
from datetime import datetime

def load_data(clients_path, properties_path):
    clients = pd.read_csv(clients_path)
    properties = pd.read_csv(properties_path)
    return clients, properties

def clean_clients(clients):
    clients = clients.drop_duplicates()

    categorical_cols = [
        "client_type",
        "gender",
        "country",
        "region",
        "acquisition_purpose",
        "loan_applied",
        "referral_channel"
    ]

    for col in categorical_cols:
        clients[col] = (
            clients[col]
            .astype(str)
            .str.strip()
            .str.title()
        )

    clients["date_of_birth"] = pd.to_datetime(
        clients["date_of_birth"],
        errors="coerce"
    )

    current_year = datetime.now().year
    clients["age"] = current_year - clients["date_of_birth"].dt.year

    clients = clients[
        (clients["age"] >= 18) &
        (clients["age"] <= 100)
    ]

    return clients

def clean_properties(properties):
    properties = properties.drop_duplicates()
    return properties

def merge_datasets(clients, properties):
    buyer_master = properties.merge(
        clients,
        left_on="client_ref",
        right_on="client_id",
        how="left"
    )
    return buyer_master

def save_processed_data(df, output_path):
    df.to_csv(output_path, index=False)

def run_pipeline():
    clients, properties = load_data(
        "data/raw/clients.csv",
        "data/raw/properties.csv"
    )

    clients = clean_clients(clients)
    properties = clean_properties(properties)

    buyer_master = merge_datasets(clients, properties)

    save_processed_data(
        buyer_master,
        "data/processed/buyer_master_dataset.csv"
    )

    print("Pipeline completed successfully.")
    print(f"Final dataset shape: {buyer_master.shape}")

if __name__ == "__main__":
    run_pipeline()