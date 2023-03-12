import json
import os

CACHE_FULL_PATH = os.environ.get('CACHE_FULL_PATH')
DEFAULT_PATH = "cache.json"


class PostCache:

    def __init__(self):
        self.path = CACHE_FULL_PATH if CACHE_FULL_PATH is not None else DEFAULT_PATH
        try:
            with open(self.path) as json_file:
                if json_file:
                    data = json.load(json_file, strict=False)
                    if data:
                        self.cache = data
                    else:
                        self.cache = {}
                else:
                    self.cache = {}
        except:
            self.cache = {}

    def handle_post(self, post, timestamp):
        if not self.peek(post['id']):
            self.handle_miss(post, timestamp)

    def dump_cache(self):
        with open(self.path, 'w') as outfile:
            json.dump(self.cache, outfile)
        return True

    def add_to_cache(self, post, timestamp):
        self.cache[post['id']] = str(timestamp)
        return True

    def peek(self, post_id):
        exists = post_id in self.cache.keys()
        if exists:
            print(post_id + " exists in cache")
        return exists

    def get_post(self, post_id):
        return self.cache[post_id]

    def handle_miss(self, post, timestamp):
        print("adding new post to cache..")
        print(post)
        self.add_to_cache(post, timestamp)

    def is_cache_empty(self):
        return len(self.cache.keys()) < 1
