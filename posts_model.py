import json

PAGE_SIZE = 5

class Post:
    db = {}
    
    def __init__(self, id_=None, title=None, body=None, created=None):
        self.id = id_
        self.title = title
        self.body = body
        self.created = created
        self.errors = {}

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def update(self, title, body):
        self.title = title
        self.body = body

    def validate(self):
        if not self.title:
            self.errors['title'] = "Title Required"
        if not self.body:
            self.errors['body'] = "Body Required"
        existing_post = next(filter(lambda p: p.id != self.id and p.title == self.title, Post.db.values()), None)
        if existing_post:
            self.errors['title'] = "Title Must Be Unique"
        return len(self.errors) == 0

    def save(self):
        if not self.validate():
            return False
        if self.id is None:
            if len(Post.db) == 0:
                max_id == 1
            else:
                max_id = max(post.id for post in Post.db.values())
            self.id = max_id + 1
            Post.db[self.id] = self
        Post.save_db()
        return True

    def delete(self):
        del Post.db[self.id]
        Post.save_db()

    @classmethod
    def all(cls, page=1):
        page = int(page)
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        return list(cls.db.values())[start:end]

    @classmethod
    def search(cls, text):
        result = []
        for p in cls.db.values():
            match_title = p.title is not None and text in p.title
            match_created = p.created is not None and text in p.created
            if match_title or match_created:
                result.append(p)

        return result

    @classmethod
    def load_db(cls):
        with open('posts.json', 'r') as posts_file:
            posts = json.load(posts_file)
            cls.db.clear()
            for p in posts:
                cls.db[p['id']] = Post(p['id'], p['title'], p['body'], p['created'])

    @staticmethod
    def save_db():
        out_arr = [p.__dict__ for p in Post.db.values()]
        with open("posts.json", "w") as f:
            json.dump(out_arr, f, indent=2)

    @classmethod
    def find(cls, id_):
        id_ = int(id_)
        p = cls.db.get(id_)
        if p is not None:
            p.errors = {}

        return p
