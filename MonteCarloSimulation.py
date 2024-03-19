import math
import matplotlib.pyplot as plt
import numpy as np
import random

SEED = 1000
MULTIPLIER = 24693
INCREMENT = 3517
MODULUS = 2 ** 17


# Generates the nth random number in a sequence
def getNthRandomNumber(n, seed, multiplier, increment, modulus) -> float:
    prevValue = seed
    for i in range(0, n):
        randomNumber = generateRandomNumber(prevValue, multiplier, increment, modulus)
        prevValue = randomNumber * modulus
        if i == (n - 1):
            return randomNumber


# Generate a single random number
def generateRandomNumber(seed, multiplier, increment, modulus) -> float:
    value = ((multiplier * seed) + increment) % modulus
    randomNumber = value / modulus
    return randomNumber


# Returns a realized value of random variable X mapped to the probability distribution provided by the CDF of X
def getRealizationOfX(randomNumber) -> float:
    return -12 * math.log(1 - randomNumber) # Inverse of CDF of X


# Calculate the CDF of x, P[X<x]
def calculateCDFOfX(x):
    return 1 - (math.e ** (-x / 12))


# Calculate the CDF probability of an interval, P[xi < X < xf]
def calculateProbabilityOfInterval(xi, xf):
    return calculateCDFOfX(xf) - calculateCDFOfX(xi)


# Get CDF values for the intervals defined by the buckets
def getProbabilitiesForIntervals(bins) -> list:
    probabilitiesForIntervals = []
    for i in range(0, len(bins)):
        if i < (len(bins) - 1):
            probabilityForInterval = calculateProbabilityOfInterval(bins[i], bins[i + 1])
            probabilitiesForIntervals.append(probabilityForInterval)

    probabilitiesForIntervals.append(0)

    return probabilitiesForIntervals


# Generates a realized value of W based on the probability model of W
def getRealizationOfW(nthPosition) -> float:
    totalSeconds = 0
    recallNeeded = True
    for i in range(0,4): # Simulates 4 phone calls
        if recallNeeded: # Only performs a call if the previous call was not successful
            seconds, recallNeeded = simulateCall(4 * nthPosition, i)
            totalSeconds += seconds

    return totalSeconds


# Generates count realized values of W
def getRealizationsOfW(count) -> list:
    realizations = []
    for i in range (0, count):
        realizations.append(getRealizationOfW(i + 1))

    return realizations


# Simulates one phone call and returns the number of seconds that phone call took, and a boolean representing if another
# call is needed
def simulateCall(nthPosition, callNumber) -> (float, bool):
    seconds = 6 # Time to dial number
    recallNeeded = True # Recall is needed unless call is received

    CDFProbabilityValue = random.random() # Generate random number -> (0,1)
    x_realized = getRealizationOfX(CDFProbabilityValue) # Map random number to value of X

    probabilityFactor = getNthRandomNumber(nthPosition + callNumber, SEED, MULTIPLIER, INCREMENT, MODULUS) # Generate a random number
    #probabilityFactor = random.random()
    if probabilityFactor < 0.3: # Line is open (25 seconds to ring, 1 second to hang up)
        seconds += 26
    elif probabilityFactor < 0.5: # Line is busy (3 seconds to ring, 1 second to hang up)
        seconds += 4
    else:
        if x_realized > 25: # Call is missed (25 seconds to ring, 1 second to hang up)
            seconds += 26
        else: # Call received (x_realized seconds to ring)
            seconds += x_realized
            recallNeeded = False

    return (seconds, recallNeeded)


def plotStatsOfW():
    realizationsOfW = getRealizationsOfW(1000)

    # Plot realizations of random variable W
    realizationsOfWPlot = plt.figure()
    ax1 = realizationsOfWPlot.add_subplot()
    ax1.hist(realizationsOfW,
                                range=(0, 128),
                                bins=128,
                                label="Rrealizations of W")

    ax1.set_title("Frequency of Realizations of W")

    # Plot realizations of random variable W by probability
    probabilityOfRealizationsOfWPlot = plt.figure()
    ax2 = probabilityOfRealizationsOfWPlot.add_subplot()
    ax2.hist(realizationsOfW,
                                range=(0, 128),
                                bins=128,
                                weights=(np.ones(len(realizationsOfW)) / len(realizationsOfW)),
                                label="Realizations of W")

    ax2.set_title("Probability of Realizations of W")

    # Plot realizations of random variable W against probability with CDF of X overlay
    probabilityOfRealizationsOfW_XOverlayPlot = plt.figure()
    ax3 = probabilityOfRealizationsOfW_XOverlayPlot.add_subplot()
    n, bins, patches = ax3.hist(realizationsOfW,
             range=(0, 128),
             bins=128,
             weights=(np.ones(len(realizationsOfW)) / len(realizationsOfW)),
             label="Realizations of W")

    x = bins
    y = getProbabilitiesForIntervals(x)
    ax3.plot(x, y, label="CDF value of X", linestyle="dashed")

    plt.show()


def main():

    plotStatsOfW()

    # Plot significant points
    #plt.plot(18, calculateProbabilityOfInterval(12, 13), "^", label="E[X]")
    #plt.plot(31, calculateProbabilityOfInterval(31, 32), "^", label="Representative hangs up")

    # Format plot
    #plt.xlabel("Time spent calling customer (W)")
    #plt.ylabel("Probability (p)")
    #plt.title("Probability distribution for W — total time spent trying to reach a customer")
    #plt.legend(loc="upper right")

    #plt.show()

main()