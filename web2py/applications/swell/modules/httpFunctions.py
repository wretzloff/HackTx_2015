import json
import urllib
import urllib2

def buildFullUrl(path, parametersArray) :
    full_url = path
    if parametersArray is not None:
        url_values = urllib.urlencode(parametersArray)
        full_url = full_url + '?' + url_values
    return full_url

#Helper function to take in a JSON object and convert it to a normal Python array	
def convertJsonToArray(jsonObject) :
    pythonArray = json.loads(jsonObject)
    return pythonArray
	
#Helper function to take in a normal Python array and convert it to a JSON object
def convertArrayToJson(array) :
	jsonObject = json.dumps(array)
	return jsonObject
	
def postRequest(url, parametersArray = None, headersArray = None) :
    #Send the request and return the response to caller.
    data = urllib.urlencode(parametersArray)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return response

def getRequest(url, parametersArray = None, headersArray = None) :
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
    return responseData
