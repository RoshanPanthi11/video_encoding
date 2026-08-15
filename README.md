# Video Encoding API

A simple video encoding backend built with FastAPI, MySQL, SQLAlchemy, and FFmpeg.

This project is created for learning purposes.

## Features

- Upload videos
- Encode videos using FFmpeg
- Store encoding jobs in MySQL
- Background worker for encoding
- Track encoding status
- Handle failed and stuck jobs

## Tech Stack

- Python
- FastAPI
- MySQL
- SQLAlchemy
- FFmpeg

## Run

Start FastAPI:
uvicorn app.main:app --reload


Start the worker in another terminal:
python -m app.services.worker
