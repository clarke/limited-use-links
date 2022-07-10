import os

# Statement for enabling the development environment
DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                    'sqlite:///db/database.db')
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Secret key for signing cookies
SECRET_KEY = "Qr)E[Y>9Yqn~8mTr{LuUD[LqZ@!4+d"

# The location to store uploaded files
UPLOAD_FILE_DIRECTORY = os.path.join(os.getcwd(), 'sharable', 'files')

# The base URL for shared files in UPLOAD_FILE_DIRECTORY.
# This URL should be exposed with nginx or another tool
# better suited to serve static files. It is not exposed
# by this application.
SHARED_FILES_BASE_URL = "http://localhost:8000/s"