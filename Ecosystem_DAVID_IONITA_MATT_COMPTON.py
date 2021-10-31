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

  def step(self): # O(n^2) + O(n) + O(n) + O(n) + a BUNCH of O(1)s = O(n^2 + 3n + a BUNCH of 1s) = O(n^2)
    # NOTE: It is O(n^2) only if you choose to print the HTML file; otherwise, it is O(n) because it removes the n^2 caused by the generate_html function.

    # Moves the whole river one step forward in time.
    # At the end, it should also print the state of the river
    # and save it to a file
    
    self.spawn_fish = 0 # O(1)
    self.spawn_bear = 0 # O(1)

    self.last = False # O(1)
    self.first = False # O(1)

    self.skip = False # O(1)
    self.skip_times = 0 # O(1)
    self.skip_done = 0 # O(1)

    riverCopy = self.river[:] # O(n)
    
    for index in range(len(self.river)): # n reps  # 0 ... len(river)-1
      
      obj = self.river[index]  # O(1)
      next_obj = self.river[0] if (index == len(self.river)-1) else self.river[index+1] # O(1) <- max

      # Skip over things that have already been dealt with
      if self.skip: # O(1) test
        self.skip_done += 1 # O(1)
        print("Skipping... " + str(self.skip_done) + "/" + str(self.skip_times)) # O(1)
        self.skip = False # O(1)
        self.skip_times = 0 # O(1)
        self.skip_done = 0 # O(1)
      # test + body = 1+5 = O(1)
      else:
        if index == len(self.river)-1: # O(1) test
          if obj != None and (riverCopy[0] == None or isinstance(obj, Bear)): # O(1) test
            print("Moving object at the end of the river to the front because it is a bear or there is a free spot at the front") # O(1)
            riverCopy[0] = obj # O(1)
            if riverCopy[index] == obj: # O(1) test
              riverCopy[index] = None  # O(1)
            # test + body = 1+1 = O(1)
          # test + body = 1+1 = O(1)
          else:
            print("Fish at the end of the river continues downstream because the front is full") # O(1)
          # test + body = 1+1 = O(1)
        # test + body = 1+1 = O(1)

        elif next_obj == None:  # O(1) test
          # If nothing is downstream, then we don't need to care what this obj is
          print("Moving object forward to empty space") # O(1)
          riverCopy[index+1] = obj # O(1)
          if riverCopy[index] == obj: # O(1) test
            riverCopy[index] = None # O(1)
          # test + body = 1+1 = O(1)
        # test + test + body = 1+1+1 = O(1)

        elif isinstance(obj, Fish) and isinstance(next_obj, Fish): # O(1) test
          # This way, upstream fish won't move, as requested
          print("Two fish collided.") # O(1)
          if obj.get_sex() != next_obj.get_sex(): # O(1) test and function
            print("Will spawn a new fish") # O(1)
            self.new_strength = (obj.get_strength() + next_obj.get_strength())/2 # O(1) function
            self.new_sex = "M" if randint(0,2) == 0 else "F"  # O(1) assuming randint is constant time based on Google searches
            self.spawn_fish += 1 # O(1)
          # test + body = 1+4 = O(1)
          else:
            print("Two fishes be fighting") # O(1)
            if obj.get_strength() > next_obj.get_strength(): # O(1) test and function
              obj.set_strength(obj.get_strength() - next_obj.get_strength()) # O(1) function
              riverCopy[index+1] = obj # O(1)
              riverCopy[index] = None # O(1)
            # test + body = 1+4 = O(1)
            else:
              next_obj.set_strength(next_obj.get_strength() - obj.get_strength()) # O(1) function
              riverCopy[index] = None # O(1)
            # test + body = 1+2 = O(1)
          # test + body = 1+1 = O(1)
        # test + test + test + body = 1+1+1+1 = O(1)

        elif isinstance(obj, Bear) and isinstance(next_obj, Bear): # O(1) test
          # Fight or f u * * ?
          print("Two bears collided.") # O(1)
          if obj.get_sex() != next_obj.get_sex(): # O(1) test and function
            print("Will spawn a new bear") # O(1)
            self.new_strength = (obj.get_strength() + next_obj.get_strength())/2 # O(1) function
            self.new_sex = "M" if randint(0,2) == 0 else "F" # O(1)
            self.spawn_bear += 1 # O(1)
          # test + body = 1+4 = O(1)
          else:
            print("Two beares be fighting") # O(1)
            if obj.get_strength() > next_obj.get_strength(): # O(1) function
              obj.set_strength(obj.get_strength() - next_obj.get_strength()) # O(1) function
              riverCopy[index+1] = obj # O(1)
              riverCopy[index] = None # O(1)
            # test + body = 1+3 = O(1)
            else:
              next_obj.set_strength(next_obj.get_strength() - obj.get_strength()) # O(1) function
              riverCopy[index] = None # O(1)
            # test + body = 1+2 = O(1)
          # test + body = 1+1 = O(1)
        # test + test + test + test + body = 1+1+1+1+1 = O(1)    

        elif isinstance(obj, Fish) and isinstance(next_obj, Bear): # O(1) test
          # Fish hides himself so it does not become dinner
          print("A fish avoided being eaten!") # O(1)
        # test + test + test + test + test + body = 1+1+1+1+1+1 = O(1)

        elif isinstance(obj, Bear) and isinstance(next_obj, Fish): # O(1) test
          # Poor fish :(
          print("A fish got rekt.") # O(1)
          obj.set_strength(obj.get_strength() + next_obj.get_strength()) # O(1) function
          riverCopy[index+1] = obj # O(1)
          riverCopy[index] = None # O(1)
          self.skip = True # O(1)
          self.skip_times = 1 # O(1)
        # test + test + test + test + test + test + body = 1+1+1+1+1+1+1 = O(1)
      # test + test + body = 1+1+1 = O(1)
      # reps * body = n*1 = n = O(n)

    # left the for loop

    for i in range(self.spawn_fish): # n reps
      print("Spawned that fish from earlier.") # O(1)
      done = False # O(1)
      while not done: # O(1) this could theoretically be infinite, but for simplicity, I'm just gonna say O(1)
        # find a random empty space for new fishe :)
        new = randint(0,len(riverCopy)-1)  # O(1)
        if riverCopy[new] == None: # O(1) test
          riverCopy[new] = Fish(self.new_strength, self.new_sex) # O(1) function/constructor
          done = True # O(1)
        # test + body = 1+2 = O(1)
        # reps * body = 1*1 = O(1)
      # reps * body = n*1 = n = O(n)

    for i in range(self.spawn_bear): # n reps
      print("Spawned that bear from earlier.") # O(1)
      done = False # O(1)
      while not done: # O(1)
        # find a random empty space for new bere :)
        new = randint(0,len(riverCopy)-1) # O(1)
        if riverCopy[new] == None: # O(1) test
          riverCopy[new] = Bear(self.new_strength, self.new_sex) # O(1) function/constructor
          done = True # O(1)
        # test + body = 1+2 = O(1)
        # reps * body = 1*1 = O(1)
      # reps * body = n*1 = n = O(n)

    self.spawn_fish = 0 # O(1)

    self.river = riverCopy # O(1)
    self.logRiver() # O(n^2) called function
    self.step_num += 1 # O(1)

  def logRiver(self): # O(n^2) + O(n) + a BUNCH of O(1)s = O(n^2 + n + a BUNCH of 1s) = O(n^2)
    # Grab the __str__'s of all animals, and log them
    state = "" # O(1)
    for element in self.river: # n reps
      state += str(element) + "\n" # O(1)
      # reps * body = n*1 = n = O(n)

    print(state) # O(1)

    with open("output.txt","a") as f: # O(1)
      f.write(state + "\n") # O(1)
    
    if self.html_out: # O(1) test
      self.generate_html() # O(n^2) called function
    # test + body = 1 + n^2 = O(n^2)

  def generate_html(self): # O(n^2) + O(n) + a BUNCH of O(1)s = O(n^2 + n + a BUNCH of 1s) = O(n^2)
    with open("container.html") as f: # O(1)
      container = f.read() # O(1)
    fn = "output_step_" + str(self.step_num) + ".html" # O(1)
    with open("output_template.html") as f: # O(1)
      html = f.read() # O(1)
    containers = "" # O(1)
    for obj in self.river: # n reps
      if obj != None: # O(1) test
        src = obj.get_image() # O(1) function
      # test + body = 1+1 = O(1)
      else:
        src="water.ppm" # O(1)
      # test + body = 1+1 = O(1) 
      my_container = container.replace("$SRC", src) # O(n) because it replaces $SRC in file (there are n $SRC based on river size)
      containers += my_container # O(1)
      # reps * body = n*n+1 = n^2+1 = O(n^2)

    containers = "<a href=\"output_step_" + str(self.step_num+1) + ".html\">Next step</a>" + containers # O(1)
    with open(fn,"w") as f: # O(1)
      f.write(html.replace("$DAT",containers).replace("$X", str(self.step_num))) # O(n) + O(n) = O(2n) = O(n) because it replaces $DAT and $X one after another

        
  def get_size(self): # = O(1)
    ''' Returns the size of the river '''
    return len(self.river) # O(1)

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
  def __init__(self, image_file, strength, sex): # = O(1)
    self._strength = strength # O(1)
    self._sex = sex # O(1)
    self.__image = image_file # O(1)
  def get_image(self): # = O(1)
    return self.generate_img() # O(1) called function
  def get_sex(self): # = O(1)
    return self._sex # O(1)
  def get_strength(self): # = O(1)
    return self._strength # O(1)
  def set_strength(self, new): # = O(1)
    self._strength = new # O(1)
    self.generate_img() # O() function
  def generate_img(self): # = O(1)
    img = Image.open(self.__image) # O(1)
    d1 = ImageDraw.Draw(img) # O(1)
    d1.text((0, 0), "Strength: " + str(self._strength), fill=(255, 0, 0)) # O(1)
    d1.text((0,90), "Sex: " + self._sex, fill=(255, 0, 0)) # O(1)
    
    fn = self.__image + "-" + str(self._strength) + "-" + self._sex + ".png" # O(1)
    img.save(fn) # O(1)
    return fn # O(1) constant time, the size is fixed (fixed image size and text size)

# Below inherit the O(_) from above, when/if used

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
  
