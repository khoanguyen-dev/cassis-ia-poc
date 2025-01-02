from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from llama_index.llms.openai import OpenAI
from llama_index.program.openai import OpenAIPydanticProgram
from typing import List, Optional
from datetime import datetime
import os
import psycopg2
import pandas as pd

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize the LlamaIndex LLM
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

llm = OpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Define Pydantic models for structured data with descriptions
class AnnuaireEntry(BaseModel):
    """Model representing an entry for the Annuaire database."""
    numero: Optional[int]
    type_de_partenaire: Optional[str]
    personnalite_juridique: Optional[str]
    type_de_fournisseur: Optional[str]
    nom: str
    prenom: str
    voie: Optional[str]
    complement: Optional[str]
    npa: Optional[int]
    localite: Optional[str]
    pays: Optional[str]
    telephone: Optional[str]
    portable: Optional[str]
    courriel: Optional[str]
    site_web: Optional[str]
    activite_specialite: Optional[str]
    medecin: Optional[bool]
    medecin_intra_hospitalier: Optional[bool]
    horaires_ouverture: Optional[str]
    coord_geo_nord: Optional[float]
    coord_geo_est: Optional[float]
    coord_geo_long: Optional[float]
    coord_geo_lat: Optional[float]
    besoin_convention: Optional[bool]
    type_de_convention: Optional[str]
    date_convention_soumise: Optional[str]
    date_convention_valide_recue: Optional[str]
    date_derniere_modification: Optional[str]
    date_saisie: Optional[str]
    date_dernier_appel_actualisation: Optional[str]

class EvenementEntry(BaseModel):
    """Model representing an entry for the Evenement database."""
    numero: Optional[int]
    nom_evenement: str
    titre_evenement: Optional[str]
    date_debut: Optional[str]
    date_fin: Optional[str]
    horaire_debut: Optional[str]
    horaire_fin: Optional[str]
    texte_libre: Optional[str]
    court_descriptif: Optional[str]
    numero_partenaire: Optional[int]
    nom_partenaire: Optional[str]
    partenaire_de_la_selection: Optional[str]
    sites_originaux: Optional[str]
    date_creation: Optional[str]
    mode_creation: Optional[str]
    date_derniere_modification: Optional[str]
    mode_modification: Optional[str]
    id_dernier_modificateur: Optional[str]
    date_de_peremption: Optional[str]

class AnnuaireEntries(BaseModel):
    """Model representing multiple entries for the Annuaire database."""
    entries: List[AnnuaireEntry]

class EvenementEntries(BaseModel):
    """Model representing multiple entries for the Evenement database."""
    entries: List[EvenementEntry]

# Define Pydantic programs
annuaire_program = OpenAIPydanticProgram.from_defaults(
    output_cls=AnnuaireEntries,
    llm=llm,
    prompt_template_str="Extract structured data for AnnuaireEntries from the following text: {text_input}",
    verbose=True
)

evenement_program = OpenAIPydanticProgram.from_defaults(
    output_cls=EvenementEntries,
    llm=llm,
    prompt_template_str="Extract structured data for EvenementEntries from the following text: {text_input}",
    verbose=True
)

@app.route('/annuaire', methods=['GET'])
def get_annuaire():
    return fetch_table_entries("annuaire")

@app.route('/evenements', methods=['GET'])
def get_evenement_entries():
    return fetch_table_entries("evenement")

