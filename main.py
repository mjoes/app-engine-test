import time
from loguru import logger
from google.cloud import storage

client = storage.Client()
bucket = client.bucket('auphonic-storage')
for blob in bucket.list_blobs(prefix='auphonic/'):
    if blob.name == 'auphonic/':
        pass
    else:
        print(blob.name)
print("DONE NOW")

# def function_test():
#     i=0
#     k=0
#     while i < 10:
#         k=k+1
#         time.sleep(1)
#         logger.info(f"logging {k}")
#         print(f"test print no: {k}")

# function_test()