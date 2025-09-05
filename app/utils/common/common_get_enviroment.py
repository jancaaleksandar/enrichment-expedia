import os


def get_environment():
    """Get environment variable that works in both local and Lambda environments"""
    # First try direct environment variable (works in Lambda)
    env = os.environ.get("ENVIRONMENT")

    # If not found and we're in local environment, try load_dotenv
    if env is None:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            env = os.getenv("ENVIRONMENT")
        except ImportError:
            # If dotenv isn't available, that's okay in Lambda
            pass

    return env
