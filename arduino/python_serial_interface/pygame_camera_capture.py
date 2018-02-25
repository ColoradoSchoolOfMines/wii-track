#!/usr/bin/env python3

import os
import pygame, sys
import time

from pygame.locals import *
import pygame.camera

width = 640
height = 480

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0", (width, height))
cam.start()


while True:

	windowSurfaceObj = pygame.display.set_mode((width, height), 1, 16)
	pygame.display.set_caption('Camera')

	image = cam.get_image()

	catSurfaceObj = image
	windowSurfaceObj.blit(catSurfaceObj, (0, 0))
	pygame.display.update()
	# time.sleep(.1)

