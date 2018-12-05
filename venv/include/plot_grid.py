# import matplotlib.pyplot as plt
# import pyplot as plt
import numpy as np
import random as rd
import scipy as sp

rd.seed()

# set parameters
width = 100
height = 100
maxTime = 500

# Preys
initialRabbitPopulation = 100
rabbitReproductionRate = 0.1
rabbitPopulationLimit = 500
rabbitNoiseLevel = 2

# Predators
initialFoxPopulation = 30
foxReproductionRate = 0.5
foxPopulationLimit = 500
foxNoiseLevel = 3
foxHungerLimit = 10
collisionDistance = 2
CDsquared = collisionDistance ** 2

# initialize agents
rabbits = []
foxes = []

for i in range(initialRabbitPopulation):
    rabbits.append([rd.uniform(0, width), rd.uniform(0, height)])

for i in range(initialFoxPopulation):
    foxes.append([rd.uniform(0, width), rd.uniform(0, height), 0])

rabbitData = [initialRabbitPopulation]
foxData = [initialFoxPopulation]

def clip(a, amin, amax):
    if a < amin:
        return amin
    elif a > amax:
        return amax
    else:
        return a


toBeRemoved = -1

for t in range(maxTime):

    # simulate random motion
    for ag in rabbits:
        ag[0] += rd.gauss(0, rabbitNoiseLevel)
        ag[1] += rd.gauss(0, rabbitNoiseLevel)
        ag[0] = clip(ag[0], 0, width)
        ag[1] = clip(ag[1], 0, height)

    for ag in foxes:
        ag[0] += rd.gauss(0, foxNoiseLevel)
        ag[1] += rd.gauss(0, foxNoiseLevel)
        ag[0] = clip(ag[0], 0, width)
        ag[1] = clip(ag[1], 0, height)

    # detect collision and change state
    for i in range(len(foxes)):
        foxes[i][2] += 1                      # fox's hunger level increasing
        for j in range(len(rabbits)):
            if rabbits[j] != toBeRemoved:
                if (foxes[i][0]-rabbits[j][0])**2 + (foxes[i][1]-rabbits[j][1])**2 < CDsquared:
                    foxes[i][2] = 0           # fox ate rabbit and hunger level reset to 0
                    rabbits[j] = toBeRemoved  # rabbit eaten by fox
        if foxes[i][2] > foxHungerLimit:
            foxes[i] = toBeRemoved            # fox died due to hunger

    # remove "toBeRemoved" agents
    while toBeRemoved in rabbits:
        rabbits.remove(toBeRemoved)
    while toBeRemoved in foxes:
        foxes.remove(toBeRemoved)

    # count survivors' populations
    rabbitPopulation = len(rabbits)
    foxPopulation = len(foxes)

    # produce offspring
    for i in range(len(rabbits)):
        if rd.random() < rabbitReproductionRate * (1.0 - float(rabbitPopulation) / float(rabbitPopulationLimit)):
            rabbits.append(rabbits[i][:]) # making and adding a copy of the parent

    for i in range(len(foxes)):
        if foxes[i][2] == 0 and rd.random() < foxReproductionRate * (1.0 - float(foxPopulation) / float(foxPopulationLimit)):
            foxes.append(foxes[i][:]) # making and adding a copy of the parent

    rabbitData.append(len(rabbits))
    foxData.append(len(foxes))

# mp.imshow(z)
# mp.gray()
# mp.show()

# plt.imshow(z)
# plt.gray()
# plt.show()

###################################################################

import glumpy
import numpy as np

# Generate some data...
x, y = np.meshgrid(np.linspace(-2,2,200), np.linspace(-2,2,200))
x, y = x - x.mean(), y - y.mean()
z = x * np.exp(-x**2 - y**2)

window = glumpy.Window(512, 512)
im = glumpy.Image(z.astype(np.float32), cmap=glumpy.colormap.Grey)

@window.event
def on_draw():
    im.blit(0, 0, window.width, window.height)
window.mainloop()
