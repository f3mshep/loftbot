#!/usr/bin/python3

from craigslist import CraigslistHousing
from service.EmailService import EmailService
from service.PostCache import PostCache
import datetime

#todo this is garbage and should be moved to another level
negative_filter = ['studio']

zippies = [97211,97218,97212,97213,97232,97214,97215,97202,97206]

site = 'portland',
area = 'mlt',
category = 'apa'

filters = {
    'max_price': 1300,
    'private_room': True,
    'search_distance': 5,
}


if __name__ == '__main__':
    timestamp = datetime.datetime.now()
    print("-----------")
    print(timestamp) 
    print("-----------")

    cache = PostCache()
    email_service = EmailService()

    for zip in zippies:
        print("Searching zipcode: ", str(zip))
        cl_h = CraigslistHousing('portland', area, category,
                             filters={
                                'max_price': filters.get('max_price'), 
                                'private_room': filters.get('private_room'),
                                'search_distance': 1, 'zip_code': zip
                                }
                                )
        results = cl_h.get_results(sort_by='newest', geotagged=True, include_details=True)


        should_send_emails = not cache.is_cache_empty()
        for result in results:
            if result['body']:
                downcase_body = result['body'].lower()
                if not any(x in downcase_body for x in negative_filter):
                    if not cache.peek(result['id']):
                        cache.handle_post(result)
                        if should_send_emails:
                            email_service.send_email(result)
        print("Finished zipcode: ", str(zip))

    cache.dump_cache()
    print("-----------")
    print("Finished job..") 
    print("-----------")
