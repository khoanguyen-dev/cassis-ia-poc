import React, { memo } from "react";

const EvenementTable = memo(({ evenements }) => (
  <section className="mt-4">
    <table className="table table-striped table-bordered">
      <thead className="table-dark">
        <tr>
          <th>Numéro</th>
          <th>Nom de l'Événement</th>
          <th>Titre</th>
          <th>Date de Début</th>
          <th>Date de Fin</th>
          <th>Horaire Début</th>
          <th>Horaire Fin</th>
          <th>Texte Libre</th>
          <th>Court Descriptif</th>
          <th>Numéro Partenaire</th>
          <th>Nom Partenaire</th>
          <th>Partenaire de la Sélection</th>
          <th>Sites Originaux</th>
          <th>Date de Création</th>
          <th>Mode de Création</th>
          <th>Date de Dernière Modification</th>
          <th>Mode de Modification</th>
          <th>ID Dernier Modificateur</th>
          <th>Date de Péremption</th>
        </tr>
      </thead>
      <tbody>
        {evenements.length > 0 ? (
          evenements.map((evenement) => (
            <tr key={evenement.numero}>
              <td>{evenement.numero}</td>
              <td>{evenement.nom_evenement}</td>
              <td>{evenement.titre_evenement}</td>
              <td>{evenement.date_debut}</td>
              <td>{evenement.date_fin}</td>
              <td>{evenement.horaire_debut}</td>
              <td>{evenement.horaire_fin}</td>
              <td>{evenement.texte_libre}</td>
              <td>{evenement.court_descriptif}</td>
              <td>{evenement.numero_partenaire}</td>
              <td>{evenement.nom_partenaire}</td>
              <td>{evenement.partenaire_de_la_selection}</td>
              <td>{evenement.sites_originaux}</td>
              <td>{evenement.date_creation}</td>
              <td>{evenement.mode_creation}</td>
              <td>{evenement.date_derniere_modification}</td>
              <td>{evenement.mode_modification}</td>
              <td>{evenement.id_dernier_modificateur}</td>
              <td>{evenement.date_de_peremption}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="19" className="text-center">
              No entries found.
            </td>
          </tr>
        )}
      </tbody>
    </table>
  </section>
));

export default EvenementTable;
