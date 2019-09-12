import json
import time

import requests
from conf.settings import env


class SeedData:
    base_url = ''
    gov_user_email = env('TEST_SSO_EMAIL')
    exporter_user_email = env('TEST_EXPORTER_SSO_EMAIL')
    gov_user_first_name = env('TEST_SSO_NAME').split(' ')[0]
    gov_user_last_name = env('TEST_SSO_NAME').split(' ')[1]

    gov_user_request_data = {
        "email": gov_user_email,
        "first_name": gov_user_first_name,
        "last_name": gov_user_last_name}
    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}
    context = {}
    logging = True
    org_name = "Test Org"

    request_data = {
        "organisation": {
            "name": org_name,
            "eori_number": "1234567890AAA",
            "sic_number": "2345",
            "vat_number": "GB1234567",
            "registration_number": "09876543",
            "user": {
                "first_name": "Trinity",
                "last_name": "Fishburne",
                "email": exporter_user_email,
                "password": "password"
            },
            "site": {
                "name": "Headquarters",
                "address": {
                    "address_line_1": "42 Question Road",
                    "postcode": "Islington", "city": "London",
                    "region": "London",
                    "country": "GB"
                }
            }
        },
        "good": {
            "description": "MPG 2.",
            "is_good_controlled": "yes",
            "control_code": "1234",
            "is_good_end_product": True,
            "part_number": "1234",
            "validate_only": False
        },
        "ecju_query_picklist": {
            "name": "Standard question 1",
            "text": "Why did the chicken cross the road?",
            "type": "ecju_query"
        },
        "proviso_picklist": {
            "name": "Misc",
            "text": "My proviso advice would be this.",
            "proviso": "My proviso would be this.",
            "type": "proviso"
        },
        "standard_advice_picklist": {
            "name": "More advice",
            "text": "My standard advice would be this.",
            "type": "standard_advice"
        },
        "gov_user": {
            "email": gov_user_email,
            "first_name": gov_user_first_name,
            "last_name": gov_user_last_name},
        "export_user": {
            "email": exporter_user_email,
            "password": "password"
        },
        "draft": {
            "name": "application",
            "licence_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"
        },
        "end-user": {
            "name": "Government",
            "address": "Westminster, London SW1A 0AA",
            "country": "Ukraine",
            "type": "government",
            "website": "https://www.gov.uk"
        },
        "ultimate_end_user": {
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "type": "commercial",
            "website": "https://www.anothergov.uk"
        },
        "add_good": {
            "good_id": "",
            "quantity": 1234,
            "unit": "NAR",
            "value": 123.45
        },
        "clc_good": {
            "description": "Targus",
            "is_good_controlled": "unsure",
            "is_good_end_product": True,
            "part_number": "1234",
            "validate_only": False,
        },
        "document": {
            'name': 'document 1',
            's3_key': env('TEST_S3_KEY'),
            'size': 0,
            'description': 'document for test setup'
        }
    }

    def __init__(self, api_url, logging=True):
        self.base_url = api_url.rstrip('/')
        self.auth_gov_user()
        self.setup_org()
        self.auth_export_user()
        self.add_good()
        self.logging = logging

    def log(self, text):
        if self.logging:
            print(text)

    def add_to_context(self, name, value):
        self.log(name + ": " + value)
        self.context[name] = value

    def auth_gov_user(self):
        data = self.request_data['gov_user']
        response = self.make_request("POST", url='/gov-users/authenticate/', body=data)
        self.add_to_context('gov_user_token', json.loads(response.text)['token'])
        self.gov_headers['gov-user-token'] = self.context['gov_user_token']

    def auth_export_user(self):
        data = self.request_data['export_user']
        response = self.make_request("POST", url='/users/authenticate/', body=data)
        self.add_to_context('export_user_token', json.loads(response.text)['token'])
        self.export_headers['exporter-user-token'] = self.context['export_user_token']
        self.export_headers['organisation-id'] = self.context['org_id']

    def setup_org(self):
        organisation = self.find_org_by_name()
        if not organisation:
            organisation = self.add_org()
        org_id = organisation['id']
        self.add_to_context('org_id', org_id)
        self.add_to_context('org_name', self.org_name)
        self.add_to_context('first_name', self.gov_user_first_name)
        self.add_to_context('last_name', self.gov_user_last_name)
        self.add_to_context('primary_site_id', self.get_org_primary_site_id(org_id))

    def add_org(self):
        self.log("Creating org: ...")
        data = self.request_data['organisation']
        response = self.make_request("POST", url='/organisations/', body=data)
        organisation = json.loads(response.text)['organisation']
        return organisation

    def add_ecju_query_picklist(self):
        self.log("Creating ECJU Query picklist item ...")
        data = self.request_data['ecju_query_picklist']
        response = self.make_request("POST", url='/picklist/', body=data)
        return json.loads(response.text)['picklist_item']

    def add_proviso_picklist(self):
        self.log("Creating proviso picklist item ...")
        data = self.request_data['proviso_picklist']
        response = self.make_request("POST", url='/picklist/', body=data)
        return json.loads(response.text)['picklist_item']

    def add_standard_advice_picklist(self):
        self.log("Creating standard advice picklist item ...")
        data = self.request_data['standard_advice_picklist']
        response = self.make_request("POST", url='/picklist/', body=data)
        return json.loads(response.text)['picklist_item']

    def find_org_by_name(self):
        response = self.make_request("GET", url='/organisations/')
        organisations = json.loads(response.text)['organisations']
        organisation = next((item for item in organisations if item["name"] == self.org_name), None)
        return organisation

    def get_org_primary_site_id(self, org_id):
        response = self.make_request("GET", url='/organisations/' + org_id)
        organisation = json.loads(response.text)['organisation']
        return organisation['primary_site']['id']

    def add_good(self):
        self.log("Adding good: ...")
        data = self.request_data['good']
        response = self.make_request("POST", url='/goods/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['good']
        self.add_to_context('good_id', item['id'])
        self.add_good_document(item['id'])

    def add_clc_query(self):
        self.log("Adding clc query: ...")
        data = self.request_data['clc_good']
        response = self.make_request("POST", url='/goods/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['good']
        self.add_good_document(item['id'])
        data = {
            'not_sure_details_details': 'something',
            'not_sure_details_control_code': 'ML17',
            'good_id': item['id']
        }
        response = self.make_request("POST", url='/queries/control-list-classifications/', headers=self.export_headers, body=data)
        self.add_to_context('case_id', json.loads(response.text)['case_id'])

    def add_good_document(self, good_id):
        data = [self.request_data['document']]
        self.make_request("POST", url='/goods/' + good_id + '/documents/', headers=self.export_headers, body=data)

    def add_end_user_document(self, draft_id):
        data = self.request_data['document']
        self.make_request("POST", url='/drafts/' + draft_id + '/end-user/document/', headers=self.export_headers,
                          body=data)

    def add_ultimate_end_user_document(self, draft_id, ultimate_end_user_id):
        data = self.request_data['document']
        self.make_request("POST", url='/drafts/' + draft_id + '/ultimate-end-user/' + ultimate_end_user_id +
                                      '/document/', headers=self.export_headers, body=data)

    def add_draft(self, draft=None, good=None, enduser=None, ultimate_end_user=None):
        self.log("Creating draft: ...")
        data = self.request_data['draft'] if draft is None else draft
        response = self.make_request("POST", url='/drafts/', headers=self.export_headers, body=data)
        draft_id = json.loads(response.text)['draft']['id']
        self.add_to_context('draft_id', draft_id)
        self.log("Adding site: ...")
        self.make_request("POST", url='/drafts/' + draft_id + '/sites/', headers=self.export_headers,
                          body={'sites': [self.context['primary_site_id']]})
        self.log("Adding end user: ...")
        data = self.request_data['end-user'] if enduser is None else enduser
        self.make_request("POST", url='/drafts/' + draft_id + '/end-user/', headers=self.export_headers,
                          body=data)
        self.log("Adding end user document: ...")
        self.add_end_user_document(draft_id)
        self.log("Adding good: ...")
        data = self.request_data['add_good'] if good is None else good
        data['good_id'] = self.context['good_id']
        self.make_request("POST", url='/drafts/' + draft_id + '/goods/', headers=self.export_headers, body=data)
        self.log("Adding ultimate end user: ...")
        data = self.request_data['ultimate_end_user'] if ultimate_end_user is None else ultimate_end_user
        ultimate_end_user_post = self.make_request('POST', url='/drafts/' + draft_id + '/ultimate-end-users/',
                                                   headers=self.export_headers, body=data)
        ultimate_end_user_id = json.loads(ultimate_end_user_post.text)['end_user']['id']
        self.add_ultimate_end_user_document(draft_id, ultimate_end_user_id)
        return draft_id, ultimate_end_user_id

    def submit_application(self, draft_id=None):
        self.log("submitting application: ...")
        draft_id_to_submit = draft_id if None else self.context['draft_id']
        data = {'id': draft_id_to_submit}
        response = self.make_request("POST", url='/applications/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['application']
        self.add_to_context('application_id', item['id'])
        self.add_to_context('case_id', item['case_id'])

    def check_end_user_document_is_processed(self, draft_id):
        data = self.make_request("GET", url='/drafts/' + draft_id + '/end-user/document/', headers=self.export_headers)
        return json.loads(data.text)['document']['safe']

    def check_ultimate_end_user_document_is_processed(self, draft_id, ultimate_end_user_id):
        data = self.make_request("GET", url='/drafts/' + draft_id + '/ultimate-end-user/'
                                            + ultimate_end_user_id + '/document/', headers=self.export_headers)
        return json.loads(data.text)['document']['safe']

    def add_queue(self, queue_name):
        self.log("adding queue: ...")
        self.context['queue_name'] = queue_name
        data = {'team': '00000000-0000-0000-0000-000000000001',
                'name': queue_name
                }
        response = self.make_request("POST", url='/queues/', headers=self.gov_headers, body=data)
        item = json.loads(response.text)['queue']
        self.add_to_context('queue_id', item['id'])

    def get_queues(self):
        self.log("getting queues: ...")
        response = self.make_request("GET", url='/queues/', headers=self.gov_headers)
        queues = json.loads(response.text)['queues']
        return queues

    def assign_case_to_queue(self, case_id=None, queue_id=None):
        self.log("assigning case to queue: ...")
        queue_id = self.context['queue_id'] if queue_id is None else queue_id
        case_id = self.context['case_id'] if case_id is None else case_id
        data = {'queues':  [queue_id]}
        self.make_request("PUT", url='/cases/' + case_id + '/', headers=self.gov_headers, body=data)

    def assign_test_cases_to_bin(self, bin_queue_id, new_cases_queue_id):
        self.log("assigning cases to bin: ...")
        response = self.make_request("GET", url='/queues/' + new_cases_queue_id + '/', headers=self.gov_headers)
        queue = json.loads(response.text)['queue']
        cases = queue['cases']
        for case in cases:
            data = {'queues':  [bin_queue_id]}
            self.make_request("PUT", url='/cases/' + case['id'] + '/', headers=self.gov_headers, body=data)

    def make_request(self, method, url, headers=None, body=None):
        if headers is None:
            headers = self.gov_headers
        if body:
            response = requests.request(method, self.base_url + url,
                                        data=json.dumps(body),
                                        headers=headers)
        else:
            response = requests.request(method, self.base_url + url, headers=headers)
        if not response.ok:
            raise Exception("bad response: " + response.text)
        return response
