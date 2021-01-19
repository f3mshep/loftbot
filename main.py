#!/usr/bin/python3

from craigslist import CraigslistHousing
from service.EmailService import EmailService
from service.PostCache import PostCache
import datetime

#todo this is garbage and should be moved to another level
negative_filter = ['lampwork lofts', 'macarthur commons', 'bakery lofts', 'the boise']

if __name__ == '__main__':
    timestamp = datetime.datetime.now()
    print(timestamp) 
    cl_h = CraigslistHousing(site='sfbay', area='eby', category='apa',
                             filters={'max_price': 2500, 'private_room': True, 'query': 'loft',
                                      'search_distance': 10, 'zip_code': 94612
                                      })
    results = cl_h.get_results(sort_by='newest', geotagged=True, include_details=True)
    cache = PostCache()
    email_service = EmailService()

    should_send_emails = not cache.is_cache_empty()
    for result in results:
        if result['body']:
            downcase_body = result['body'].lower()
            if not any(x in downcase_body for x in negative_filter):
                if not cache.peek(result['id']):
                    cache.handle_post(result)
                    if should_send_emails:
                        email_service.send_email(result)

    cache.dump_cache()
