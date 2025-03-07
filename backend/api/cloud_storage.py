import cloudinary.uploader

def upload_to_cloudinary(file):
    upload_result = cloudinary.uploader.upload(file)
    return upload_result["secure_url"]
