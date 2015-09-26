import customFunctions
import json
import urllib
import urllib2

def buildFullUrl(path, parametersArray) :
    full_url = path
    if parametersArray is not None:
        url_values = urllib.urlencode(parametersArray)
        full_url = full_url + '?' + url_values
    customFunctions.printToLog('buildFullUrl: ' + full_url, 1)
    return full_url

#Helper function to take in a JSON object and convert it to a normal Python array	
def convertJsonToArray(jsonObject) :
    customFunctions.printToLog('convertJsonToArray: ' + jsonObject, 1)
    pythonArray = json.loads(jsonObject)
    return pythonArray
	
#Helper function to take in a normal Python array and convert it to a JSON object
def convertArrayToJson(array) :
	jsonObject = json.dumps(array)
	customFunctions.printToLog('convertArrayToJson: ' + jsonObject, 1)
	return jsonObject
	
def postRequest(url, parametersArray = None, headersArray = None) :
    #Logging
    if parametersArray is not None:
        for key, value in parametersArray.iteritems():
            customFunctions.printToLog('postRequest: parametersArray: ' + key + ': ' + value, 0)
    if headersArray is not None:
        for key, value in headersArray.iteritems():
            customFunctions.printToLog('postRequest: headersArray: ' + key + ': ' + value, 0)
    customFunctions.printToLog('postRequest: url: ' + url, 1)
    #Send the request and return the response to caller.
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response

def getRequest(url, parametersArray = None, headersArray = None) :
    #Logging
    if parametersArray is not None:
        for key, value in parametersArray.iteritems():
            customFunctions.printToLog('getRequest: parametersArray: ' + key + ': ' + value, 0)
    if headersArray is not None:
        for key, value in headersArray.iteritems():
            customFunctions.printToLog('getRequest: headersArray: ' + key + ': ' + value, 0)
    customFunctions.printToLog('getRequest: url: ' + url, 1)
    #Send the request and return the response to caller.
    #Build the final URL and the Request object
    full_url = buildFullUrl(url, parametersArray)
    req = urllib2.Request(full_url)
    #Loop through array of headers and add them to the request headers. 
    if headersArray is not None:
        for key, value in headersArray.iteritems():
            req.add_header(key,value)
    #Send the request and get the response
    response = urllib2.urlopen(req)
    responseData = response.read()
    customFunctions.printToLog('getRequest: ' + responseData, 1)
    return responseData
