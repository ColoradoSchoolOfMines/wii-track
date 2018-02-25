#! /usr/bin/env python3

import boto3
import json
import decimal
import sys

if len(sys.argv) != 3:
    raise Exception("Invalid parameters")

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

inventory = dynamodb.Table('Inventory')

with open(sys.argv[1]) as json_file:
    items = json.load(json_file, parse_float=decimal.Decimal)
    for item in items:
        name = item['name']
        weight = item['weight']
        deviation = item['deviation']

        print("Adding inventory item:", name, weight)

        inventory.put_item(
           Item={
               'name': name,
               'weight': weight,
               'info': {
                   'deviation': deviation,
               },
            }
        )

inventory_tracking = dynamodb.Table('InventoryTracking')

with open(sys.argv[2]) as json_file:
    items = json.load(json_file, parse_float=decimal.Decimal)
    for item in items:
        item_id = item['id']
        info = item['info']

        print("Adding inventory tracking item:", item_id)

        inventory_tracking.put_item(
           Item={
               'id': item_id,
               'info': info,
            }
        )
