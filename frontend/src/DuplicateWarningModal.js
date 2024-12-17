import React, { useState, useEffect } from "react";

function DuplicateWarningModal({ duplicate, onUpdate, onReplace, onAdd, onCancel, onNext }) {
  const TABLE_FIELDS = duplicate?.new_entry?.hasOwnProperty("nom_evenement")
    ? [
        "nom_evenement",
        "titre_evenement",
        "date_debut",
        "date_fin",
        "horaire_debut",
        "horaire_fin",
        "texte_libre",
        "court_descriptif",
        "numero_partenaire",
        "nom_partenaire",
        "partenaire_de_la_selection",
        "sites_originaux",
        "date_creation",
        "mode_creation",
        "date_derniere_modification",
        "mode_modification",
        "id_dernier_modificateur",
        "date_de_peremption",
      ]
    : [
        "type_de_partenaire",
        "personnalite_juridique",
        "type_de_fournisseur",
        "nom",
        "prenom",
        "voie",
        "complement",
        "npa",
        "localite",
        "pays",
        "telephone",
        "portable",
        "courriel",
        "site_web",
        "activite_specialite",
        "medecin",
        "medecin_intra_hospitalier",
        "horaires_ouverture",
        "coord_geo_nord",
        "coord_geo_est",
        "coord_geo_long",
        "coord_geo_lat",
        "besoin_convention",
        "type_de_convention",
        "date_convention_soumise",
        "date_convention_valide_recue",
        "date_derniere_modification",
        "date_saisie",
        "date_dernier_appel_actualisation",
      ];

  const [editedEntry, setEditedEntry] = useState({});
  const [selectedExistingEntry, setSelectedExistingEntry] = useState(null);

  useEffect(() => {
    if (duplicate) {
      const newEntryData = TABLE_FIELDS.reduce(
        (acc, field) => ({
          ...acc,
          [field]: duplicate.new_entry[field] || "",
        }),
        {}
      );
      setEditedEntry(newEntryData);
      setSelectedExistingEntry(null);
    }
  }, [duplicate]);

  const handleFieldChange = (field, value) => {
    setEditedEntry((prev) => ({ ...prev, [field]: value }));
  };

  const handleSelectExistingEntry = (entry) => {
    setSelectedExistingEntry(entry);
    setEditedEntry((prev) => ({ ...prev, numero: entry.numero }));
  };

  const handleAddAndNext = async () => {
    await onAdd(editedEntry);
    onNext();
  };

  const handleReplaceAndNext = async () => {
    if (!selectedExistingEntry) {
      alert("Please select an entry to replace.");
      return;
    }
    await onReplace(editedEntry);
    onNext();
  };

  return (
    <div className="modal show d-block">
      <div className="modal-dialog modal-lg">
        <div className="modal-content">
          <div className="modal-header bg-danger text-white">
            <h5 className="modal-title">Duplicate Entry Found</h5>
            <button className="btn-close text-white" onClick={onCancel}></button>
          </div>
          <div className="modal-body">
            <p className="text-danger">
              Resolve the duplicate entry by filling in all fields, adding as a new entry, or replacing an existing entry.
            </p>

            <h6>New Entry:</h6>
            <form>
              {TABLE_FIELDS.map((field) => (
                <div className="mb-3" key={field}>
                  <label className="form-label">
                    {field.replace(/_/g, " ").toUpperCase()}
                  </label>
                  <input
                    type={field.includes("date") ? "date" : "text"}
                    value={editedEntry[field] || ""}
                    onChange={(e) => handleFieldChange(field, e.target.value)}
                    className="form-control"
                  />
                </div>
              ))}
            </form>

            <h6>Existing Entries in Database:</h6>
            {duplicate?.existing_entries.map((existing, idx) => (
              <div
                key={idx}
                className={`border p-2 mb-2 ${
                  selectedExistingEntry?.numero === existing.numero
                    ? "border-primary"
                    : "border-secondary"
                }`}
                onClick={() => handleSelectExistingEntry(existing)}
                style={{ cursor: "pointer" }}
              >
                <strong>Numero {existing.numero}:</strong>
                <pre>{JSON.stringify(existing, null, 2)}</pre>
              </div>
            ))}
          </div>
          <div className="modal-footer">
            <button className="btn btn-success" onClick={handleAddAndNext}>
              Add as New Entry
            </button>
            <button className="btn btn-warning" onClick={handleReplaceAndNext}>
              Replace Selected Entry
            </button>
            <button className="btn btn-info" onClick={onNext}>
              Skip to Next Duplicate
            </button>
            <button className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DuplicateWarningModal;
