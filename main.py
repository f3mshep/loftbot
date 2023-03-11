#!/usr/bin/python3
from datetime import datetime

from craigslist_headless import CraigslistHousing
from service.EmailService import EmailService
from service.PostCache import PostCache

negative_filter = ['studio']

if __name__ == '__main__':
    timestamp = datetime.now()
    print("-----------")
    print(str(timestamp) + " started!")
    print("-----------")

    cl_h = CraigslistHousing(site='portland', area='mlt', category='apa',
                             filters={'max_price': 1400, 'private_room': True,
                                      'search_distance': 3, 'zip_code': 97211, 'dogs_ok': True, 'query': 'yard'
                                      })
    results = cl_h.get_results(sort_by='newest', geotagged=True, include_details=True)
    cache = PostCache()
    email_service = EmailService()

    should_send_emails = True
    for result in results:
        if result is not None and 'body' in result:
            downcase_body = result['body'].lower()
            if not any(x in downcase_body for x in negative_filter):
                if not cache.peek(result['id']):
                    cache.handle_post(result, timestamp)
                    if should_send_emails:
                        email_service.send_email(result)

    timestamp_finished = datetime.now()
    print("-----------")
    print(str(timestamp_finished) + " complete!")
    print("-----------")
    cache.dump_cache()
