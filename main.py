from bloxel.iso import Cornerstone, IsoCoors
"""
corn = Cornerstone.get(color=(157, 214, 59, 255))
corn.save('Bloxel-Green.png')
"""

from time import time
from random import randint
from raylib.static import *
from game import Game

ctm = lambda: int(round(time() * 1000))


class Landscape(Game):
	def __init__(self):
		Game.__init__(self, 'Landscape Generator')

	def init(self):
		ShowCursor()
		self.image = LoadTexture(b'Bloxel-White.png')
		self.coors = IsoCoors(4)
		self.off_x = 0
		self.off_y = 0
		self.plane_x = 70
		self.plane_y = 70
		self.plane_z = 50
		self.auto = True

		coor1 = self.coors.get(0, 0, 0)
		coor2 = self.coors.get(self.plane_x, self.plane_y, 0)
		self.horizontal_w = (coor2[0] - coor1[0]) // 2
		self.vertical_h = (coor2[1] - coor1[1]) // 2

		self.last_time = ctm()
		self.fps = 1
		self.display_fps = 1
		self.draw_noise_texture = False

	def render2D(self):
		noise_image = GenImagePerlinNoise(self.plane_x, self.plane_y, self.off_x, self.off_y, 1)
		#noise_texture = LoadTextureFromImage(noise_image)
		noise_data = GetImageData(noise_image)
		for y in range(noise_image.height):
			for x in range(noise_image.width):
				zd = noise_data[y * noise_image.width + x].r / 255.0
				clr_zd = int(zd * 255)

				if self.draw_noise_texture:
					ground_coors = self.coors.get(x, y, 0)
					clr = [clr_zd, clr_zd, clr_zd, 255]
					DrawTexture(
						self.image,
						(ground_coors[0] + GetScreenWidth() // 2) - self.horizontal_w,
						(ground_coors[1] + GetScreenHeight() // 2) - self.vertical_h,
						clr
					)

				coors = self.coors.get(x, y, zd * self.plane_z)
				clr = [157, 214, 59, clr_zd]
				clr = [255, clr_zd, 255, clr_zd]
				DrawTexture(
					self.image,
					(coors[0] + GetScreenWidth() // 2) - self.horizontal_w,
					(coors[1] + GetScreenHeight() // 2) - self.vertical_h,
					clr
				)

		self.fps += 1

		DrawText(f'FPS: {self.display_fps}'.encode('utf-8'), 8, 10, 20, [255, 0, 255, 255])
		DrawText(b'Generate a new map with SPACE',           8, 35, 20, [255, 0, 255, 255])
		DrawText(b'Toggle auto-move with ENTER',             8, 60, 20, [255, 0, 255, 255])
		DrawText(b'Use WASD keys to move around',            8, 85, 20, [255, 0, 255, 255])
		DrawText(b'Show Noise Texture with BACKSPACE',       8, 110, 20, [255, 0, 255, 255])

		if ctm() > self.last_time + 1000:
			self.display_fps = self.fps
			self.last_time = ctm()
			self.fps = 1

	def update(self):
		if IsKeyReleased(KEY_SPACE):
			self.off_x = randint(0, 1000)
			self.off_y = randint(0, 1000)

		if IsKeyReleased(KEY_ENTER):
			self.auto = not self.auto

		if IsKeyReleased(KEY_BACKSPACE):
			self.draw_noise_texture = not self.draw_noise_texture

		if IsKeyDown(KEY_D):
			self.off_x += 1
		if IsKeyDown(KEY_A):
			self.off_x -= 1
		if IsKeyDown(KEY_W):
			self.off_y += 1
		if IsKeyDown(KEY_S):
			self.off_y -= 1

		if self.auto:
			self.off_x += 1

if __name__ == '__main__':
	game = Landscape()
	game.start()

