#! /usr/bin/env python3
# Standard Libraries
import json
import math
from decimal import Decimal
from datetime import datetime

# AWS Libraries
import boto3
from boto3.dynamodb.conditions import Attr, Key

# 3rd Party Libraries
from scipy.stats import norm


def lambda_handler(event, context):
    """Calculate what we think this object is."""

    item_id = 1  # TODO: make this come from the event data

    print('DEBUG: EVENT:', event)
    # Calculate the average
    total = 0
    n = 0
    for sample in json.loads(event['body']):
        print('DEBUG: Sample is: ', sample)
        for data in sample:
            print('DEBUG: data is', data)
            n += 1
            total += (int(data['top_left']) +
                      int(data['top_right']) +
                      int(data['bottom_left']) +
                      int(data['bottom_right']))

    average = total / n

    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Inventory')

    max_tolerance = 4  # Hard coding this because IT'S A HACKATHON!!!

    # Find all of the possible items with tolerances in the range.
    low = Decimal(average - max_tolerance)
    high = Decimal(average + max_tolerance)
    potential_items = table.scan(
        FilterExpression=Attr('weight').between(low, high),
    )

    confidences = []

    for item in potential_items[u'Items']:
        # Use a normal distribution to determine how confidant we are that this
        # item is the item that was measured.
        diff = float(item['weight']) - average
        sd = float(item['info']['deviation'])
        max_height = 1 / (math.sqrt(2 * math.pi) * sd)
        confidence = norm.pdf(0, loc=diff, scale=sd) / max_height * 100
        confidences.append({
            'item': item['name'],
            'confidence': confidence,
        })

    inventory_tracking = dynamodb.Table('InventoryTracking')
    existing_entry = inventory_tracking.query(
        KeyConditionExpression=Key('id').eq(item_id),
    )

    if existing_entry['Count'] == 1:
        # If the entry is not expecting weight, blow up.
        if 'weight' not in existing_entry['Items']['info']['missing_sources']:
            return {
                'statusCode': 500,
            }

        # TODO: merge confidences

        inventory_tracking.update_item(
            Key={
                'id': item_id,
            },
            UpdateExpression='set info.missing_sources = :m, info.probabilities=:p',
            ExpressionAttributeValues={
                ':m': [],
                ':p': confidences,
            },
        )
    else:
        inventory_tracking.put_item(
            Item={
                'id': item_id,
                'info': {
                    'missing_sources': ['image'],
                    'probabilities': confidences,
                    'time': str(datetime.now()),
                }
            }
        )

    response = {
        'statusCode': 200,
    }
    return response
