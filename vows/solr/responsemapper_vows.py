import os
from cStringIO import StringIO

from pyvows import Vows, expect

from tornado.httpclient import HTTPRequest, HTTPResponse
from doppler.solr.responsemapper import map_error_response

def response_for_code(status_code):
    current_path = os.path.dirname(__file__)
    html_file_path = os.path.abspath(
            os.path.join(current_path, 'solr_%s.html' % status_code))
    with open(html_file_path) as html_file:
        buffer = StringIO(html_file.read()) 
        request = HTTPRequest('//http://foo.bar')
        return HTTPResponse(request, status_code, buffer=buffer)

fixtures = {
    '400': [ 'unknown field \'date_checked\'', 
        'HTTP ERROR 400'\
        + ' Problem accessing /solr/dev/update/json. Reason: '\
        + 'ERROR: [doc=null] unknown field \'date_checked\'' ],
    '404': [ 'Error 404 NOT_FOUND', 
        'HTTP ERROR 404'\
        + ' Problem accessing /solr/dev/update/json. Reason: NOT_FOUND' ]
 }

@Vows.batch
class SolrErrorResponse(Vows.Context):
    
    class Solr400ErrorResponse(Vows.Context):
        def topic(self):
            solr_response = response_for_code(400)
            topic =  map_error_response(solr_response) 
            fixture = fixtures['400']
            fixture.append(topic)
            return fixture

        def hasCorrectResponseFormat(self, topic):
            _, _, actual = topic
            expect(actual).to_be_instance_of(dict)

        def hasReason(self, topic):
            reason, _, actual = topic
            expect(actual['reason']).to_equal(reason)

        def hasOriginalMessage(self, topic):
            _, original_message, actual = topic
            expect(actual['original_message']).to_equal(original_message)
        
    class Solr404ErrorResponse(Solr400ErrorResponse):

        def topic(self):
            solr_response = response_for_code(404)
            topic =  map_error_response(solr_response) 
            fixture = fixtures['404']
            fixture.append(topic)
            return fixture
