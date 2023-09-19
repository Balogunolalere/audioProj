from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from moviepy.editor import VideoFileClip
import deta
import os
import shutil
import tempfile
import io

app = FastAPI()

# Initialize Deta Drive with your project key
drive = deta.Deta("a0bkhtw7ore_KF3xzLHFkwq46hcyC9vGdtaAEEDF6fqF").Drive('audioProj')

def convert_video_to_audio(input_file: str, output_file: str): 
    '''
    Convert the video to audio

    Parameters
    ----------
    input_file : str
        Path to the input video file
    output_file : str
        Path to the output audio file

    Returns
    -------
    None
    '''
    # Convert the video to audio
    video = VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    '''
    Upload a video file to the server, convert it to audio, and upload the audio file to Deta Drive

    Parameters
    ----------
    file : UploadFile
        The video file to be uploaded

    Returns
    -------
    dict
    '''
    # Check if the uploaded file is a video
    if not file.filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
        raise HTTPException(status_code=400, detail="Uploaded file must be a video (mp4, mkv, avi, mov, flv)")
    
    # Create a temporary directory to store the video file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Convert the video to audio
        output_file = os.path.splitext(file.filename)[0] + '.mp3'
        output_path = os.path.join(temp_dir, output_file)
        convert_video_to_audio(file_path, output_path)
        
        # Upload the audio file to Deta Drive
        with open(output_path, 'rb') as f:
            drive.put(output_file, f)

    return {"message": "Video uploaded successfully"}

@app.get("/download/{file_name}")
def download(file_name: str):
    '''
    Download an audio file from Deta Drive

    Parameters
    ----------
    file_name : str
        Name of the audio file to be downloaded

    Returns
    -------
    StreamingResponse
    '''
    # check if the file exists in Deta Drive
    if not drive.get(file_name):
        raise HTTPException(status_code=404, detail="File not found")
    
    # download the file from Deta Drive
    audio_data = drive.get(file_name).read()

    media_type = f"audio/{file_name.split('.')[-1]}"
    headers = {
        "Content-Disposition": f"attachment; filename={file_name}"
    }
    return StreamingResponse(io.BytesIO(audio_data), media_type=media_type, headers=headers)

    
@app.get("/audio/{file_name}")
def play_audio(file_name: str):
    '''
    Stream an audio file from Deta Drive

    Parameters
    ----------
    file_name : str
        Name of the audio file to be streamed

    Returns
    -------
    StreamingResponse
    '''
    # check if the file exists in Deta Drive
    if not drive.get(file_name):
        raise HTTPException(status_code=404, detail="File not found")
    
    # download the file from Deta Drive

    audio_data = drive.get(file_name).read()

    media_type = f"audio/{file_name.split('.')[-1]}"
    return StreamingResponse(io.BytesIO(audio_data), media_type=media_type)

  