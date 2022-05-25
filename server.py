# Added spyne dependencies to run a basic application
# Used as refference - https://github.com/arskom/spyne/blob/master/examples/helloworld_soap.py
# WsgiMounter is used to create multiple endpoints - https://stackoverflow.com/questions/20275836/deploy-multiple-web-services-i-e-multiple-wsdl-files-in-python

from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.util.wsgi_wrapper import WsgiMounter

# Google translate free python library - https://pypi.org/project/googletrans/

from googletrans import Translator

# As per the spyne documentation each application should be separeted into classes


class googleTranslateService(ServiceBase):
    @rpc(String, String, String, _returns=String)
    def translate_text(ctx, text, dest, src):
        translator = Translator()
        result = translator.translate(text=text, dest=dest, src=src)
        return result.text


class googleLanguageDetectService(ServiceBase):
    @rpc(String, _returns=String)
    def detect_text(ctx, text):
        translator = Translator()
        result = translator.detect(text)
        return result.lang


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
