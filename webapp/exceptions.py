from rest_framework.exceptions import APIException 


# 404 
class ObjectNotFoundException(APIException):
    status_code = 404
    default_detail = data={'message':'object not found','response_code':404}
    

