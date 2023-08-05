# -*- coding: utf-8 -*-


from monkey.crawler.crawler import Crawler
from monkey.crawler.processor import Processor


class SOAPCrawler(Crawler):

    def __init__(self, source_name: str, processor: Processor, wsdl: str, operation_name: str, offset: int = 0,
                 max_retry: int = 0, wsse=None, transport=None, service_name=None, port_name=None, plugins=None,
                 settings=None, soap_header=None, soap_body=None):
        """Instantiates a crawler on an ODBC data source
        :param source_name: the name of the data source
        :param processor: the processor that will process every records
        :param wsdl: the string URL of endpoint WSDL
        :param operation_name
        :param offset: indicates if many records have to be skipped before starting to process the data (0 by default)
        :param max_retry: indicates how many time the processing can be retried when it raises a recoverable error
        :param wsse:
        :param transport: the request session
        :param service_name:
        :param port_name:
        :param plugins: a list of zeep plugins to enable
        :param settings:
        :param soap_header: the SOAP payload elements
        :param soap_body: the SOAP payload body elements
        """
        super().__init__(source_name, processor, offset, max_retry)
        self.wsdl: str = wsdl
        self.operation_name = operation_name
        self.wsse = wsse
        self.transport = transport
        self.service_name = service_name
        self.port_name = port_name
        self.plugins = plugins
        self.settings = settings
        self.soap_header = soap_header
        self.soap_body = soap_body

    def _get_records(self):
        from zeep import Client
        self._client = Client(self.wsdl, wsse=self.wsse, transport=self.transport, service_name=self.service_name,
                              port_name=self.port_name, plugins=self.plugins, settings=self.settings)
        result = self._client.service[self.operation_name](_soapheaders=self.soap_header, **self.soap_body)
        return result

    def _echo_start(self):
        self.logger.info(
            f'Crawling {self.source_name} from SOAP Web service: {self.wsdl}.'
        )
