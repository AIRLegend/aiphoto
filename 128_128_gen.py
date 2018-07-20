#!/bin/python3
from PIL import Image, ImageFilter, ImageChops

import numpy as np
import os

PATH_GOOD = "data/good/"
PATH_BAD = "data/bad/"

SIZE_INPUT = 128

'''
	Anhadir ruido gaussiano a una imagen (tiene que ser RGB)
'''
def addNoise(image, mean=0, var=0.1, alpha=0.3) :
	noiseArr = np.random.normal(mean, var**0.5,(image.size[1],)+(image.size[0],)+(3,))
	noiseIm = Image.fromarray(np.uint8(noiseArr*255))
	return ImageChops.blend(image, noiseIm, alpha)

'''
	filtro -> (size_filter,size_filter) recomendado 3 o 9
'''
def blur(image, size_filter=3):
	return image.filter(ImageFilter.MedianFilter(size_filter))



if __name__ == '__main__':
	good_photos = os.listdir(PATH_GOOD) # Nombres de las fotos

	completed = 0
	total_size = len(good_photos)

	print("Total number of photos = {}".format(total_size))

	for name in good_photos:

		image_good = Image.open(PATH_GOOD+name)
		#Anhadir desenfoque a algunas
		image = image_good.copy()
		if np.random.rand() > 0.75:
			image = blur(image)
		image = addNoise(image)


		#Ir recortando cachos de 100x100 de cada imagen y anadirlos al array
		size_x = image_good.width
		size_y = image_good.height
        
		for i in range(128, size_y, SIZE_INPUT):
			for j in range(128, size_x, SIZE_INPUT):
				crop_good = image_good.crop((j-128, i-128, j, i))
				crop_bad = image.crop((j-128, i-128, j, i))

				crop_good.save("crops_good/{}_{}_{}".format(i,j,name), 'JPEG')
				crop_bad.save("crops_bad/{}_{}_{}".format(i,j,name), 'JPEG')
		completed += 1
		print("completed {} of {}".format(completed, total_size))



