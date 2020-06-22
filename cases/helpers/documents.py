from django.http import StreamingHttpResponse
from s3chunkuploader.file_handler import S3FileUploadHandler, UploadFailed, s3_client

from conf.settings import MAX_UPLOAD_SIZE, STREAMING_CHUNK_SIZE, AWS_STORAGE_BUCKET_NAME
from lite_content.lite_internal_frontend import cases


def _validate_document_upload_files(files):
    if not files:
        return cases.Manage.Documents.AttachDocuments.NO_FILE_ERROR
    elif len(files) != 1:
        return cases.Manage.Documents.AttachDocuments.MULTIPLE_FILES
    else:
        return None


def _extract_document_data(files, description=None):
    file = files[0]

    data = {
        "name": getattr(file, "original_name", file.name),
        "s3_key": file.name,
        "size": int(file.size // 1024) if file.size else 0,  # in kilobytes
    }
    if description:
        data["description"] = description

    return data


def handle_document_upload(request):
    """
    Returns (data, None) for a successful document process with data being the document dictionary
    Returns (None, error) if an error occurred, with error being the string of the error
    """
    try:
        request.upload_handlers.insert(0, S3FileUploadHandler(request))
        files = request.FILES.getlist("file")

        # NOTE: File too large check in exception block due to S3FileUploadHandler limitations
        error = _validate_document_upload_files(files)
        if error:
            return None, error

        return _extract_document_data(files, request.POST.get("description")), None
    except UploadFailed:
        if request.upload_handlers[0].content_length > MAX_UPLOAD_SIZE:
            return None, cases.Manage.Documents.AttachDocuments.FILE_TOO_LARGE
        else:
            return None, cases.Manage.Documents.AttachDocuments.UPLOAD_FAILURE_ERROR


def generate_file(result):
    # Stream file upload
    for chunk in iter(lambda: result["Body"].read(STREAMING_CHUNK_SIZE), b""):
        yield chunk


def download_document_from_s3(s3_key, original_file_name):
    s3 = s3_client()
    s3_response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    _kwargs = {}
    if s3_response.get("ContentType"):
        _kwargs["content_type"] = s3_response["ContentType"]
    response = StreamingHttpResponse(generate_file(s3_response), **_kwargs)
    response["Content-Disposition"] = f'attachment; filename="{original_file_name}"'
    return response
