from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil

from sqlalchemy.orm import Session


from app.database import get_db
from app.models.video import EncodingJob


router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)


UPLOAD_DIR = Path("uploads")
ENCODED_DIR = Path("encoded")

UPLOAD_DIR.mkdir(exist_ok=True)
ENCODED_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    input_path = UPLOAD_DIR / file.filename
    output_path = ENCODED_DIR / f"encoded_{file.filename}"

    # 1. Save uploaded video
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Create encoding job
    job = EncodingJob(
        original_filename=file.filename,
        input_path=str(input_path),
        output_path=str(output_path),
        status="queued"
    )

    # 3. Save job to MySQL
    db.add(job)
    db.commit()

    # 4. Get generated job ID
    db.refresh(job)

    return {
        "message": "Video uploaded successfully",
        "job_id": job.id,
        "status": job.status,
        "original_file": job.original_filename
    }

@router.get("/jobs/{job_id}")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(EncodingJob)
        .filter(EncodingJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Encoding job not found"
        )

    return {
        "job_id": job.id,
        "original_file": job.original_filename,
        "status": job.status,
        "input_path": job.input_path,
        "output_path": job.output_path,
        "error_message": job.error_message,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at
    }