from spyne import Application, rpc, ServiceBase, Iterable, Unicode, String, AnyXml

from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication


from googletrans import Translator

class googleTranslateService(ServiceBase):
    @rpc(String, String, String, _returns=String)
    def translate_text(ctx, text, dest, src):
        translator = Translator()
        result = translator.translate(text=text, dest=dest, src=src)
        return result.text


application = Application([googleTranslateService], 'google.translate.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
