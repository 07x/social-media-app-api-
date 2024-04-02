from rest_framework.response import Response 



class CustomResponse(Response):

    def __init__(self,message=None,data=None,status=None):

        response = {
            "message"           : message,
            "response_code"     : status,
            "data"              : data ,
        }
        super().__init__(response,status=status)


        
        