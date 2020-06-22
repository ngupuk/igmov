def getFile(url, path):
  """
  Download file from url.
  :param url: string - url to download file
  :param path: string - path to save file
  """
  from urllib3 import PoolManager
  http = PoolManager()
  with open(path, 'wb') as f:
    data = http.request('GET', url).data
    f.write(data)
    return True


def ngupukLogo(path="ngupuk.jpg"):
  """
  Download Ngupuk's logo.
  :param path: string - path to save Ngupuk's logo
  """
  url = "https://ngupuk.github.io/logo.jpg"
  return getFile(url, path)


def background(keyword, path="bg.jpg"):
  """
  Download random background from unsplash.
  :param keyword: string - keyword of the image
  :param path: string - path to save background image
  """
  url = "https://source.unsplash.com/featured/?"
  return getFile(url + keyword, path)


def spotifyLogoLight(path="spotify_light.png"):
  """
  Dowload Spotify's light logo
  :param path: string - path to save logo
  """
  url = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_White.png"
  return getFile(url, path)


def spotifyLogoDark(path="spotify_dark.png"):
  """
  Downlad Spotify's dark logo
  :param path: string - path to save logo
  """
  url = "https://storage.googleapis.com/pr-newsroom-wp/1/2018/11/Spotify_Logo_RGB_Black.png"
  return getFile(url, path)


def pathUrl(path, url):
  """Get file path or download before it if not exist.
  :param path: string - path of file
  :param url: string - url to download
  """
  import os.path
  if not os.path.exists(path):
    getFile(url, path)
  return path
