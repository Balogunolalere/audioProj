import moviepy.editor as mp
import typer

app = typer.Typer()

def main(input_file: str, output_file: str):
    video = mp.VideoFileClip(input_file)
    audio = video.audio
    audio.write_audiofile(output_file)

@app.command()
def convert_audio(input_file: str, output_file: str):
    main(input_file, output_file)
    typer.echo(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    app()

