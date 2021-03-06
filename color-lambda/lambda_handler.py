#!/usr/bin/env python3
from PIL import Image
import base64
import io
from math import sqrt
import json
from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Attr, Key


threshold = 120


def lambda_handler(event, context):
    j = json.loads(event['body'])
    b64 = j['image']
    f = io.BytesIO(base64.b64decode(b64))
    im = Image.open(f)

    sums = [0, 0, 0]
    n = 0
    for x in range(0, im.size[0], 5):
        for y in range(0, im.size[1], 5):
            pixel = im.getpixel((x, y))
            if pixel[0] < threshold or \
               pixel[1] < threshold or \
               pixel[2] < threshold:
                sums[0] += pixel[0] ** 2
                sums[1] += pixel[1] ** 2
                sums[2] += pixel[2] ** 2
                n = n + 1

    item_id = int(j['id'])

    sums = map(lambda x: sqrt(x / n), sums)

    color_csv = ','.join(map(str, sums))

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('InventoryTracking')

    existing_entry = table.query(
        KeyConditionExpression=Key('id').eq(item_id),
    )

    if existing_entry['Count'] == 1:
        table.update_item(
            Key={
                'id': item_id
            },
            UpdateExpression="set info.color = :c, info.image = :i, info.missing_sources = :m",
            ExpressionAttributeValues={
                ':c': color_csv,
                ':i': b64,
                ':m': [],
            },
        )
    else:
        table.put_item(
            Item={
                'id': item_id,
                'info': {
                    'missing_sources': ['weight'],
                    'time': str(datetime.now()),
                    'color': color_csv,
                    'image': b64,
                }
            }
        )

    response = {
        'statusCode': 200,
    }

    return response
