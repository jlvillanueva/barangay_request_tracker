
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
print("DIGEST_SALT after load_dotenv:", os.environ.get("DIGEST_SALT"))
from common import *
import mobile

if __name__ == "__main__":
  app.run(threaded=True,debug=True,host='0.0.0.0', port=5001)