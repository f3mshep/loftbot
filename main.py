#!/usr/bin/python3
import logging
from datetime import datetime

from craigslist_headless import CraigslistHousing

from service.EmailService import EmailService
from service.PostCache import PostCache

negative_filter = ['studio']
LOG_NAME = "loftbot.log"

if __name__ == '__main__':

    logging.basicConfig(filename=LOG_NAME,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    logging.info("Running Urban Planning")

    timestamp = datetime.now()
    logging.info("-----------")
    logging.info(str(timestamp) + " started!")
    logging.info("-----------")

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
    logging.info("-----------")
    logging.info(str(timestamp_finished) + " complete!")
    logging.info("-----------")
    cache.dump_cache()
    cl_h.quit()