def fetch_table_entries(table_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return jsonify([dict(zip(column_names, row)) for row in rows])
    except Exception as e:
        import traceback
        print("Error occurred while fetching table entries:")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def scrape_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Visit the page
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded")  # Ensure basic page content is loaded

            # Optional: Click toggles/buttons to reveal hidden content
            try:
                # Adjust this selector to match elements that toggle hidden content
                toggles = page.query_selector_all("button, .toggle, [data-toggle]")
                for toggle in toggles:
                    if toggle.is_visible():  # Only click visible elements
                        toggle.click()
                        page.wait_for_timeout(100)  # Small delay for DOM updates
            except Exception as toggle_error:
                print(f"Error clicking toggles: {toggle_error}")

            # Wait for the main content to load
            try:
                page.wait_for_selector(".content-class", timeout=10000)  # Replace with actual content selector
            except Exception as wait_error:
                print(f"Content not found in time: {wait_error}")

            # Extract all visible text from the page
            content = page.evaluate("() => document.body.innerText")

            browser.close()
            return content
    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return None

@app.route('/process-annuaire', methods=['POST'])
def process_annuaire_input():
    return process_input("annuaire", annuaire_program)

@app.route('/process-evenement', methods=['POST'])
def process_evenement_input():
    return process_input("evenement", evenement_program)

def process_input(table_name, program):
    url = request.form.get('url', None)
    text_input = request.form.get('text', '')
    file = request.files.get('file')

    if url:
        # Scrape content if a URL is provided
        text_input = scrape_content(url)
        if not text_input:
            return jsonify({'error': 'Failed to scrape content from the provided URL'}), 400
    elif file:
        # Process the uploaded file
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                text_input = file.read().decode('utf-8')
                df = None

            if df is not None:
                text_input = df.to_json(orient='records')
        except Exception as e:
            return jsonify({'error': f"Failed to process file: {str(e)}"}), 400

    if not text_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        # Use Pydantic Program for structured extraction
        response = program(text_input=text_input)
        entries = response.entries
    except (ValidationError, Exception) as e:
        return jsonify({'error': f"Failed to process input: {str(e)}"}), 500

    conn = get_db_connection()
    cursor = conn.cursor()

    duplicates = []
    successful_inserts = []

    for entry in entries:
        try:
            entry_dict = entry.model_dump()  # Use Pydantic v2 `model_dump` to serialize data
            entry_dict.pop('numero', None)  # Ensure `numero` is excluded for new entries

            # Prepare the duplicate detection query
            if table_name == "annuaire":
                cursor.execute(
                    """
                    SELECT *
                    FROM annuaire
                    WHERE similarity(nom, %s) > 0.3 AND LEFT(prenom, 1) = LEFT(%s, 1);
                    """,
                    (entry_dict['nom'], entry_dict['prenom'])
                )
            elif table_name == "evenement":
                cursor.execute(
                    """
                    SELECT *
                    FROM evenement
                    WHERE similarity(nom_evenement, %s) > 0.3 AND LEFT(nom_evenement, 1) = LEFT(%s, 1);
                    """,
                    (entry_dict['nom_evenement'], entry_dict['nom_evenement'])
                )

            # Check for existing entries
            existing = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            close_matches = [dict(zip(column_names, row)) for row in existing]

            if close_matches:
                # Add to duplicates if matches found
                duplicates.append({
                    'new_entry': entry_dict,
                    'existing_entries': close_matches
                })
            else:
                # Insert into the database if no duplicates
                entry_dict['date_derniere_modification'] = datetime.now().strftime('%Y-%m-%d')
                columns = ', '.join(entry_dict.keys())
                values = ', '.join(['%s'] * len(entry_dict))
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({values}) RETURNING numero",
                    list(entry_dict.values())
                )
                new_numero = cursor.fetchone()[0]  # Fetch the new `numero`
                entry_dict['numero'] = new_numero  # Update entry with the generated `numero`
                successful_inserts.append(entry_dict)
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f"Database error: {str(e)}"}), 500

    # Commit changes to the database
    conn.commit()
    conn.close()

    # Construct the response
    response = {'message': 'Processing completed.', 'successful_inserts': successful_inserts}
    if duplicates:
        response['duplicates'] = duplicates

    # If duplicates exist, return a 409 status with duplicate details
    if duplicates:
        return jsonify(response), 409

    # Return success response if no duplicates
    return jsonify(response), 201

@app.route('/replace-annuaire', methods=['PUT'])
def replace_annuaire_entry():
    return replace_entry("annuaire")

@app.route('/replace-evenement', methods=['PUT'])
def replace_evenement_entry():
    return replace_entry("evenement")

def replace_entry(table_name):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        for entry in data:
            processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}
            if "numero" in processed_entry:
                cursor.execute(f"""
                    UPDATE {table_name}
                    SET {', '.join([f'{k} = %s' for k in processed_entry.keys() if k != 'numero'])},
                        date_derniere_modification = CURRENT_DATE
                    WHERE numero = %s
                """, list(processed_entry.values()) + [processed_entry['numero']])
            else:
                return jsonify({'error': "Missing 'numero' field for replacement"}), 400

        conn.commit()
        conn.close()
        return jsonify({'message': f'Entries in {table_name} replaced successfully'}), 200
    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500

@app.route('/add-annuaire', methods=['POST'])
def add_annuaire_entry():
    return add_entry("annuaire")

@app.route('/add-evenement', methods=['POST'])
def add_evenement_entry():
    return add_entry("evenement")

def add_entry(table_name):
    try:
        entry = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}
        processed_entry['date_derniere_modification'] = datetime.now().strftime('%Y-%m-%d')

        columns = ', '.join(processed_entry.keys())
        values = ', '.join(['%s'] * len(processed_entry))
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})", list(processed_entry.values()))

        conn.commit()
        conn.close()
        return jsonify({'message': f'Entry added to {table_name} successfully'}), 201
    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
