import os

from dotenv import load_dotenv

load_dotenv()

def get_env_vars(name,default=None):
    """
    Makes accessing the environment variables easy. Returns a default value if not found any.
    """
    return os.environ.get(name,default=default)