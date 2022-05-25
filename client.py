# Zeep is a python SOAP client - https://docs.python-zeep.org/en/master/

import zeep

WSDL = 'http://localhost:8000/detect/?wsdl'

# WSDL = 'http://localhost:8000/translate/?wsdl'

client = zeep.Client(wsdl=WSDL)

# result = client.service.translate_text( 
#     text='Здравейте', 
#     dest='en', 
#     src='bg'
# )

result = client.service.detect_text( 
    text='Здравейте', 
    # dest='en', 
    # src='bg'
)

print(result)