import json


class PostCache:
    CACHE_CONTENTS = 'cache.json'

    def __init__(self):
        try:
            with open(PostCache.CACHE_CONTENTS) as json_file:
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
        with open(PostCache.CACHE_CONTENTS, 'w') as outfile:
            output = json.dump(self.cache, outfile)
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
