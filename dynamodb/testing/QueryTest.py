#! /usr/bin/env python3
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr, Between


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('Inventory')

potential_items = table.scan(
    FilterExpression=Attr('weight').between(54, 62),
)

for i in potential_items[u'Items']:
    print(i)
    print(json.dumps(i, cls=DecimalEncoder))

print(table.query(
    KeyConditionExpression=Key('weight').eq(1) & Key('name').eq('ohea'),
))
