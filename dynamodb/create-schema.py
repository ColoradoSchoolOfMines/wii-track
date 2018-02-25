#! /usr/bin/env python3
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

print('Create Inventory table')

table = dynamodb.create_table(
    TableName='Inventory',
    KeySchema=[
        {
            'AttributeName': 'name',
            'KeyType': 'HASH',
        },
        {
            'AttributeName': 'weight',
            'KeyType': 'RANGE',
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'name',
            'AttributeType': 'S',
        },
        {
            'AttributeName': 'weight',
            'AttributeType': 'N',
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1,
    },
)

print("Table status:", table.table_status, end='\r')
