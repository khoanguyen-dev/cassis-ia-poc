<?php

namespace App\Filament\Resources;

use App\Filament\Resources\AnnuaireResource\Pages;
use App\Filament\Resources\AnnuaireResource\RelationManagers;
use App\Models\Annuaire;
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\DatePicker;
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Columns\BooleanColumn;
use Filament\Tables\Columns\DateColumn;

class AnnuaireResource extends Resource
{
    protected static ?string $model = Annuaire::class;

    protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';

    public static ?int $defaultPaginationCount = 10; // Show 10 rows per page

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                TextInput::make('type_de_partenaire')->label('Type de Partenaire'),
                TextInput::make('personnalite_juridique')->label('Personnalité Juridique'),
                TextInput::make('type_de_fournisseur')->label('Type de Fournisseur'),
                TextInput::make('nom')->label('Nom')->required(),
                TextInput::make('prenom')->label('Prenom')->required(),
                TextInput::make('voie')->label('Voie'),
                TextInput::make('complement')->label('Complement'),
                TextInput::make('npa')->label('NPA'),
                TextInput::make('localite')->label('Localité'),
                TextInput::make('pays')->label('Pays'),
                TextInput::make('telephone')->label('Téléphone'),
                TextInput::make('portable')->label('Portable'),
                TextInput::make('courriel')->label('Courriel'),
                TextInput::make('site_web')->label('Site Web'),
                Textarea::make('activite_specialite')->label('Activité / Spécialité'),
                Toggle::make('medecin')->label('Médecin'),
                Toggle::make('medecin_intra_hospitalier')->label('Médecin Intra-Hospitalier'),
                Textarea::make('horaires_ouverture')->label('Horaires d\'Ouverture'),
                TextInput::make('coord_geo_nord')->label('Coord Geo Nord'),
                TextInput::make('coord_geo_est')->label('Coord Geo Est'),
                TextInput::make('coord_geo_long')->label('Coord Geo Long'),
                TextInput::make('coord_geo_lat')->label('Coord Geo Lat'),
                Toggle::make('besoin_convention')->label('Besoin de Convention'),
                TextInput::make('type_de_convention')->label('Type de Convention'),
                DatePicker::make('date_convention_soumise')->label('Date Convention Soumise'),
                DatePicker::make('date_convention_valide_recue')->label('Date Convention Validée Reçue'),
                DatePicker::make('date_derniere_modification')->label('Date Dernière Modification'),
                DatePicker::make('date_saisie')->label('Date Saisie'),
                DatePicker::make('date_dernier_appel_actualisation')->label('Date Dernier Appel Actualisation'),
                DatePicker::make('date_derniere_modif')->label('Date Dernière Modif'),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                TextColumn::make('numero')->label('Numero')->sortable()->searchable(),
                TextColumn::make('type_de_partenaire')->label('Type de Partenaire')->searchable(),
                TextColumn::make('personnalite_juridique')->label('Personnalité Juridique')->searchable(),
                TextColumn::make('type_de_fournisseur')->label('Type de Fournisseur')->searchable(),
                TextColumn::make('nom')->label('Nom')->searchable(),
                TextColumn::make('prenom')->label('Prenom')->searchable(),
                TextColumn::make('voie')->label('Voie'),
                TextColumn::make('complement')->label('Complement'),
                TextColumn::make('npa')->label('NPA'),
                TextColumn::make('localite')->label('Localité'),
                TextColumn::make('pays')->label('Pays'),
                TextColumn::make('telephone')->label('Téléphone'),
                TextColumn::make('portable')->label('Portable'),
                TextColumn::make('courriel')->label('Courriel'),
                TextColumn::make('site_web')->label('Site Web'),
                TextColumn::make('activite_specialite')->label('Activité / Spécialité')->limit(50),
                BooleanColumn::make('medecin')->label('Médecin'),
                BooleanColumn::make('medecin_intra_hospitalier')->label('Médecin Intra-Hospitalier'),
                TextColumn::make('horaires_ouverture')->label('Horaires d\'Ouverture')->limit(50),
                TextColumn::make('coord_geo_nord')->label('Coord Geo Nord'),
                TextColumn::make('coord_geo_est')->label('Coord Geo Est'),
                TextColumn::make('coord_geo_long')->label('Coord Geo Long'),
                TextColumn::make('coord_geo_lat')->label('Coord Geo Lat'),
                BooleanColumn::make('besoin_convention')->label('Besoin de Convention'),
                TextColumn::make('type_de_convention')->label('Type de Convention')
            ])
            ->defaultSort('numero', 'asc'); // Optional: set default sorting
    }

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListAnnuaires::route('/'),
            'create' => Pages\CreateAnnuaire::route('/create'),
            'edit' => Pages\EditAnnuaire::route('/{record}/edit'),
        ];
    }
}
