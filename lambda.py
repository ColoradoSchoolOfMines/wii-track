def lambda_handler(event, context):
    import json
    average = 0
    n = 0
    for sample in json.loads(event['body']):
        print("Sample is: ", sample)
        for data in sample:
            print("data is", data)
            n += 1
            average += int(data['top_left']) + int(data['top_right']) + int(data['bottom_left']) + int(data['bottom_right'])
    response = {
        "statusCode": 200,
        "headers": {
            "my_header": "my_value"
        },
        "body": average / n,
        "isBase64Encoded": False
    }
    return response
