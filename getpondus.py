# importing the requests library
import requests
import shutil
import time
import boto3
from secrets import *

# AWS Stuff
MyS3 = boto3.resource('s3', aws_access_key_id=my_aws_access_key_id,
                      aws_secret_access_key=my_aws_secret_access_key)
targetBucket = 'mclonberg-pondus'

# Could add automation here to retrieve the list of strips
stripList = ['hanneland', 'hjalmar', 'lunch', 'pondus', 'storefri']
curdate = time.strftime("%Y-%m-%d", time.localtime())

# Get today's strips
for strip in stripList:
    curstrip = strip
    # api-endpoint
    URL = "https://www.vg.no/tegneserier/api/images/" + \
        curstrip + "/" + curdate + ".webp"
    headers = {"cookie": "SP_ID=eyJjbGllbnRfaWQiOiI0ZWYxY2ZiMGU5NjJkZDJlMGQ4ZDAwMDAiLCJhdXRoIjoiZDFkNC1lWmwtRGtLWHRRRWV0ZVdJYlpYZF9jU3NnYUdGXzFHb3E0ak5feHhVdkJSd2VHQjhnVEZtdnN6RWtXZnB6bDFZVDBvRFlqVW9pSWhTQkNnaEtHZklRME8wU3hsQkJwcnFaczhyeGsifQ;"}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, headers=headers, stream=True)
    curfile = 'img/' + curstrip + '-' + curdate + '.webp'
    targetfile = 'img/' + curdate + '/' + curstrip + '.webp'
    
    if r.status_code == 200:
        with open(curfile, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        # Once file is complete, write it to AWS
        MyS3.Bucket(targetBucket).upload_file(curfile, targetfile)
        #  Add SNS Notification?
    else:
        print(r.status_code)
        #  Add SNS Notification?
