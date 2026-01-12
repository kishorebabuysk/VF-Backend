'''import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads/onboarding"

def save_file(file: UploadFile) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return path'''

import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads/onboarding"

def save_file(file: UploadFile) -> str:
    if not file or not file.filename:
        raise ValueError("Invalid file upload")

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path
