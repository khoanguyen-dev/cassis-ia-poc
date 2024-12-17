import pandas as pd
from sqlalchemy import create_engine, text
import os

# Constants
USERNAME = "khoa"
PASSWORD = "k123"
DATABASE = "cassis_ia"
HOST = "localhost"
PORT = "5432"
CSV_FILE = "data/initial_data.csv"

# SQL queries
CHECK_CASSIS_IA_DB = f"""
SELECT 1 FROM pg_database WHERE datname = '{DATABASE}';
"""

CREATE_CASSIS_IA_DB = f"""
CREATE DATABASE {DATABASE};
"""

CHECK_ANNUAIRE_TABLE = f"""
SELECT EXISTS (
    SELECT FROM pg_tables
    WHERE schemaname = 'public'
    AND tablename = 'annuaire'
);
"""

# Helper function to run a query directly in PostgreSQL
def execute_query(engine, query, success_msg, error_msg):
    try:
        with engine.connect() as connection:
            connection.execute(text(query))
        print(success_msg)
    except Exception as e:
        print(f"{error_msg}: {e}")

# Main script
def main():
    # Connect to the default postgres database to check/create cassis_ia
    default_engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/postgres")
    with default_engine.connect() as connection:
        db_exists = connection.execute(text(CHECK_CASSIS_IA_DB)).scalar()
        if not db_exists:
            print(f"Database '{DATABASE}' does not exist. Creating...")
            connection.execute(text(CREATE_CASSIS_IA_DB))
            print(f"Database '{DATABASE}' created successfully.")
        else:
            print(f"Database '{DATABASE}' already exists.")

    # Connect to the cassis_ia database
    engine = create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

    # Check if the 'annuaire' table exists, and create it if not
    with engine.connect() as connection:
        table_exists = connection.execute(text(CHECK_ANNUAIRE_TABLE)).scalar()
        if not table_exists:
            print("Table 'annuaire' does not exist. Creating...")
            # Create the 'annuaire' table if it doesn't exist
            create_table_query = """
            CREATE TABLE annuaire (
                numero SERIAL PRIMARY KEY,
                type_de_partenaire VARCHAR(50),
                personnalite_juridique VARCHAR(50),
                type_de_fournisseur VARCHAR(50),
                nom VARCHAR(100),
                prenom VARCHAR(100),
                voie VARCHAR(200),
                complement VARCHAR(100),
                npa INTEGER,
                localite VARCHAR(100),
                pays VARCHAR(50),
                telephone VARCHAR(15),
                portable VARCHAR(15),
                courriel VARCHAR(100),
                site_web VARCHAR(100),
                activite_specialite TEXT,
                medecin BOOLEAN,
                medecin_intra_hospitalier BOOLEAN,
                horaires_ouverture TEXT,
                coord_geo_nord NUMERIC,
                coord_geo_est NUMERIC,
                coord_geo_long NUMERIC,
                coord_geo_lat NUMERIC,
                besoin_convention BOOLEAN,
                type_de_convention VARCHAR(100),
                date_convention_soumise DATE,
                date_convention_valide_recue DATE,
                date_derniere_modification DATE,
                date_saisie DATE,
                date_dernier_appel_actualisation DATE,
                date_derniere_modif DATE
            );
            """
            connection.execute(text(create_table_query))
            print("Table 'annuaire' created successfully.")
        else:
            print("Table 'annuaire' already exists.")

    # Load CSV data into a DataFrame
    if not os.path.exists(CSV_FILE):
        print(f"CSV file '{CSV_FILE}' not found. Exiting.")
        return

    print(f"Loading data from '{CSV_FILE}'...")
    df = pd.read_csv(CSV_FILE)

    # Rename columns to match the database schema
    column_mapping = {
        "Numéro": "numero",
        "Type de partenaire": "type_de_partenaire",
        "Personnalité juridique": "personnalite_juridique",
        "Type de fournisseur": "type_de_fournisseur",
        "Nom": "nom",
        "Prénom": "prenom",
        "Voie": "voie",
        "Complément": "complement",
        "NPA": "npa",
        "Localité": "localite",
        "Pays": "pays",
        "N° de téléphone": "telephone",
        "N° de portable": "portable",
        "Courriel": "courriel",
        "Site web": "site_web",
        "Activité et éventuelle(s) spécialité(s)": "activite_specialite",
        "Médecin": "medecin",
        "Médecin intra-hospitalier": "medecin_intra_hospitalier",
        "Horaires d’ouverture": "horaires_ouverture",
        "Coordonnées de géolocalisation long.": "coord_geo_long",
        "Coordonnées de géolocalisation lat.": "coord_geo_lat",
        "Coordonnées de géolocalisation Nord": "coord_geo_nord",
        "Coordonnées de géolocalisation Est": "coord_geo_est",
        "Besoin d'une convention": "besoin_convention",
        "Type de convention": "type_de_convention",
        "Date convention soumise": "date_convention_soumise",
        "Date convention valide reçue": "date_convention_valide_recue",
        "Date dernière modification": "date_derniere_modification",
        "Date de saisie": "date_saisie",
        "Date du dernier appel à actualisation des données": "date_dernier_appel_actualisation",
        "Date de dernière modification": "date_derniere_modif"
    }
    df.rename(columns=column_mapping, inplace=True)

    # Convert "Oui" and "Non" to boolean (True/False) for the relevant columns
    bool_columns = ['medecin', 'medecin_intra_hospitalier', 'besoin_convention']
    for column in bool_columns:
        if column in df.columns:
            df[column] = df[column].map({'Oui': True, 'Non': False})

    # Insert data into the 'annuaire' table
    try:
        df.to_sql('annuaire', engine, if_exists='append', index=False)
        print(f"Data successfully inserted into 'annuaire' table.")
    except Exception as e:
        print(f"Failed to insert data into 'annuaire': {e}")

if __name__ == "__main__":
    main()
    