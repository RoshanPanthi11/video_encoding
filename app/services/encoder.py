import subprocess
from pathlib import Path


def encode_video(input_path: str, output_path: str):
    command = [
        "ffmpeg",
        "-i", input_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        output_path
    ]

    subprocess.run(command, check=True)