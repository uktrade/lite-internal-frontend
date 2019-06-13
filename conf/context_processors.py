import os


def export_vars(request):
    return {'ENVIRONMENT_VARIABLES': dict(os.environ.items())}


def lite_menu(request):
    return {
		'LITE_MENU': [
			{
				'title': 'Cases',
				'url': '/cases/',
				'icon': 'menu/cases'
			},
			{
				'title': 'Organisations',
				'url': '/organisations/',
				'icon': 'menu/businesses'
			},
			{
				'title': 'Teams',
				'url': '/teams/',
				'icon': 'menu/teams'
			},
			{
				'title': 'Queues',
				'url': '/queues/',
				'icon': 'menu/teams'
			}
		]
	}
