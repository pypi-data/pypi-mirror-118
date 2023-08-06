from PIL import Image
from mapfost import mapfost as mf

im1 = Image.open("test_im1.tif")
im2 = Image.open("test_im2.tif")

res = mf.est_aberr([im1, im2])
print(res)
