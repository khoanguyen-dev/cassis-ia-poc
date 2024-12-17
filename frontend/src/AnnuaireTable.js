import React, { memo } from "react";

const AnnuaireTable = memo(({ entries }) => (
  <section className="mt-4">
    <table className="table table-striped table-bordered">
      <thead className="table-dark">
        <tr>
          <th>Numéro</th>
          <th>Type de Partenaire</th>
          <th>Personnalité Juridique</th>
          <th>Type de Fournisseur</th>
          <th>Nom</th>
          <th>Prénom</th>
          <th>Voie</th>
          <th>Complément</th>
          <th>NPA</th>
          <th>Localité</th>
          <th>Pays</th>
          <th>Téléphone</th>
          <th>Portable</th>
          <th>Courriel</th>
          <th>Site Web</th>
          <th>Activité Spécialité</th>
          <th>Médecin</th>
          <th>Médecin Intra-Hospitalier</th>
          <th>Horaires Ouverture</th>
          <th>Coord Geo Nord</th>
          <th>Coord Geo Est</th>
          <th>Coord Geo Long</th>
          <th>Coord Geo Lat</th>
          <th>Besoin Convention</th>
          <th>Type de Convention</th>
          <th>Date Convention Soumise</th>
          <th>Date Convention Valide Reçue</th>
          <th>Date Dernière Modification</th>
          <th>Date Saisie</th>
          <th>Date Dernier Appel Actualisation</th>
          <th>Date Dernière Modif</th>
        </tr>
      </thead>
      <tbody>
        {entries.length > 0 ? (
          entries.map((entry) => (
            <tr key={entry.numero}>
              <td>{entry.numero}</td>
              <td>{entry.type_de_partenaire}</td>
              <td>{entry.personnalite_juridique}</td>
              <td>{entry.type_de_fournisseur}</td>
              <td>{entry.nom}</td>
              <td>{entry.prenom}</td>
              <td>{entry.voie}</td>
              <td>{entry.complement}</td>
              <td>{entry.npa}</td>
              <td>{entry.localite}</td>
              <td>{entry.pays}</td>
              <td>{entry.telephone}</td>
              <td>{entry.portable}</td>
              <td>{entry.courriel}</td>
              <td>{entry.site_web}</td>
              <td>{entry.activite_specialite}</td>
              <td>{entry.medecin ? "Yes" : "No"}</td>
              <td>{entry.medecin_intra_hospitalier ? "Yes" : "No"}</td>
              <td>{entry.horaires_ouverture}</td>
              <td>{entry.coord_geo_nord}</td>
              <td>{entry.coord_geo_est}</td>
              <td>{entry.coord_geo_long}</td>
              <td>{entry.coord_geo_lat}</td>
              <td>{entry.besoin_convention ? "Yes" : "No"}</td>
              <td>{entry.type_de_convention}</td>
              <td>{entry.date_convention_soumise}</td>
              <td>{entry.date_convention_valide_recue}</td>
              <td>{entry.date_derniere_modification}</td>
              <td>{entry.date_saisie}</td>
              <td>{entry.date_dernier_appel_actualisation}</td>
              <td>{entry.date_derniere_modif}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="31" className="text-center">
              No entries found.
            </td>
          </tr>
        )}
      </tbody>
    </table>
  </section>
));

export default AnnuaireTable;
