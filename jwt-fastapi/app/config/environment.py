import os

from dotenv import load_dotenv

load_dotenv()


class Environment:
    def __init__(self):
        self.JWT_SECRET = os.environ["JWT_SECRET"]
        self.ALGORITHM = os.environ.get("ALGORITHM", "HS256")
        self.EXPIRE_MINUTES = int(os.environ.get("EXPIRE_MINUTES", "30"))


env = Environment()
