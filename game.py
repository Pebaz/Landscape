from raylib.static import *


class Game:
	def __init__(self, title):
		self.title = title

	def __init(self):
		#SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT)
		InitWindow(1680, 1050, self.title.encode('utf-8'))
		HideCursor()
		InitAudioDevice()
		SetTargetFPS(200)

	def init(self):
		pass

	def update(self):
		pass

	def render2D(self):
		pass

	def __shutdown(self):
		CloseAudioDevice()
		CloseWindow()

	def shutdown(self):
		pass

	def start(self):
		self.__init()
		self.init()

		while not WindowShouldClose():
			self.update()
			BeginDrawing()
			ClearBackground(RAYWHITE)
			self.render2D()
			EndDrawing()
		
		self.shutdown()
		self.__shutdown()
