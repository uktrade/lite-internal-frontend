ISO8601_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
DEFAULT_QUEUE_ID = '00000000-0000-0000-0000-000000000001'

# URLS
ORGANISATIONS_URL = '/organisations/'
CASE_URL = '/cases/'
APPLICATIONS_URL = '/applications/'
CASE_NOTES_URL = '/case_notes/'
CASE_FLAGS_URL = '/flags/'
ACTIVITY_URL = '/activity/'
CASE_DENIAL_REASONS_URL = '/denial_reasons/'
SITES_URL = '/sites/'
TEAMS_URL = '/teams/'
QUEUES_URL = '/queues/'
AUTHENTICATION_URL = '/gov-users/authenticate/'
GOV_USERS_URL = '/gov-users/'
GOV_USERS_ROLES_URL = '/gov-users/roles/'
GOV_USERS_PERMISSIONS_URL = '/gov-users/permissions/'
FLAGS_URL = '/flags/'
FLAGS_CASE_LEVEL_FOR_TEAM = '/flags/?level=Case&team=True'
CLC_QUERIES_URL = '/clc_queries/'

# Static URLs
STATIC_URL = '/static/'
DENIAL_REASONS_URL = STATIC_URL + 'denial-reasons/'
COUNTRIES_URL = STATIC_URL + 'countries/'

# Permissions
MAKE_FINAL_DECISIONS = 'MAKE_FINAL_DECISIONS'
