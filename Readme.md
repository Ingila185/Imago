# Imago Backend

This project is a Django-based backend application for managing and searching media data using Elasticsearch. It provides RESTful APIs for querying media information and integrates with Elasticsearch to fetch and filter data efficiently.

---

## Features

- **Elasticsearch Integration**: Query and retrieve media data from Elasticsearch.
- **Django REST Framework**: Provides a robust API layer for the application.
- **Custom Serializers**: Serialize Elasticsearch data into structured JSON responses.
- **CORS Support**: Allows cross-origin requests for frontend integration.
- **Unit Testing**: Includes test cases for API endpoints.

---

## Installation

### Prerequisites

- Python 3.8+
- Elasticsearch (compatible version)
- Django 4.x
- pip (Python package manager)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Ingila185/Imago.git
   cd imago
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Here is the markdown version of the README:

```markdown
# Imago Backend

This project is a Django-based backend application for managing and searching media data using Elasticsearch. It provides RESTful APIs for querying media information and integrates with Elasticsearch to fetch and filter data efficiently.

---

## Features

- **Elasticsearch Integration**: Query and retrieve media data from Elasticsearch.
- **Django REST Framework**: Provides a robust API layer for the application.
- **Custom Serializers**: Serialize Elasticsearch data into structured JSON responses.
- **CORS Support**: Allows cross-origin requests for frontend integration.
- **Unit Testing**: Includes test cases for API endpoints.

---

## Installation

### Prerequisites

- Python 3.8+
- Elasticsearch (compatible version)
- Django 4.x
- pip (Python package manager)

### Steps

1. Clone the repository:

   git clone https://github.com/Ingila185/Imago.git
   cd imago

2. Create a virtual environment:

   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies:

   pip install -r requirements.txt

4. Configure Elasticsearch:

   - Ensure Elasticsearch is running.
   - Update the Elasticsearch connection settings in `elasticsearch_utils.py`.

5. Run migrations:

   python manage.py migrate

6. Start the development server:

   python manage.py runserver
```

## API Endpoints

### Search Media Data

**Endpoint**: `/api/imago-search`  
**Method**: `GET`  
**Description**: Fetch media data from Elasticsearch based on query parameters.

**Query Parameters**:

- `q` (optional): Search term to filter results.

**Example Request**:

```bash
curl -X GET "http://127.0.0.1:8000/api/imago-search?q=test"
```

**Example Response**:

```json
[
  {
    "bildnummer": "93882934",
    "datum": "2018-01-01T00:00:00.000Z",
    "suchtext": "Happiness girl in jump,model released, Symbolfoto ING_19071_09621",
    "fotografen": "ingimage",
    "hoehe": "3840",
    "breite": "5760",
    "db": "stock"
  }
]
```

---

## Serializers

### `ImagoSerializer`

Serializes individual media data fields:

- `bildnummer`
- `datum`
- `suchtext`
- `fotografen`
- `hoehe`
- `breite`
- `db`

### `ImagoSearchResponseSerializer`

Serializes the entire Elasticsearch response, including metadata like `took`, `timed_out`, and `hits`.

---

## Running Tests

Unit tests are included to validate the functionality of the API. To run the tests:

```bash
python manage.py test
```

---

## Configuration

### CORS

To enable CORS, the `django-cors-headers` package is used. Update the `settings.py` file to configure allowed origins:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## Project Structure

```
imago/
├── imagoApp/
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   ├── tests.py          # Unit tests
│   ├── urls.py           # URL routing
│   └── elasticsearch_utils.py  # Elasticsearch client setup
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

---

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

---

## Contact

For questions or support, please contact ingila185@gmail.com.
