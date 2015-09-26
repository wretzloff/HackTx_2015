@auth.requires_login()
def index():
    #Get the ID of the logged in user
    loggedInUserQuery = (db.auth_user.id == auth.user.id)
    loggedInUserResults = db(loggedInUserQuery).select()
    logged_in_user_id = loggedInUserResults[0].id
    
    #Use the ID of the logged in user to get a list of devices that the user has authenticated with.
    credentialsQuery = (db.credentials.account == logged_in_user_id)
    credentialsResults = db(credentialsQuery).select()
    devicesList = []
    for credentialsRow in credentialsResults:
        #Get the text of the email
        resourceOwnerName = credentialsRow.resourceOwner
        devicesList.append(resourceOwnerName)
    
    return dict(message=T('Hello World'), devicesList = devicesList)


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
