def getFile(url, path):
  from urllib3 import PoolManager
  http = PoolManager()
  with open(path, 'wb') as f:
    data = http.request('GET', url).data
    f.write(data)
    return True


def ngupukLogo(path="ngupuk.jpg"):
  url = "https://ngupuk.github.io/logo.jpg"
  return getFile(url, path)


def background(keyword, path="bg.jpg"):
  url = "https://source.unsplash.com/featured/?"
  return getFile(url + keyword, path)


def spotifyLogoLight(path="spotify_light.png"):
  url = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png"
  return getFile(url, path)


def spotifyLogoDark(path="spotify_dark.png"):
  url = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Black.png"
  return getFile(url, path)
