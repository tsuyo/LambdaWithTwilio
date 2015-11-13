import re
import config
from datetime import datetime
from urllib2 import urlopen
from twilio.rest import TwilioRestClient

def validateStatus(site):
    '''Return False to trigger the canary'''
    return urlopen(site).getcode() == 200

def validateString(site):
    p = re.compile(config.CHECK_STR)
    return p.match(urlopen(site).read())

def lambda_handler(event, context):
    print('Checking {} at {}...'.format(config.SITE, event['time']))
    try:
        if not validateString(config.SITE):
            raise Exception('Validation failed')
    except:
        print('Check failed!')
        make_call()
        raise
    else:
        print('Check passed!')
        return event['time']
    finally:
        print('Check complete at {}'.format(str(datetime.now())))

def make_call():
    client = TwilioRestClient(config.ACCOUNT_SID, config.AUTH_TOKEN)

    call = client.calls.create(
        to=config.PHONE_TO,
        from_=config.PHONE_FROM,
        url=config.CALL_URL,
        method="GET",
        fallback_method="GET",
        status_callback_method="GET",
        record="false"
    )
    return call.sid
