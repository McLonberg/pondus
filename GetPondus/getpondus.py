# importing libraries incl requests
import requests
import shutil
import time
import boto3

print('Loading Function')

def lambda_handler(event, context):
    # AWS Stuff
    MyS3 = boto3.resource('s3')
    targetBucket = 'mclonberg-pondus'

    # Could add automation here to retrieve the list of strips
    stripList = ['hanneland', 'hjalmar', 'lunch', 'pondus', 'storefri']
    curdate = time.strftime("%Y-%m-%d", time.localtime())
    SNS_message = 'Comic Strip status for ' + curdate + '\n'

    # Get today's strips
    for strip in stripList:
        curstrip = strip
        # api-endpoint
        URL = "https://www.vg.no/tegneserier/api/images/" + \
            curstrip + "/" + curdate + ".webp"
        headers = {"cookie": "SP_ID=eyJjbGllbnRfaWQiOiI0ZWYxY2ZiMGU5NjJkZDJlMGQ4ZDAwMDAiLCJhdXRoIjoiZDFkNC1lWmwtRGtLWHRRRWV0ZVdJYlpYZF9jU3NnYUdGXzFHb3E0ak5feHhVdkJSd2VHQjhnVEZtdnN6RWtXZnB6bDFZVDBvRFlqVW9pSWhTQkNnaEtHZklRME8wU3hsQkJwcnFaczhyeGsifQ;"}

        # sending get request and saving the response as response object
        r = requests.get(url=URL, headers=headers, stream=True)
        curfile = '/tmp/' + curstrip + '-' + curdate + '.webp'
        targetfile = 'img/' + curdate + '/' + curstrip + '.webp'

        if r.status_code == 200:
            with open(curfile, 'wb') as f:  # Creating a binary file
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

            print(curstrip + ' for ' + curdate + ' copied')

            # Once file is complete, write it to AWS
            MyS3.Bucket(targetBucket).upload_file(curfile, targetfile)
            #  SNS Mesage Construct
            SNS_message = SNS_message + curstrip + ' - successfully downloaded\n'
        else:
            print(r.status_code)
            #  SNS Mesage Construct
            SNS_message = SNS_message + curstrip + ' - failed\n'

    print(SNS_message)
    print('Function complete')