""" Graphics for the Ecosystem project developed by Lea Wittie
	with help from Matt Rogge. """
from graphics import *

class River:
	def __init__(self, ecosystem, screen):

		""" BBBBBBFFFNNNNBN
						  F
			BBBBBBFFFNNNNBN
			N
			FFFFBBNNNNF """
		self.length = ecosystem.get_size()	# number of items to show
		offset = 100	  # offset from left side, right side, and top
		img_size = 100 # width of images

		# full window
		maxcol = screen
		rows = self.length//maxcol # a row is 15 images across and 1 down so the
		# river looks like a snake
		width = offset + maxcol*img_size + offset
		height = offset + rows*2*img_size + offset + offset
		self.window = GraphWin("River Ecosystem", width, height)
		self.window.setBackground('aqua')

		# Quit Button
		self.quit = Button(Point(width/2, height - offset), "Quit")
		self.quit.draw(self.window)

		# the river items
		self.images = []
		row = 0
		col = 0
		x = offset
		y = offset
		bend = False
		for index in range(self.length):
			img = Image(Point(x,y), img_size,img_size)

			if not bend and row%2==0:
				col += 1
			elif not bend and row%2==1:
				col -= 1


			if not bend and col > maxcol:
				col -= 1
				bend = True
				y += img_size
			elif not bend and col == -1:
				col = 0
				bend = True
				y += img_size
			elif bend:
				row += 1
				bend = False
				y += img_size
				x += img_size

			if col == 0:
				x = offset

			elif not bend and row%2==0:
				x += img_size
			elif not bend and row%2==1:
				x -= img_size

			img.draw(self.window)
			self.images.append(img)

		# the ecosystem implemented by the students
		self.ecosystem = ecosystem

	def update_gui(self):
		""" Update the gui to match the ecosystem. """

		for index in range(self.length):
			# Get river inhabitant (Bear,Fish,None) and image
			try:
				inhabitant = self.ecosystem.get_inhabitant(index)
			except:
				print("River was too short. Did not find index " + str(index) + ". Using water.")
				inhabitant = None

			if inhabitant == None:
				img = "water.ppm"
			else:
				try:
					img = inhabitant.get_image()

				except:
					print("inhabitant in index " +str(index) + " did not have an image. Using whirlpool.")
					img = "whirlpool.ppm"

			# Put image in the river
			try:
				self.images[index].set_image(img)
			except Exception:
				print("Bad image: " + img + ". Using whirlpool.")
				self.images[index].set_image("whirlpool.ppm")

			self.images[index].undraw()
			self.images[index].draw(self.window)

	def run(self):
		""" Get and process a mouse click. Repeat till quit is pressed. """
		# redraw
		self.update_gui()

		# wait for clicks
		pt = self.window.getMouse()

		# Click quit: close window
		if self.quit.contains(self.window, pt):
			self.ecosystem.quit()
			self.window.close()

		# Click elsewhere: step thru time
		else:
			self.ecosystem.step()
			self.run()




