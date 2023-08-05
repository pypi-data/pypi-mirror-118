import uuid
import requests
import json
import enum
import zipfile
import os


HELLO_WORLD_MESSAGE = 'Hello world! PyOhio Demo - 3! CLEpy'

API_GW = "https://qe3b75sz3m.execute-api.us-east-2.amazonaws.com/api/"

def get_message():
    return HELLO_WORLD_MESSAGE


def print_hello_world():
    print(get_message())

class FileType(enum.Enum):
    Train = 1
    Test = 2
    EntryPoint = 3
    Code = 4
    Inputs = 5
    mnist = 6
    MNIST = 7
    processed = 8
    output = 9


def create_training_job(local_train_data, local_test_data, entry_point, inputs_folder, hyper_param):

    # create job id

    job_id = str(uuid.uuid4())
    print(f"job id is: {job_id}")

    # upload data and code to s3
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
    if local_train_data is not None:
        __upload_one_file_infolder(job_id, FileType.mnist.name, FileType.MNIST.name, FileType.processed.name, local_train_data)
        print(f"upladed {local_train_data}")

    if local_test_data is not None:
        __upload_one_file_infolder(job_id, FileType.mnist.name, FileType.MNIST.name, FileType.processed.name, local_test_data)
        print(f"upladed {local_test_data}")

    if entry_point is not None:
        __upload_one_file(job_id, FileType.EntryPoint.name, entry_point)
        print(f"upladed {entry_point}")

    if inputs_folder is not None:
        pass

    # put hyper param to Dynamodb through API Gateway
    headers = {
        'Content-Type': 'application/json'
    }
    hyper_param.update({"jobid": job_id})
    payload = json.dumps(hyper_param)
    print(f"payload {payload}")
    response = requests.request("POST", f"{API_GW}/job", headers=headers, data=payload)

    print(response)

    return job_id

def folder_upload(jobid, rootDir): 
    for lists in os.listdir(rootDir): 
        path = os.path.join(rootDir, lists) 
        #print path 
        if os.path.isdir(path): 
            folder_upload(jobid, path)
        else:
            __upload_one_file(jobid, FileType.Inputs.name, path)


def get_training_job_status(job_id):

    # read status from API Gateay - backed by Dynamodb
    url = f"{API_GW}/jobs/{job_id}"
    print(f"getting {url}")
    response = requests.request("GET", url)
    print(f"response {response}")
    response_body = json.loads(response.text)
    print(response_body[job_id])
    return response_body[job_id]

def get_model(job_id, model):
    url = f"{API_GW}/s3urld/{job_id}/{FileType.output.name}/{model}"
    response = requests.get(url, allow_redirects=True)

    response_s3 = requests.get(response.__dict__['_content'])
    print(f"getting {url}")

    if response.status_code == 200:
        size = 2**10
        with open("./model.tar.gz", 'wb') as tar:
            for chunk in response_s3.iter_content(chunk_size=size):
                tar.write(chunk)
        tar.close()




    

def cancel_training_job_status(job_id):
    """
    If a job status is submited then it can be cancled.
    """
    pass

def get_zipfile(dirpath,outpath):
	"""
	zip file
	:dirpath: source
	:outpath: dest
	"""

	zip = zipfile.ZipFile(outpath, "w", zipfile.ZIP_STORED)
	for path, dirnames, filenames in os.walk(dirpath):
		fpath = path.replace(dirpath, '')
		for filename in filenames:
			zip.write(os.path.join(path, filename), os.path.join(fpath,filename))
	zip.close()



##############################################
# Helpers
##############################################

def __upload_one_file(job_id, type, object_name):

    # request a s3 presigned URL
    url = f"{API_GW}/s3url/{job_id}/{type}/{object_name}"
    print(f"getting {url}")
    response = requests.request("GET", url)
    print(f"response {response}")
    response_body = json.loads(response.text)


    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response_body['url'], data=response_body['fields'], files=files)
    # If successful, returns HTTP status code 204
    print(f'File upload HTTP status code: {http_response.status_code}')

def __upload_one_file_infolder(job_id, type1, type2, type3, object_name):

    # request a s3 presigned URL
    url = f"{API_GW}/s3urlf/{job_id}/{type1}/{type2}/{type3}/{object_name}"
    print(f"getting {url}")
    response = requests.request("GET", url)
    print(f"response {response}")
    response_body = json.loads(response.text)


    with open(object_name, 'rb') as f:
        files = {'file': (object_name, f)}
        http_response = requests.post(response_body['url'], data=response_body['fields'], files=files)
    # If successful, returns HTTP status code 204
    print(f'File upload HTTP status code: {http_response.status_code}')



if __name__ == "__main__":
    #__upload_one_file("11112222", "mnist/MNIST/processed", "buffer1.txt")
    #create_training_job("training.pt", "test.pt", "buffer1.txt", None, {"epoch":"10"})
    #get_zipfile("./test","./test.zip")
    #folder_upload("test")
    #get_training_job_status("125cddd2-6686-44c2-8e14-1e4fe882ad94")
    get_model("125cddd2-6686-44c2-8e14-1e4fe882ad94", "model.tar.gz")