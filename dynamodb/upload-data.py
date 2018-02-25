#! /usr/bin/env python3

import boto3
import json
import decimal

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

inventory = dynamodb.Table('Inventory')

inventory_file = input('Enter Inventory JSON file:')

with open(inventory_file) as json_file:
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

inventory_tracking_file = input('Enter InventoryTracking JSON file:')
inventory_tracking = dynamodb.Table('InventoryTracking')

with open(inventory_tracking_file) as json_file:
    items = json.load(json_file, parse_float=decimal.Decimal)
    for item in items:
        item_id = item['id']
        info = item['info']

        print("Adding inventory tracking item:", item_id)

        inventory.put_item(
           Item={
               'id': item_id,
               'info': info,
            }
        )
