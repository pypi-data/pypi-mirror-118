"""
Copyright 2021-present Airbnb, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import ssl
import sys
from datetime import datetime, timedelta
from typing import List

import OpenSSL
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

from .logger import get_logger

LOGGER = get_logger(__name__)


def get_secret(path, element=None, region: str = 'us-east-1') -> str:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=path
        )
    except ClientError as error:
        raise error
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            if element is None:
                return secret
            else:
                output = json.loads(secret)
                return output[element]


def query_subject_alternative_names(hostname, table) -> List[str]:
    response = table.query(
        IndexName='system_name_index',
        KeyConditionExpression=Key('system_name').eq(hostname))

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items'][0]['subject_alternative_name']
    else:
        LOGGER.error('DynamoDB Returned Invalid HTTPStatusCode')
        sys.exit(1)


def update_certificate_expiration(hostname, table, certificate_expiration) -> None:
    try:
        _ = datetime.fromisoformat(certificate_expiration)
        response = table.update_item(
            Key={
                'system_name': hostname
            },
            UpdateExpression="SET certificate_expiration = :certificate_expiration",
            ExpressionAttributeValues={
                ":certificate_expiration": certificate_expiration
            },
            ReturnValues="UPDATED_NEW"
        )
        LOGGER.info(response)
    except Exception as error:
        LOGGER.error(error)
        sys.exit(1)


def query_certificate_expiration(system_name: str) -> str:
    cert = ssl.get_server_certificate(
        ('{hostname}'.format(hostname=system_name), 443))
    x509 = OpenSSL.crypto.load_certificate(
        OpenSSL.crypto.FILETYPE_PEM, cert)
    certificate_expiration = datetime.strptime(
        x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').isoformat()
    lets_encrypt_certificate_duration = (
        datetime.utcnow() + timedelta(days=89)).isoformat()
    certificate_issuer = x509.get_issuer().O
    LOGGER.info(certificate_issuer)
    LOGGER.info(certificate_expiration)

    if certificate_expiration > lets_encrypt_certificate_duration and certificate_issuer in ["Let's Encrypt", "(STAGING) Let's Encrypt"]:
        return certificate_expiration
    else:
        LOGGER.error('Failure to Upload Certificate to Device')
        sys.exit(1)
