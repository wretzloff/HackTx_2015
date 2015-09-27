import httpFunctions

@auth.requires_login()
def index():
    #Get the ID of the logged in user
    loggedInUserQuery = (db.auth_user.id == auth.user.id)
    loggedInUserResults = db(loggedInUserQuery).select()
    logged_in_user_id = loggedInUserResults[0].id
    
    #Use the ID of the logged in user to get a list of devices that the user has authenticated with.
    devicesList = []
    credentialsRows = db(db.credentials.account == logged_in_user_id).select(join=db.resourceOwners.on(db.credentials.resourceOwner==db.resourceOwners.id))
    
    #Build a list of devices to send to the view.
    for row in credentialsRows:
        deviceListRecord = []
        deviceListRecord.append(row.resourceOwners.resourceOwnerName)
        deviceListRecord.append(row.resourceOwners.id)
        devicesList.append(deviceListRecord)
    
    #Build a list of available resource owners that are available to authenticate with.
    #resourceOwnerRows = db(db.resourceOwners).select()
    #for resourceOwnerRow in resourceOwnerRows:
    #    print resourceOwnerRow.resourceOwnerName
    
    return dict(devicesList = devicesList)

def redirectUri_Up():
    parameterCode = request.vars['code']
    requestBodyParameters = {'grant_type' : 'authorization_code',
                             'code' : parameterCode,
                             'client_id' : 'GmMxBR58418',
                             'client_secret' : '9075fb17326254ff2d7072a625ae09e638a142d9'}
    #Call the function to send the HTTP POST and get the response
    responseFromPost = httpFunctions.postRequest('https://jawbone.com/auth/oauth2/token', requestBodyParameters)
    #Parse the response and return the data to the caller.
    responseDataInJson = responseFromPost.read()
    responseDataInArray = httpFunctions.convertJsonToArray(responseDataInJson)
    print responseDataInArray['access_token']
    print responseDataInArray['token_type']
    print responseDataInArray['expires_in']
    print responseDataInArray['refresh_token']
    
    #Get the ID of the logged in user so it can be used to insert a record into the database.
    loggedInUserQuery = (db.auth_user.id == auth.user.id)
    loggedInUserResults = db(loggedInUserQuery).select()
    logged_in_user_id = loggedInUserResults[0].id
    
    #Get the ID of Up so it can be used to insert a record into the database.
    resourceOwnerQuery = (db.resourceOwners.resourceOwnerName == 'Up')
    resourceOwnerResults = db(resourceOwnerQuery).select()
    resourceOwnerid = resourceOwnerResults[0].id
    
    #Insert the credentials
    db.credentials.insert(account=logged_in_user_id, resourceOwner=resourceOwnerid, accessToken=responseDataInArray['access_token'], tokenType=responseDataInArray['token_type'], expiresIn=responseDataInArray['expires_in'],refreshToken=responseDataInArray['refresh_token'])
    redirect(URL('index'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
