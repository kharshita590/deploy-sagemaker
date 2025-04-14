import json
import boto3

def invoke_sagemaker_endpoint(endpoint_name, input_data):
    runtime = boto3.client('sagemaker-runtime')
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='text/plain',
        Body=input_data
    )
    audio_bytes=response['Body'].read()
    return audio_bytes
audio_data=invoke_sagemaker_endpoint("kippss-tts","hello i am harshita")
with open("output.wav", "wb") as f:
    f.write(audio_data)




