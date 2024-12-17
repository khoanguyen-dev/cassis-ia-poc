from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import openai
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configure OpenAI API key
openai.api_key = "API key"

# Database connection
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        database="cassis_ia",
        user="khoa",
        password="k123"
    )

# Define JSON schema for structured output
json_schema = {
    "type": "object",
    "properties": {
        "entries": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type_de_partenaire": {"type": "string"},
                    "personnalite_juridique": {"type": "string"},
                    "type_de_fournisseur": {"type": "string"},
                    "nom": {"type": "string"},
                    "prenom": {"type": "string"},
                    "voie": {"type": "string"},
                    "complement": {"type": "string"},
                    "npa": {"type": "integer"},
                    "localite": {"type": "string"},
                    "pays": {"type": "string"},
                    "telephone": {"type": "string"},
                    "portable": {"type": "string"},
                    "courriel": {"type": "string"},
                    "site_web": {"type": "string"},
                    "activite_specialite": {"type": "string"},
                    "medecin": {"type": "boolean"},
                    "medecin_intra_hospitalier": {"type": "boolean"},
                    "horaires_ouverture": {"type": "string"},
                    "coord_geo_nord": {"type": "number"},
                    "coord_geo_est": {"type": "number"},
                    "coord_geo_long": {"type": "number"},
                    "coord_geo_lat": {"type": "number"},
                    "besoin_convention": {"type": "boolean"},
                    "type_de_convention": {"type": "string"},
                    "date_convention_soumise": {"type": "string", "format": "date"},
                    "date_convention_valide_recue": {"type": "string", "format": "date"},
                    "date_derniere_modification": {"type": "string", "format": "date"},
                    "date_saisie": {"type": "string", "format": "date"},
                    "date_dernier_appel_actualisation": {"type": "string", "format": "date"}
                },
                "required": ["nom", "prenom"]
            }
        }
    },
    "required": ["entries"]
}

@app.route('/entries', methods=['GET'])
def get_entries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM annuaire;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return jsonify([dict(zip(column_names, row)) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_input():
    text_input = request.form.get('text', '')
    file = request.files.get('file')

    if file:
        text_input = file.read().decode('utf-8')

    if not text_input:
        return jsonify({'error': 'No input provided'}), 400

    # Call OpenAI API to parse text into structured JSON
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant."},
                {"role": "user", "content": f"Extract structured entries from the following text:\n{text_input}"}
            ],
            functions=[
                {"name": "generate_entry", "parameters": json_schema}
            ],
            function_call={"name": "generate_entry"}
        )

        structured_data = json.loads(response.choices[0].message['function_call']['arguments'])
        entries = structured_data.get('entries', [])
    except json.JSONDecodeError as e:
        return jsonify({'error': f"Failed to decode JSON: {str(e)}"}), 500
    except Exception as e:
        return jsonify({'error': f"Failed to process input: {str(e)}"}), 500

    conn = get_db_connection()
    cursor = conn.cursor()

    duplicates = []
    successful_inserts = []

    for entry in entries:
        try:
            # Check for duplicates using fuzzy matching
            cursor.execute("""
                SELECT *,
                       similarity(nom, %s) AS nom_similarity,
                       similarity(prenom, %s) AS prenom_similarity
                FROM annuaire
                WHERE similarity(nom, %s) > 0.3 OR LEFT(prenom, 1) = LEFT(%s, 1);
            """, (entry["nom"], entry["prenom"], entry["nom"], entry["prenom"]))
            existing = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            close_matches = [
                dict(zip(column_names, row))
                for row in existing
                if row[-2] > 0.3 or row[-1] > 0.3  # Using similarity scores
            ]

            if close_matches:
                duplicates.append({
                    'new_entry': entry,
                    'existing_entries': close_matches
                })
            else:
                # Add current date to `date_derniere_modification`
                entry['date_derniere_modification'] = datetime.now().strftime('%Y-%m-%d')
                columns = ', '.join(entry.keys())
                values = ', '.join(['%s'] * len(entry))
                cursor.execute(f"INSERT INTO annuaire ({columns}) VALUES ({values})", list(entry.values()))
                successful_inserts.append(entry)
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f"Database error: {str(e)}"}), 500

    conn.commit()
    conn.close()

    if duplicates:
        return jsonify({'warning': 'Duplicate entries found', 'duplicates': duplicates}), 409

    return jsonify({'message': 'Entries successfully added', 'successful_inserts': successful_inserts}), 201

