import json
import saveReason
import randomQuestion

def lambda_handler(event, context):
    print(event)
    
    intentName = event ['interpretations'][0]['intent']['name']
    
    if intentName=='demo-welcome':
        response = saveReason.main(event)
    elif intentName=='random-question' or intentName=='validate-question':
        response = randomQuestion.main(event)
    
    print('result = ' + str(response))
    
    return response
    


