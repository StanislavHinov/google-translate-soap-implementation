import zeep

WSDL = 'http://localhost:8000/?wsdl'

# country = 'DE'

client = zeep.Client(wsdl=WSDL)
result = client.service.translate_text( 
    text='Здравейте', 
    dest='en', 
    src='bg'
)

print(result)