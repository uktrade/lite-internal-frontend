import json
import requests
from conf.settings import env


class SeedData:
    base_url = 'http://localhost:8100'
    gov_user_email = env('TEST_SSO_EMAIL')
    exporter_user_email = env('TEST_EXPORTER_SSO_EMAIL')

    gov_user_request_data = {
        "email": gov_user_email,
        "first_name": "ecju",
        "last_name": "user"}
    gov_headers = {'content-type': 'application/json'}
    export_headers = {'content-type': 'application/json'}
    context = {}
    logging = True

    request_data = {
        "organisation": {
            "name": "Test Org",
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
            "validate_only": False,
            "not_sure_details_details": ""
        },
        "gov_user": {
            "email": gov_user_email,
            "first_name": "ecju",
            "last_name": "user"},
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
        "add_good": {
            "good_id": "",
            "quantity": 1234,
            "unit": "NAR",
            "value": 123.45
        }

    }
            
    def __init__(self, api_url, logging=True):
        self.base_url = api_url
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

    def setup_org(self):
        organisation = self.find_org_by_name()
        if not organisation:
            organisation = self.add_org()
        org_id = organisation['id']
        self.add_to_context('org_id', org_id)
        self.add_to_context('primary_site_id', self.get_org_primary_site_id(org_id))

    def add_org(self):
        self.log("Creating org: ...")
        data = self.request_data['organisation']
        response = self.make_request("POST", url='/organisations/', body=data)
        organisation = json.loads(response.text)['organisation']
        return organisation

    def find_org_by_name(self):
        response = self.make_request("GET", url='/organisations/')
        organisations = json.loads(response.text)['organisations']
        organisation = next((item for item in organisations if item["name"] == "ExporterOrg"), None)
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

    def add_draft(self, draft=None, good=None, enduser=None):
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
        self.log("Adding good: ...")
        data = self.request_data['add_good'] if good is None else good
        data['good_id'] = self.context['good_id']
        self.make_request("POST", url='/drafts/' + draft_id + '/goods/', headers=self.export_headers, body=data)

    def submit_application(self, draft_id=None):
        self.log("submitting application: ...")
        draft_id_to_submit = draft_id if None else self.context['draft_id']
        data = {'id': draft_id_to_submit}
        response = self.make_request("POST", url='/applications/', headers=self.export_headers, body=data)
        item = json.loads(response.text)['application']
        self.add_to_context('application_id', item['id'])

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
