import azure.functions as func
import logging
import base64
import json;

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

def enccryptData(data):
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def decryptData(data):
    return base64.b64decode(data.encode('utf-8')).decode('utf-8')

@app.route(route="encryptUserName")
def encryptUserName(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userName = req.params.get('userName')
    if not userName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userName = req_body.get('userName')

    if userName:
        encryptedName = enccryptData(userName)
        #return func.HttpResponse(f"Hello, here is the encrypted name - {encryptedName}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(json.dumps({'success': True, 'encryptedName':encryptedName}),mimetype='application/json')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="decryptUserName", auth_level=func.AuthLevel.ANONYMOUS)
def decryptUserName(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    userName = req.params.get('userName')
    if not userName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('userName')

    if userName:
        decryptedName = decryptData(userName)
        #return func.HttpResponse(f"Hello, {userName}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(json.dumps({'success': True, 'encryptedName':decryptedName}),mimetype='application/json')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )