#!/usr/bin/env python3
from PIL import Image
import base64
import io
from math import sqrt
import json

import boto3


threshold = 120


def lambda_handler(event, context):
    j = json.loads(event['body'])
    b64 = j['image']
    f = io.BytesIO(base64.b64decode(b64))
    im = Image.open(f)

    sums = [0, 0, 0]
    n = 0
    for x in range(im.size[0]):
        for y in range(im.size[1]):
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

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('InventoryTracking')

    table.update_item(
        Key={
            'id': item_id
        },
        UpdateExpression="set info.color = :c, info.image = :i",
        ExpressionAttributeValues={
            ':c': ','.join(map(str, sums)),
            ':i': b64,
        },
    )

    response = {
        'statusCode': 200,
    }

    return response
