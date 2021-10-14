from __future__ import print_function

# get the list of files
import re

import boto3

s3 = boto3.resource('s3')
my_bucket = s3.Bucket('fedor-malyshkin')

files = [f for f in my_bucket.objects.filter(Prefix="bbc-why-factor/") if f.key.endswith(".mp3")]

files = files[0:1]
transcribe = boto3.client('transcribe')
for s3_file in files:
    job_name = s3_file.key[15:]
    job_name = re.sub(r'\.mp3$', '', job_name)
    job_uri = "s3://fedor-malyshkin/" + s3_file.key
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        LanguageCode="en-GB",
        MediaSampleRateHertz=44100,
        MediaFormat="mp3",
        OutputBucketName="fedor-malyshkin",
        OutputKey="bbc-why-factor/",
        Subtitles={"Formats": ['srt']}
    )
