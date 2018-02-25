#! /usr/bin/env python3
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

print('Create Inventory table')

inventory = dynamodb.create_table(
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

print("Table status:", inventory.table_status, end='\r')

print('Create InventoryTracking table')
inventory_tracking = dynamodb.create_table(
    TableName='InventoryTracking',
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH',
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'N',
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 1,
        'WriteCapacityUnits': 1,
    },
)

print("Table status:", inventory_tracking.table_status, end='\r')
