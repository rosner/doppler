# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2012 Retresco GmbH
# Copyright (c) 2011 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
"""
A collection of sample response mappers.
"""
import re

from lxml.html import document_fromstring as parse_html
from lxml.etree import tostring

def map_to_docs(solr_response):
    """
    Response mapper that only returns the list of result documents.
    """
    return solr_response['response']['docs']

def map_error_response(solr_response):
    if 'response' in solr_response and solr_response['response'].code >= 400:
        real_response = solr_response['response']

        document = parse_html(real_response.body)
        title = tostring(document.xpath('//title').pop(), method='text')
        reason = title.strip()
        body_element = document.xpath('//body').pop()
        raw_body = tostring(body_element, method='text').strip()
        original_message = re.sub(r'(\s+)|(Powered.*$)', ' ', raw_body).strip()
        return {'reason':reason, 'original_message': original_message,
                'response': real_response}

    else:
        return solr_response
