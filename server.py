# Added spyne dependencies to run a basic application
# Used as refference - https://github.com/arskom/spyne/blob/master/examples/helloworld_soap.py
# WsgiMounter is used to create multiple endpoints - https://stackoverflow.com/questions/20275836/deploy-multiple-web-services-i-e-multiple-wsdl-files-in-python

from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.util.wsgi_wrapper import WsgiMounter
import requests
import json
import codecs

# As per the spyne documentation each application should be separeted into classes
# Since Google Translate API is a payed service an alternative freemium is used - https://rapidapi.com/armangokka/api/translo/details


class googleTranslateService(ServiceBase):
    @rpc(String, String, String, _returns=String)
    def translate_text(ctx, text, dest, src):
        url = "https://translo.p.rapidapi.com/api/v3/translate"

        payload = "from=" + src + "&to=" + dest + "&text=" + text
        payload = codecs.encode(payload, "utf-8")
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Host": "translo.p.rapidapi.com",
            "X-RapidAPI-Key": "PASTE-API-KEY-HERE"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        k = json.loads(response.text)
        return k["translated_text"]


class googleLanguageDetectService(ServiceBase):
    @rpc(String, _returns=String)
    def detect_text(ctx, text):
        url = "https://translo.p.rapidapi.com/api/v3/detect"

        querystring = {"text": text}

        headers = {
            "X-RapidAPI-Host": "translo.p.rapidapi.com",
            "X-RapidAPI-Key": "PASTE-API-KEY-HERE"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        k = json.loads(response.text)
        return k["lang"]


translateService = Application([googleTranslateService], 'google.translate.soap',
                               in_protocol=Soap11(validator='lxml'),
                               out_protocol=Soap11())

languageDetectService = Application([googleLanguageDetectService], 'google.translate.soap',
                                    in_protocol=Soap11(validator='lxml'),
                                    out_protocol=Soap11())

wsgi_application = WsgiMounter({
    'translate': translateService,
    'detect': languageDetectService,
})


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000/translate")
    logging.info("wsdl is at: http://localhost:8000/translate/?wsdl")
    logging.info("listening to http://127.0.0.1:8000/detect")
    logging.info("wsdl is at: http://localhost:8000/detect/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
