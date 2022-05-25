import zeep

WSDL = 'http://localhost:8000/app2/?wsdl'

# country = 'DE'

client = zeep.Client(wsdl=WSDL)
result = client.service.detect_text( 
    text='Здравейте', 
    # dest='en', 
    # src='bg'
)

print(result)