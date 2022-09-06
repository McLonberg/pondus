import shutil
import time
import boto3
import requests


print('Loading Function')


def lambda_handler(event, context):
    # AWS Stuff
    my_s3 = boto3.resource('s3')
    my_sns = boto3.client('sns')
    target_bucket = 'mclonberg-pondus'

    # Could add automation here to retrieve the list of strips
    # stripList = ['hanneland', 'hjalmar', 'lunch', 'pondus', 'storefri']
    # //  Hanneland removed 27/08/2020 and replaced with Zelda
    # Storefri re-added 07/03/2022
    strip_list = ['gjesteserie', 'hjalmar', 'lunch', 'pondus', 'storefri', 'hanneland']
    curdate = time.strftime("%Y-%m-%d", time.localtime())
    sns_message = 'Comic Strip status for ' + curdate + '\n'

    # Get today's strips
    for strip in strip_list:
        curstrip = strip
        # api-endpoint
        target_url = "https://www.vg.no/tegneserier/api/images/" + \
            curstrip + "/" + curdate + ".webp"
        headers = {"cookie": \
            "SP_ID=eyJjbGllbnRfaWQiOiI0ZWYxY2ZiMGU5NjJkZDJlMGQ4ZDAwMDAiLCJhdXRoIjoiZDFkNC1lWmwtRGtLWHRRRWV0ZVdJYlpYZF9jU3NnYUdGXzFHb3E0ak5feHhVdkJSd2VHQjhnVEZtdnN6RWtXZnB6bDFZVDBvRFlqVW9pSWhTQkNnaEtHZklRME8wU3hsQkJwcnFaczhyeGsifQ;"}

        # sending get request and saving the response as response object
        req_call = requests.get(url=target_url, headers=headers, stream=True)
        curfile = '/tmp/' + curstrip + '-' + curdate + '.webp'
        targetfile = 'img/' + curdate + '/' + curstrip + '.webp'

        if req_call.status_code == 200:
            with open(curfile, 'wb') as output_file:  # Creating a binary file
                req_call.raw.decode_content = True
                shutil.copyfileobj(req_call.raw, output_file)

            print(curstrip + ' for ' + curdate + ' copied')

            # Once file is complete, write it to AWS
            my_s3.Bucket(target_bucket).upload_file(curfile, targetfile)
            #  SNS Mesage Construct
            sns_message = sns_message + curstrip + ' - successfully downloaded\n'
        else:
            print(req_call.status_code)
            #  SNS Mesage Construct
            sns_message = sns_message + curstrip + ' - failed\n'

    # print(SNS_message)
    my_sns.publish(
        TopicArn='arn:aws:sns:eu-west-1:575052121955:MyDailyPondus',
        Subject='My Daily Pondus',
        Message=sns_message)

    print('Function complete')
