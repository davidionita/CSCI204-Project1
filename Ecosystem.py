# Matt Compton & David Ionita

from random import *
import os,sys,shutil

from PIL import Image, ImageDraw

class Ecosystem:

  # Constructor
  def __init__(self, filename, html_out=False):
    self.html_out = html_out

    self.step_num = 0
    if os.path.exists("output.txt"):
      os.remove("output.txt")

    if os.path.exists(filename):
      with open(filename) as f: 
        river = f.read().split("\n")
        self.river = []
        for obj in river:
          if " " in obj:
            animal, sex, strength = obj.split(" ")
            if animal == "B":
              new = Bear(float(strength), sex)
            elif animal == "F":
              new = Fish(float(strength), sex)
          elif obj == "N" or obj == "":
            new = None
          self.river.append(new)
      self.logRiver()
    else:
      print("File doesn't exist.")
      sys.exit(1)

  def step(self):
    # Moves the whole river one step forward in time.
    # At the end, it should also print the state of the river
    # and save it to a file
    
    self.spawn_fish = 0
    self.spawn_bear = 0

    self.last = False
    self.first = False

    self.skip = False
    self.skip_times = 0
    self.skip_done = 0

    riverCopy = self.river[:]
    
    for index in range(len(self.river)): # 0 ... len(river)-1
      print("Index is " + str(index))
      
      obj = self.river[index]
      print("Obj is " + str(obj))
      next_obj = self.river[0] if (index == len(self.river)-1) else self.river[index+1]
      print("Next obj is " + str(next_obj))

      # Skip over things that have already been dealt with
      if self.skip:
        self.skip_done += 1
        print("Skipping... " + str(self.skip_done) + "/" + str(self.skip_times))
        self.skip = False
        self.skip_times = 0
        self.skip_done = 0

      else:
        if index == len(self.river)-1:
          if obj != None and (riverCopy[0] == None or isinstance(obj, Bear)):
            print("Moving object at the end of the river to the front because it is a bear or there is a free spot at the front")
            riverCopy[0] = obj
            if riverCopy[index] == obj: riverCopy[index] = None
          else:
            print("Fish at the end of the river continues downstream because the front is full")

        elif next_obj == None: 
          # If nothing is downstream, then we don't need to care what this obj is
          print("Moving object forward to empty space")
          riverCopy[index+1] = obj
          if riverCopy[index] == obj: riverCopy[index] = None

        elif isinstance(obj, Fish) and isinstance(next_obj, Fish):
          # This way, upstream fish won't move, as requested
          print("Two fish collided.")
          if obj.get_sex() != next_obj.get_sex():
            print("Will spawn a new fish")
            self.new_strength = (obj.get_strength() + next_obj.get_strength())/2
            self.new_sex = "M" if randint(0,2) == 0 else "F"
            self.spawn_fish += 1
          else:
            print("Two fishes be fighting")
            if obj.get_strength() > next_obj.get_strength():
              obj.set_strength(obj.get_strength() - next_obj.get_strength())
              riverCopy[index+1] = obj
              riverCopy[index] = None
            else:
              next_obj.set_strength(next_obj.get_strength() - obj.get_strength())
              riverCopy[index] = None

        elif isinstance(obj, Bear) and isinstance(next_obj, Bear):
          # Fight or f u * * ?
          print("Two bears collided.")
          if obj.get_sex() != next_obj.get_sex():
            print("Will spawn a new bear")
            self.new_strength = (obj.get_strength() + next_obj.get_strength())/2
            self.new_sex = "M" if randint(0,2) == 0 else "F"
            self.spawn_bear += 1
          else:
            print("Two beares be fighting")
            if obj.get_strength() > next_obj.get_strength():
              obj.set_strength(obj.get_strength() - next_obj.strength())
              riverCopy[index+1] = obj
              riverCopy[index] = None
            else:
              next_obj.set_strength(next_obj.get_strength() - obj.get_strength())
              riverCopy[index] = None
            

        elif isinstance(obj, Fish) and isinstance(next_obj, Bear):
          # Fish hides himself so it does not become dinner
          print("A fish avoided being eaten!")

        elif isinstance(obj, Bear) and isinstance(next_obj, Fish):
          # Poor fish :(
          print("A fish got rekt.")
          obj.set_strength(obj.get_strength() + next_obj.get_strength())
          riverCopy[index+1] = obj
          riverCopy[index] = None
          self.skip = True
          self.skip_times = 1
        
    for i in range(self.spawn_fish):
      print("Spawned that fish from earlier.")
      done = False
      while not done:
        # find a random empty space for new fishe :)
        new = randint(0,len(riverCopy)-1)
        if riverCopy[new] == None:
          riverCopy[new] = Fish(self.new_strength, self.new_sex)
          done = True
    
    for i in range(self.spawn_bear):
      print("Spawned that bear from earlier.")
      done = False
      while not done:
        # find a random empty space for new bere :)
        new = randint(0,len(riverCopy)-1)
        if riverCopy[new] == None:
          riverCopy[new] = Bear(self.new_strength, self.new_sex)
          done = True
          
    self.spawn_fish = 0

    self.river = riverCopy
    self.logRiver()
    self.step_num += 1

  def logRiver(self):
    # Grab the __str__'s of all animals, and log them
    state = ""
    for element in self.river:
      state += str(element) + "\n"
    print(state)
    with open("output.txt","a") as f:
      f.write(state + "\n")
    
    if self.html_out:
      self.generate_html()

  def generate_html(self):
    with open("container.html") as f:
      container = f.read()
    fn = "output_step_" + str(self.step_num) + ".html"
    with open("output_template.html") as f:
      html = f.read()
    containers = ""
    for obj in self.river:
      if obj != None:
        src = obj.get_image()
      else:
        src="water.ppm"
      my_container = container.replace("$SRC", src)
      containers += my_container
    containers = "<a href=\"output_step_" + str(self.step_num+1) + ".html\">Next step</a>" + containers 
    with open(fn,"w") as f:
      f.write(html.replace("$DAT",containers).replace("$X", str(self.step_num)))

        
  def get_size(self):
    ''' Returns the size of the river '''
    return len(self.river)

  def get_inhabitant(self, index):
    ''' Returns the item at this index of the river.
    It should either be a Bear, Fish, or None
    '''
    if self.river[index] is not None:
      return self.river[index]
    else:
      return None

  def quit(self):
    '''Called when program quits. Close your output file.'''
    if not self.html_out:
      print("Cleaning up dynamic files")
      for file in os.listdir():
        if "-" in file:
          print("Removing: " + file)
          os.remove(file)
    else:
      print("Not cleaning up since we've made html")

