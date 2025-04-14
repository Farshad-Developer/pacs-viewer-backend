
# PACS Viewer Backend

This project simulates a backend for a PACS (Picture Archiving and Communication System) to upload and view medical image files.

## Features

- Upload medical image files (e.g., DICOM, JPG, PNG)
- Store metadata in SQLite database
- Retrieve list of uploaded files
- Download individual files by ID
- Full Swagger UI documentation

## Technologies Used

- Python 3.10+
- FastAPI
- SQLite
- Swagger / OpenAPI

## How to Run

1. Install dependencies:

```bash
pip install fastapi uvicorn python-multipart
```

2. Run the server:

```bash
python -m uvicorn pacs_main:app --reload
```

3. Open in browser:

```
http://127.0.0.1:8000/docs
```

## Author

Farshad | [GitHub Profile](https://github.com/farshad-dev)
