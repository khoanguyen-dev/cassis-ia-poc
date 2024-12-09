# Project Name: Cassis IA Proof of Concept

## Description
La preuve de concept du projet CASSIS IA.

## Features
- Data import/export from Excel and CSV files.
- Integration with other data sources (e.g. medCHUV).
- AI-powered duplicate detection and embeddings.
- Structured data outputs.
- Laravel front-end with Filament package.

## Requirements
- Python 3.8+
- PostgreSQL
- Laravel 10.x
- Composer
- Node.js
- Jupyter Notebook

## Installation
### Clone the repository
   ```bash
   git clone https://github.com/your-username/cassis-ia.git
   cd cassis-ia
   ```
### Backend Setup (Laravel):
1. Navigate to the `backend/` folder:
    ```bash
   cd backend
    ```
2. Install dependencies:
    ```bash
    composer install
    ```
3. Copy the `.env` file:
   ```bash
    cp .env.example .env
    ```
4. Configure the `.env` file with your database credentials:
    ```.env
    DB_CONNECTION=pgsql
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_DATABASE=cassis_ia
    DB_USERNAME=your_db_username
    DB_PASSWORD=your_db_password
    ```
5. Run migrations:
    ```bash
    php artisan migrate
    ```
6. Create an admin user for Filament:
    ```bash
    php artisan make:filament-user
    ```
7. Start the development server:
    ```bash
    php artisan serve
    ```
8. Access the admin panel:
    ```bash
    http://127.0.0.1:8000/admin
    ```
### Python Setup for CSV Import:
1. Navigate to the `scripts/` folder:
    ```bash
   cd scripts
    ```
2. Install Python dependencies:
    ```bash
    pip install pandas sqlalchemy psycopg2
    ```
3. Run the CSV import script
   ```bash
    python init_database.py
    ```

## Usage
- Load and preprocess data using the provided scripts.
- View and manage data through the Laravel front-end.
- Generate embeddings and structured outputs using Python scripts.

## Contribution
Feel free to fork the repository and submit pull requests!

## License
MIT License

Copyright (c) 2024 Cassis IA

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
