Video to Audio Converter API
============================

This is a FastAPI application that allows users to upload video files, convert them to audio, and download or stream the converted audio files.

Features
--------

*   Upload video files (MP4, MKV, AVI, MOV, FLV)
*   Convert uploaded videos to MP3 audio
*   Save converted audio files to Deta Drive
*   Download converted audio files
*   Stream converted audio files

Endpoints
---------

### /upload

*   Accepts POST requests with a video file to upload
*   Converts the video to MP3 audio
*   Saves the audio file to Deta Drive
*   Returns a success message

### /download/{file\_name}

*   Accepts GET requests with the audio file name
*   Downloads the audio file from Deta Drive
*   Returns the file as an attachment

### /audio/{file\_name}

*   Accepts GET requests with the audio file name
*   Streams the audio file from Deta Drive

Setup
-----

1.  Clone the repository
2.  Install dependencies



`pip install -r requirements.txt`




`uvicorn main:app`

The application will be served at [http://127.0.0.1:8000](http://127.0.0.1:8000)

Dependencies
------------


*    FastAPI - Web framework for building the REST API endpoints.
*    Deta - Used to interact with Deta Drive for file storage.
*    moviepy - Media processing library used to convert videos to audio.
*    uvicorn - ASGI server for running the FastAPI application.
*    python-multipart - Used for handling multipart/form-data requests to upload files.
*    python-dotenv - Used for loading environment variables from a .env file.


