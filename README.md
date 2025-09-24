# RAG API Documentation

## API Endpoints

### GET /
Welcome endpoint returning app name and version.

Response:
```json
{
  "app_name": "string",
  "app_version": "string"
}
```

### POST /data/upload/{project_id}
Upload files to a specific project.

Parameters:
- `project_id`: Project identifier in the path

Request body:
- `file`: File to upload

Response:
```json
{
  "status": "success|error",
  "message": "string"
}
```

### POST /data/process/{project_id}
Process files with chunking parameters.

Parameters:
- `project_id`: Project identifier in the path

Request body:
```json
{
  "file_id": "string",
  "chunk_size": "integer (default: 100)",
  "over_lap_size": "integer (default: 20)",
  "do_reset": "integer (default: 0)"
}
```

Response:
Returns processed file chunks.

## Configuration
The application uses environment variables defined in `.env` file:
- `APP_NAME` - Application name
- `APP_VERSION` - Application version
- `OPENAI_API_KEY` - OpenAI API key
- `FILE_ALLOWED_TYPES` - Allowed MIME types
- `FILE_MAX_SIZE` - Maximum file size in bytes
- `FILES_DEFAULT_CHUNK_SIZE` - Default chunk size for file uploads

## Dependencies
- FastAPI
- Uvicorn
- LangChain
- PyMuPDF
- Pydantic