@app.route('/replace-entry', methods=['PUT'])
def replace_entry():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        for entry in data:
            # Convert empty strings to None (NULL in SQL)
            processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}

            if "numero" in processed_entry:
                cursor.execute("""
                    UPDATE annuaire
                    SET type_de_partenaire = %s,
                        personnalite_juridique = %s,
                        type_de_fournisseur = %s,
                        nom = %s,
                        prenom = %s,
                        voie = %s,
                        complement = %s,
                        npa = %s,
                        localite = %s,
                        pays = %s,
                        telephone = %s,
                        portable = %s,
                        courriel = %s,
                        site_web = %s,
                        activite_specialite = %s,
                        medecin = %s,
                        medecin_intra_hospitalier = %s,
                        horaires_ouverture = %s,
                        coord_geo_nord = %s,
                        coord_geo_est = %s,
                        coord_geo_long = %s,
                        coord_geo_lat = %s,
                        besoin_convention = %s,
                        type_de_convention = %s,
                        date_convention_soumise = %s,
                        date_convention_valide_recue = %s,
                        date_derniere_modification = CURRENT_DATE,
                        date_saisie = %s,
                        date_dernier_appel_actualisation = %s
                    WHERE numero = %s
                """, (
                    processed_entry.get("type_de_partenaire"),
                    processed_entry.get("personnalite_juridique"),
                    processed_entry.get("type_de_fournisseur"),
                    processed_entry.get("nom"),
                    processed_entry.get("prenom"),
                    processed_entry.get("voie"),
                    processed_entry.get("complement"),
                    processed_entry.get("npa"),
                    processed_entry.get("localite"),
                    processed_entry.get("pays"),
                    processed_entry.get("telephone"),
                    processed_entry.get("portable"),
                    processed_entry.get("courriel"),
                    processed_entry.get("site_web"),
                    processed_entry.get("activite_specialite"),
                    processed_entry.get("medecin"),
                    processed_entry.get("medecin_intra_hospitalier"),
                    processed_entry.get("horaires_ouverture"),
                    processed_entry.get("coord_geo_nord"),
                    processed_entry.get("coord_geo_est"),
                    processed_entry.get("coord_geo_long"),
                    processed_entry.get("coord_geo_lat"),
                    processed_entry.get("besoin_convention"),
                    processed_entry.get("type_de_convention"),
                    processed_entry.get("date_convention_soumise"),
                    processed_entry.get("date_convention_valide_recue"),
                    processed_entry.get("date_saisie"),
                    processed_entry.get("date_dernier_appel_actualisation"),
                    processed_entry["numero"]
                ))
            else:
                return jsonify({'error': "Missing 'numero' field for replacement"}), 400

        conn.commit()
        conn.close()
        return jsonify({'message': 'Entry replaced successfully'}), 200

    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500

@app.route('/add-entry', methods=['POST'])
def add_entry():
    try:
        entry = request.json  # Expecting a single entry as JSON
        conn = get_db_connection()
        cursor = conn.cursor()

        # Convert empty strings to None (NULL in SQL)
        processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}

        # Add current date to `date_derniere_modification`
        processed_entry['date_derniere_modification'] = datetime.now().strftime('%Y-%m-%d')

        columns = ', '.join(processed_entry.keys())
        values = ', '.join(['%s'] * len(processed_entry))
        cursor.execute(f"INSERT INTO annuaire ({columns}) VALUES ({values})", list(processed_entry.values()))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Entry added successfully'}), 201

    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    
@app.route('/evenements', methods=['GET'])
def get_evenement_entries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM evenement;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()
        return jsonify([dict(zip(column_names, row)) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-evenement', methods=['POST'])
def add_evenement_entry():
    try:
        entry = request.json  # Expecting a single entry as JSON
        conn = get_db_connection()
        cursor = conn.cursor()

        # Convert empty strings to None (NULL in SQL)
        processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}

        # Add current date to `date_derniere_modification`
        processed_entry['date_derniere_modification'] = datetime.now().strftime('%Y-%m-%d')

        columns = ', '.join(processed_entry.keys())
        values = ', '.join(['%s'] * len(processed_entry))
        cursor.execute(f"INSERT INTO evenement ({columns}) VALUES ({values})", list(processed_entry.values()))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Evenement entry added successfully'}), 201

    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500
    
@app.route('/replace-evenement', methods=['PUT'])
def replace_evenement_entry():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()

        for entry in data:
            # Convert empty strings to None (NULL in SQL)
            processed_entry = {k: (None if v == "" else v) for k, v in entry.items()}

            if "numero" in processed_entry:
                cursor.execute("""
                    UPDATE evenement
                    SET nom_evenement = %s,
                        titre_evenement = %s,
                        date_debut = %s,
                        date_fin = %s,
                        horaire_debut = %s,
                        horaire_fin = %s,
                        texte_libre = %s,
                        court_descriptif = %s,
                        numero_partenaire = %s,
                        nom_partenaire = %s,
                        partenaire_de_la_selection = %s,
                        sites_originaux = %s,
                        date_creation = %s,
                        mode_creation = %s,
                        date_derniere_modification = CURRENT_DATE,
                        mode_modification = %s,
                        id_dernier_modificateur = %s,
                        date_de_peremption = %s
                    WHERE numero = %s
                """, (
                    processed_entry.get("nom_evenement"),
                    processed_entry.get("titre_evenement"),
                    processed_entry.get("date_debut"),
                    processed_entry.get("date_fin"),
                    processed_entry.get("horaire_debut"),
                    processed_entry.get("horaire_fin"),
                    processed_entry.get("texte_libre"),
                    processed_entry.get("court_descriptif"),
                    processed_entry.get("numero_partenaire"),
                    processed_entry.get("nom_partenaire"),
                    processed_entry.get("partenaire_de_la_selection"),
                    processed_entry.get("sites_originaux"),
                    processed_entry.get("date_creation"),
                    processed_entry.get("mode_creation"),
                    processed_entry.get("mode_modification"),
                    processed_entry.get("id_dernier_modificateur"),
                    processed_entry.get("date_de_peremption"),
                    processed_entry["numero"]
                ))
            else:
                return jsonify({'error': "Missing 'numero' field for replacement"}), 400

        conn.commit()
        conn.close()
        return jsonify({'message': 'Evenement entry replaced successfully'}), 200

    except Exception as e:
        return jsonify({'error': f"Database error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
