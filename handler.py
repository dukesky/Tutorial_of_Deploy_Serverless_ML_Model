import json
from sklearn.externals import joblib

# cold start
# load model also need to be run

# warm start
# only lambda function(predict) will run
# that's why load model need to be placed out of lambda function

model_name = 'regreession_model_1585449038.4613056.joblib'
model = joblib.load(model_name)

def predict(event, context):
    body = {
        "message": "OK",
    }

    if 'queryStringParameters' in event.keys():

        params = event['queryStringParameters']

        medInc = float(params['medInc'])/100000
        houseAge =  float(params['houseAge'])
        aveRooms = float(params['aveRooms'])
        aveBedrms = float(params['aveBedrms'])
        population = float(params['population'])
        aveOccup = float(params['aveOccup'])
        latitude = float(params['latitude'])
        longitude = float(params['longitude']) 
    
        inputVector = [medInc, houseAge, aveRooms, aveBedrms, population, aveOccup, latitude, longitude]

        data = [inputVector]
        predictedPrice = model.predict(data)[0] *1000000
        predictedPrice = round(predictedPrice,2)
        body['predictedPrice'] = predictedPrice

        print(params)
        print(predictedPrice)
        print('finish one API calling')

    else:
        body["message"] = 'queryStringParameters not in event.'
    
    print(body['message'])


    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": 'application/json',
            'Access-Control-Allow-Origin': "*" ,
            # cross origin request sharing

        }
        
    }

    return response

def test():
    event = {
        'queryStringParameters': {
            'medInc': 200000,
            'houseAge': 10,
            'aveRooms': 4,
            'aveBedrms': 1,
            'population': 800,
            'aveOccup': 3,
            'latitude': 37.54,
            'longitude': -121.72
        }
    }

    response = predict(event, None)

    body = json.loads(response['body'])

    print(response)
    print('Price',body['predictedPrice'])
    
    with open('event.json','w') as event_file:
        event_file.write(json.dumps(event))

#test()