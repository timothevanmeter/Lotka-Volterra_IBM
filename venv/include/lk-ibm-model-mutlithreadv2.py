#   MULTITHREAD VERSION OF THE
# 	IBM SCRIPT FOR ECEV42600
###
# 	MODIFIED FROM predatorprey-withplot.py PyCX Project
###
# 	Timothe Van Meter (timothevanmeter.github.io)


# import pylab as pl
import random as rd
import scipy as SP
import numpy as np
import pandas as pd
from multiprocessing import Process, Queue



# TODO: use a def function to have all initial settings in one container

# set parameters

# ENVIRONMENT DIMENSIONS
width = 1000
height = 1000
# SIMULATION TIME
maxTime = 50

# PREYS
initialRabbitPopulation = 500
rabbitReproductionRate = 0.3
# EQUIVALENT TO K
rabbitPopulationLimit = 1000
# EXPLANATION?
rabbitNoiseLevel = 8
# rabbitBackgroundMortality = 0.05

# PREDATORS
initialFoxPopulation = 300
foxReproductionRate = 0.3
# EQUIVALENT TO K
foxPopulationLimit = 1000
#
foxNoiseLevel = 15
# foxHungerLimit = 30
foxBackgroundMortality = 0.03

# PREDATION PARAMETERS
# MINIMUM DISTANCE FOR WHICH A PREDATION EVENT CAN OCCUR
collisionDistance = 10

# WORKING DIRECTORY
home = '/home/timothe/WORK/lk-ibm-model/'

# INITIALIZING THE CSV FILE
data_sim = pd.DataFrame(columns=['parameter_value', 'predator_minimum', 'predator_maximum'])
initcsv = data_sim.to_csv('/home/timothe/WORK/lk-ibm-model/sim_summary.csv', header=True)
initcsv



# INITIALIZING AGENTS TABLES
rabbits = []
foxes = []
for i in range(initialRabbitPopulation):
    rabbits.append([rd.uniform(0, width), rd.uniform(0, height)])

for i in range(initialFoxPopulation):
    foxes.append([rd.uniform(0, width), rd.uniform(0, height), 0])
rabbitData = [initialRabbitPopulation]
foxData = [initialFoxPopulation]

# INITIALIZING RANDOM SEED
rd.seed()


# RUN FOR ONE SIMULATION
def simulation(data, q):

    # INITIALIZING RANDOM SEED
    rd.seed()

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
                foxes[i][2] += 1  # fox's hunger level increasing
                for j in range(len(rabbits)):
                    if rabbits[j] != toBeRemoved:
                        if (foxes[i][0] - rabbits[j][0]) ** 2 + (foxes[i][1] - rabbits[j][1]) ** 2 < CDsquared:
                            foxes[i][2] = 0  # fox ate rabbit and hunger level reset to 0
                            rabbits[j] = toBeRemoved  # rabbit eaten by fox
                    # if rd.uniform(0, 1) < rabbitBackgroundMortality:
                    # rabbits[j] = toBeRemoved  # rabbit bakground motality ***ADDED***
                if rd.uniform(0, 1) < foxBackgroundMortality:  # fox background mortality ***ADDED***
                    # if foxes[i][2] > foxHungerLimit:
                    foxes[i] = toBeRemoved  # fox died due to hunger

            # remove "toBeRemoved" agents
            while toBeRemoved in rabbits:
                rabbits.remove(toBeRemoved)
            while toBeRemoved in foxes:
                foxes.remove(toBeRemoved)

            # count survivors' populations
            rabbitPopulation = len(rabbits)
            foxPopulation = len(foxes)

            # MODEL RETENTION CRITERIA
            if foxPopulation == 0:
                print("\n\n----->  PREDATOR POPULATION EXTINCTION\n\n")
                # store()
                break
            if rabbitPopulation == 0:
                print("\n\n----->  PREY POPULATION EXTINCTION\n\n")
                # store()
                break
            # We are interested in simulations allowing coexistence
            # As soon as this criteria is violated the simulation is discarded

            # produce offspring
            for i in range(len(rabbits)):
                if rd.random() < rabbitReproductionRate * (
                        1.0 - float(rabbitPopulation) / float(rabbitPopulationLimit)):
                    rabbits.append(rabbits[i][:])  # making and adding a copy of the parent

            for i in range(len(foxes)):
                if foxes[i][2] == 0 and rd.random() < foxReproductionRate * (
                        1.0 - float(foxPopulation) / float(foxPopulationLimit)):
                    foxes.append(foxes[i][:])  # making and adding a copy of the parent

            rabbitData.append(len(rabbits))
            foxData.append(len(foxes))

    # SHOWS DATA TO STDOUT
    print("\n\n FoxMin = " +str(min(foxData))+ " ; FoxMax = " + str(max(foxData)))

    # SAVES SIMULATION SUMMARY IN DATA
    data.loc[i] = [initialFoxPopulation, min(foxData), max(foxData)]

    # PUSH DATA IN THE QUEUE
    q.put(data)


