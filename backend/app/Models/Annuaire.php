<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Annuaire extends Model
{
    use HasFactory;

    protected $table = 'annuaire'; // Ensure it points to the correct table
    protected $primaryKey = 'numero'; // Define the primary key
    public $timestamps = false; // Disable timestamps if not in use

    protected $fillable = [
        'type_de_partenaire',
        'personnalite_juridique',
        'type_de_fournisseur',
        'nom',
        'prenom',
        'voie',
        'complement',
        'npa',
        'localite',
        'pays',
        'telephone',
        'portable',
        'courriel',
        'site_web',
        'activite_specialite',
        'medecin',
        'medecin_intra_hospitalier',
        'horaires_ouverture',
        'coord_geo_nord',
        'coord_geo_est',
        'coord_geo_long',
        'coord_geo_lat',
        'besoin_convention',
        'type_de_convention',
        'date_convention_soumise',
        'date_convention_valide_recue',
        'date_derniere_modification',
        'date_saisie',
        'date_dernier_appel_actualisation',
        'date_derniere_modif',
    ];
}
