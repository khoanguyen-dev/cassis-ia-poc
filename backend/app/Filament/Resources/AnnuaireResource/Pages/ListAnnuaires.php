<?php

namespace App\Filament\Resources\AnnuaireResource\Pages;

use App\Filament\Resources\AnnuaireResource;
use Filament\Actions;
use Filament\Resources\Pages\ListRecords;

class ListAnnuaires extends ListRecords
{
    protected static string $resource = AnnuaireResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\CreateAction::make(),
        ];
    }
}