# SAVE SIMULATION DATA TO CSV FILE
def store(q):
    # prey = pd.DataFrame(rabbitData)
    # predator = pd.DataFrame(foxData)
    # # p1csv = prey.to_csv('/home/timothe/WORK/community_ecology/python-code/prey.csv')
    # # p1csv
    # # p2csv = predator.to_csv('/home/timothe/WORK/community_ecology/python-code/predator.csv')
    # # p2csv
    # # merge dataframes
    # sim = pd.concat([prey, predator], axis=1)
    # sim.columns = ['prey_number', 'predator_number']
    # # EXPORT OUTPUT TO CSV
    # name = 'sim_'+ str(initialFoxPopulation)
    # path_name = home + name + '.csv'
    # csv = sim.to_csv(path_name)
    # csv

    ################
    # SIMULATIONS SUMMARY
    dat = q.get()
    summarycsv = dat.to_csv('/home/timothe/WORK/lk-ibm-model//sim_summary.csv', mode='a', header=False)
    summarycsv



# LOOP FOR PARAMETER 1
for initialFoxPopulation in range(10, 12, 1):

    # VISUALIZE AGENTS
    # pl.ion()
    # fig = pl.figure()
    # pl.hold(False)
    def visualize(rb, fx, time):
        pl.subplot(1, 2, 1)

        pl.cla()
        if rb != []:
            x = [agent[0] for agent in rb]
            y = [agent[1] for agent in rb]
            pl.scatter(x, y, color='pink')
        if fx != []:
            pl.hold(True)
            x = [agent[0] for agent in fx]
            y = [agent[1] for agent in fx]
            pl.scatter(x, y, color='brown')
            pl.hold(False)
        pl.axis('scaled')
        pl.axis([0, width, 0, height])
        pl.title('t = ' + str(time))

        pl.subplot(1, 2, 2)

        pl.cla()
        pl.plot(rabbitData, color='pink')
        pl.hold(True)
        pl.plot(foxData, color='brown')
        pl.title('Populations')
        pl.hold(False)
    #
    #     fig.canvas.manager.window.update()
    # visualize(rabbits, foxes, 0)

    CDsquared = collisionDistance ** 2


    def clip(a, amin, amax):
        if a < amin:
            return amin
        elif a > amax:
            return amax
        else:
            return a


    toBeRemoved = -1


    # PARALLEL PROCESSING FOR REPLICATES
    ####################################

    # DEFINE AN OUTPUT QUEUE
    q = Queue()

    # CREATES  A LIST TO STACK PENDING PROCESSES
    procs =[]

    # CREATES AND STARTS AS MANY PROCESSES AS SIMULATION REPLICATES
    # HERE, 5 REPLICATES PER SIMULATION
    for i in range(10):
        proc1 = Process(target=simulation, args=(data_sim, q))
        proc2 = Process(target=store, args=(q,))
        procs.append(proc1)
        procs.append(proc2)
        proc1.start()
        proc2.start()

    # RESOLVES ALL PROCESSES STARTED
    for proc in procs:
        q.close()
        q.join_thread()
        proc1.join()
        proc2.join()


    # SIGNAL SIMULATION END
    print '\n\nSIMULATION for value', str(initialFoxPopulation), 'ENDED'


print '\n\n------- PROGRAM FINISHED -------\n\n'