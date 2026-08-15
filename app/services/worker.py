import time
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models.video import EncodingJob
from app.services.encoder import encode_video


# A job processing for longer than this is considered stuck
JOB_TIMEOUT_MINUTES = 30


def recover_stuck_jobs():
    db = SessionLocal()

    try:
        timeout = datetime.utcnow() - timedelta(
            minutes=JOB_TIMEOUT_MINUTES
        )

        stuck_jobs = (
            db.query(EncodingJob)
            .filter(
                EncodingJob.status == "processing",
                EncodingJob.started_at < timeout
            )
            .all()
        )

        for job in stuck_jobs:
            print(
                f"Recovering stuck job {job.id}: "
                f"{job.original_filename}"
            )

            job.status = "queued"
            job.started_at = None

        db.commit()

        if stuck_jobs:
            print(
                f"Recovered {len(stuck_jobs)} stuck job(s)."
            )

    finally:
        db.close()


def process_job():
    db = SessionLocal()

    try:
        # Find and lock one queued job
        job = (
            db.query(EncodingJob)
            .filter(
                EncodingJob.status == "queued"
            )
            .with_for_update()
            .first()
        )

        if not job:
            return False

        print(
            f"Claiming job {job.id}: "
            f"{job.original_filename}"
        )

        # Mark job as processing
        job.status = "processing"
        job.started_at = datetime.utcnow()

        db.commit()

        try:
            # Run FFmpeg
            encode_video(
                job.input_path,
                job.output_path
            )

            # Encoding successful
            job.status = "completed"
            job.completed_at = datetime.utcnow()

            db.commit()

            print(
                f"Job {job.id} completed successfully."
            )

        except Exception as error:
            # Encoding failed
            job.status = "failed"
            job.error_message = str(error)

            db.commit()

            print(
                f"Job {job.id} failed: {error}"
            )

        return True

    finally:
        db.close()


def start_worker():
    print("Video encoding worker started.")

    while True:

        # 1. Recover jobs from crashed workers
        recover_stuck_jobs()

        # 2. Process new queued jobs
        job_processed = process_job()

        if not job_processed:
            print("No queued jobs. Waiting...")

        # 3. Wait before checking again
        time.sleep(5)


if __name__ == "__main__":
    start_worker()