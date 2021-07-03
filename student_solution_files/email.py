"""
    Lambda Function used to send emails via Amazon SES.
    
    Author: Explore Data Science Academy.
    
    Note:
    ---------------------------------------------------------------------
    The contents of this file should be added to a AWS  Lambda function 
    created as part of the EDSA Cloud-Computing Predict. 
    For further guidance around this process, see the README instruction 
    file which sits at the root of this repo.
    ---------------------------------------------------------------------

"""

# Lambda dependencies
import boto3
import json  # Used for handling API-based data.
import base64  # Needed to decode the incoming POST data
from botocore.exceptions import ClientError  # Catch errors on client s



def lambda_handler(event, context):
    ses = boto3.client('ses')
    # Perform JSON data decoding
    body_enc = event['body']
    dec_dict = json.loads(base64.b64decode(body_enc))

    # Sample text that you would like to email to your recipient 
    # address from your sender address.
    email_text = 'Hello world'

    # ** SES Functionality **

    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    # --- Insert your code here ---
    SENDER = 'ntseleta@gmail.com'
    ses.send_mail(
        Source='ntseleta@gmail.com',
        Destination={
            'ToAddresses': [
                'ntselet@hotmail.com',
            ]
        },
        Message={
            'Subject': {
                'Data': 'Predict',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': email_text,
                    'Charset': 'UTF-8'
                },

            }
        },
    )
    # -----------------------------

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    # --- Insert your code here ---
    RECIPIENT = 'ntseleta@gmail.com'
    # -----------------------------

    # The subject line for the email.
    # --- DO NOT MODIFY THIS CODE ---
    SUBJECT = f"Data Science Portfolio Project Website - Hello {dec_dict['name']}"
    # -------------------------------

    # The email body for recipients with non-HTML email clients
    BODY_TEXT = (email_text)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES service resource
    client = client('ses')

    # Try to send the email.
    try:
        # Provide the contents of the email.
        ses_response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                    # 'edsa.predicts@explore-ai.net', # <--- Uncomment this line once you have successfully tested your predict end-to-end
                ],
            },
            Message={
                'Body': {

                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(ses_response['MessageId'])

    # ** Create a response object to inform the website 
    #    that the workflow executed successfully. **
    lambda_response = {
        'statusCode': 200,
        'body': json.dumps({
            'Name': dec_dict['name'],
            'Email': dec_dict['email'],
            'Cell': dec_dict['phone'],
            'Message': dec_dict['message'],
            'SES_response': ses_response,
            'Email_message': email_text
        })
    }

    return lambda_response
