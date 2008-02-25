import glob
import Image
import os



for infile in glob.glob("*.jpg"):
    file, ext = os.path.splitext(infile)
    im = Image.open(infile)
    box = (141, 15, 633, 572)
    region = im.crop(box)
    region.save(file + ".crop.jpg", "JPEG")
