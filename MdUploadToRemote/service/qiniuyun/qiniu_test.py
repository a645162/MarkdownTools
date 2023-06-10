from qiniu import Auth
from qiniu import put_data
import qiniu_config

qiniu_config = qiniu_config.QiniuConfig()

access_key = qiniu_config.access_key
secret_key = qiniu_config.secret_key

bucket_name = qiniu_config.bucket_name

q = Auth(access_key, secret_key)

token = q.upload_token(bucket_name)

key = 'a/bc/你好.html'
data = 'hello bubby!'
token = q.upload_token(bucket_name)
ret, info = put_data(token, key, data)
print(info)
assert ret['key'] == key

# data = 'hello bubby!'
# token = q.upload_token(bucket_name, key)
# ret, info = put_data(token, key, data, mime_type="application/octet-stream", check_crc=True)
# print(info)
# assert ret['key'] == key
