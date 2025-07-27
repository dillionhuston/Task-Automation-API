# this file contains the logic for file hashing etc
from app.utils import * # make a bit simpler instead of importing, one by one

def compute(file, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    while chunk := file.read(8192):
        hasher.update(chunk)
    return hasher.hexdigest()

def save_file(file: UploadFile, user_id: str,) -> tuple[str, str]:
    filename = f"{user_id}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return filename, file_path


def validate_file(file: UploadFile):
    max_size = 1028 * 1028 # 5 bytes bt can be changed
    if file.size > max_size:
        HTTPException(status_code=404, detail="file too big")
        return