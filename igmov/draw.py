
# def line(img, )

def spectrum(img, data, x, y, color=[255, 255, 255],
                spacing=2, max_length=None, factor=1, 
                direction= 'top'
                ):
  import numpy as np
  from skimage.draw import line

  img = np.array(img).copy()
  for i, l in enumerate(data):
    l = l * factor
    if (max_length != None):
      tall = int(l) if int(l) < max_length else max_length
    else:
      tall = int(l)

    if (direction == 'bottom'):
      c0 = y
      c1 = y + tall
    elif (direction == 'dual'):
      c0 = y - tall
      c1 = y + tall
    else:
      c0 = y - tall
      c1 = y

    r0 = x + i * spacing
    r1 = r0
    xx, yy = line(c0, r0, c1, r1)
    img[xx, yy] = color
  return img