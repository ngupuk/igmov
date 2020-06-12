# Get random image

# %%
import urllib3
http = urllib3.PoolManager()

# %%
resultPath = "../sample/result.jpg"
baseUrl = "https://source.unsplash.com/featured/?"
query = "nature"
result = http.request('GET', baseUrl + query).data
with open(resultPath, 'wb') as photos:
    photos.write(result)

from IPython.display import Image
Image(filename=resultPath)