from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Storage(S3Boto3Storage):
    bucket_name = 'shikala'
    endpoint_url = 'https://minio.shikala.com'
    access_key = 'vUZDxCpXfwRL24WTGhTM'
    secret_key = 'yzPTaa8k5crrAeUmOUejkLnf6hJ3EzNoef3khaF6'
    file_overwrite = True
    default_acl = 'public-read'
    querystring_auth = False
    region_name = 'us-east-1'
    signature_version = 's3v4'
    addressing_style = 'path'

class MediaStorage(S3Boto3Storage):
    bucket_name = 'shikala'
    location = 'media'  # prefix داخل bucket
    endpoint_url = 'https://minio.shikala.com'
    access_key = 'vUZDxCpXfwRL24WTGhTM'
    secret_key = 'yzPTaa8k5crrAeUmOUejkLnf6hJ3EzNoef3khaF6'
    file_overwrite = False
    default_acl = 'public-read'
    querystring_auth = False
    region_name = 'us-east-1'
    signature_version = 's3v4'
    addressing_style = 'path'
    

class StaticStorage(S3Boto3Storage):
    bucket_name = 'shikala'
    location = 'static'
    endpoint_url = 'https://minio.shikala.com'
    access_key = 'M0P0pT0ShSorWYCpePCi'
    secret_key = 'E0k68nU1A1VYJtVSKI3Eh7VMIPlJ5znmk9ib0LEF'
    file_overwrite = True
    default_acl = 'public-read'
    querystring_auth = False
    region_name = 'us-east-1'
    signature_version = 's3v4'
    addressing_style = 'path'
