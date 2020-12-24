def xmaslight():
    # This is the code from my 
    
    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    import board
    import neopixel
    import re
    import math
    
    # You are welcome to add any of these:
    # import random
    # import numpy
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES (please don't break this bit)
    
    coordfilename = "Python/coords.txt"
	
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    
    pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    
    
    # YOU CAN EDIT FROM HERE DOWN
    # The Christmas Tree Brownian Motion !
    import random
    
    #   The way it works is this : it will visit a new light at every step, selected uniformly from
    # the set of lights within a sphere of a given radius.
    neighbourhood_radius = 50
    
    # Here is a distance function to help us determine who are our neighbours.
    def distance(p1, p2):
        if len(p1) != len(p2) :
            return -1
        else :
            dsq = 0
            i = 0
            while i < len(p1):
                dsq += (p2[i]-p1[i]) ** 2
            return dsq ** .5
    
    #   The light where the walk IS will be a certain initial colour. It will then fade to black
    # as time passes.
    
    # This defines how the fade out happens over this period of time.
    def color_fade_from_age(age):
        # As a default, we start out bright white. But you could have it set up differently.
        init_colour = [255, 255, 255]
        
        # This controls how long the fade out takes (in cycles)
        fade_time = 500
        
        # These exponents control how the fade happens. The higher the exponent, the quicker that colour (RGB) fades out.
        # The values here should make a fade out with more blue in it, but you can switch things up if you like !
        exponent = [5, 5, 0.3]
        f_age = age/fade_time
        
        if age < fade_time and age >= 0:
            return [ int( init_colour[0] * (1-f_age) ** exponent[0] ), int( init_colour[1] * (1-f_age) ** exponent[1] ), int( init_colour[2] * (1-f_age) ** exponent[2] ) ]
        else :
            return [0,0,0]
    
    # INITIALISE SOME VALUES
    current = 0 #index of the current LED
    nearest = 0 #index of the nearest LED
    neighbours = [] #list of indices of LEDs within the radius
    ages = [-1] * len(coords) #ages (time since last visit) for all LEDs. -1 if never visited.
    
    # ... AND THEN FOREVER UNTIL THE END OF TIMES ...
    while True:
        
        time.sleep(slow)
        
        # On our first loop around, we figure out who our neighbours are.
        # We also keep track of the nearest LED, just in case there's no one in our "neighbourhood".
        
        i = 0
        nearest = (current + 1) % len(coords) # Just so we don't start with the current as nearest and never update it.
        d_n = distance(coords[current], coords[nearest])
        neighbours = [] 
        
        while i < len(coords):
            if i != current:
                d = distance(coords[current], coords[i]) #we get the distance to i.
                
                # Check if i is nearer than "nearest", and update accordingly.
                if d < d_n:
                    nearest = i
                    d_n = d
                    
                # Check if we're within the radius and update neighbours if need be :
                if d < neighbourhood_radius:
                    neighbours.append(i)
                    
            i += 1
            
        # we should now have figured out who our neighbours are.
        
        # If we have no neighbours, we move to the nearest LED. Otherwise we just pick a neighbour at random.
        if neighbours == []:
            current = nearest
        else:
            current = random.choice(neighbours)
        
        # On our second loop around, we will set the colours for the LEDs in the current state, and
        # update the ages for the next state :
        LED = 0
        while LED < len(coords):
            # Set the colour :
            pixels[LED] = colour_fade_from_age(ages[LED])
            
            # update the ages
            ages[LED] += 1
            if LED == current:
                ages[LED] = 0
            
            LED += 1
        
        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        pixels.show()
        
    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()