class Animal:
  def __init__(self, image_file, strength, sex):
    self._strength = strength
    self._sex = sex
    self.__image = image_file
  def get_image(self):
    return self.generate_img()
  def get_sex(self):
    return self._sex
  def get_strength(self):
    return self._strength
  def set_strength(self, new):
    self._strength = new
    self.generate_img()
  def generate_img(self):
    img = Image.open(self.__image)
    d1 = ImageDraw.Draw(img)
    d1.text((0, 0), "Strength: " + str(self._strength), fill=(255, 0, 0))
    d1.text((0,90), "Sex: " + self._sex, fill=(255, 0, 0))
    
    fn = self.__image + "-" + str(self._strength) + "-" + self._sex + ".png"
    img.save(fn)
    return fn
    

class Bear(Animal):
  def __init__(self, strength, sex):
    super().__init__("bear.ppm", strength, sex)
  def imabear(self):
    return
  def __str__(self):
    sex = "Male" if self._sex == "M" else "Female"
    string = "Bear " + sex
    string += " " + str(self._strength)
    return string
  def __repr__(self):
    return self.__str__()

class Fish(Animal):
  def __init__(self, strength, sex):
    img = "salmon.ppm" if sex == "F" else "newsalmon.png" 
    super().__init__(img, strength, sex)
  def icanswim(self):
    return
  def __str__(self):
    sex = "Male" if self._sex == "M" else "Female"
    string = "Fish " + sex
    string += " " + str(self._strength)
    return string
  def __repr__(self):
    return self.__str__()
  
