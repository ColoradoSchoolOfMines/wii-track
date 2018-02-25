#! /usr/bin/env python3

import boto3
import json
import decimal
import sys

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

table = dynamodb.Table('Inventory')

if len(sys.argv) != 2:
    raise Exception('Invalid parameters. Please enter filename.')

with open(sys.argv[1]) as json_file:
    items = json.load(json_file, parse_float=decimal.Decimal)
    for item in items:
        name = item['name']
        weight = item['weight']
        deviation = item['deviation']

        print("Adding inventory item:", name, weight)

        table.put_item(
           Item={
               'name': name,
               'weight': weight,
               'info': {
                   'deviation': deviation,
               },
            }
        )
