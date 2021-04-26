from PIL import Image, ImageChops
import numpy as np
import matplotlib.pyplot as plt

# this doesnt work
# img1 = Image.open('code.png')
# img2 = Image.open('frame.png')

# a = np.array(img1)
# b = np.array(img2)

# c = np.bitwise_xor(a, b)
# plt.imsave('res.png', c.astype(np.uint8))

#
img1 = Image.open('code.png').convert(mode='1')
img2 = Image.open('frame.png').convert(mode='1')

out = ImageChops.logical_xor(img1, img2)
out.save('out.png')
