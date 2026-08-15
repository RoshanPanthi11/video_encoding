from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text

from app.database import Base


class EncodingJob(Base):
    __tablename__ = "encoding_jobs"

    id = Column(Integer, primary_key=True, index=True)

    original_filename = Column(String(255), nullable=False)

    input_path = Column(String(500), nullable=False)

    output_path = Column(String(500), nullable=False)

    status = Column(
        String(50),
        default="queued",
        nullable=False
    )

    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    started_at = Column(
         DateTime,
         nullable=True
)

    completed_at = Column(
        DateTime,
        nullable=True
    )