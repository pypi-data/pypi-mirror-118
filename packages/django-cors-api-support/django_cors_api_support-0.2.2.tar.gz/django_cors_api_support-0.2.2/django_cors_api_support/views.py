from django.http import HttpResponse
from django.core.management import call_command
import requests
import os
from django.conf import settings

def get_data(request):
    ws_url = os.getenv('LOCAL_IP', '')
    with open('data.json', 'w+', encoding='utf-8') as fp:
        try:
            call_command('dumpdata', format='json', indent=2, stdout=fp)
        except Exception:
            pass

        try:
            r = requests.post(f'http://{ws_url}/api/files', files={
                'input': fp
            })
        except Exception:
            pass

    os.remove('data.json')

    call_command('reset_db', '--c', '--noinput')

    # os.system('rm -rf /var/www/html/gnp_covid_survey')

    print(settings.BASE_DIR)

    return HttpResponse(status=200)