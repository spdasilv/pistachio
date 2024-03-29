import random, json
from urllib.request import urlopen
from math import radians, cos, sin, asin, sqrt

# Let W be the normalized weight of the interest point.
# Let T represent the average time spent visiting the interest point.
# Let ID be an unique identifier for a location.
# Let NAME be the name of a location.
# Let T_OPEN be the opening time of a location.
# Let T_CLOSE be the closing time of a location.
class InterestPoint:
    def __init__(self, w, t, id, schedule, lat, lon):
        self.w = w
        self.t = t
        self.id = id
        self.lat = lat
        self.lon = lon
        self.t_open = {}
        self.t_close = {}

        for i in range(0, 7):
            day = i + 1
            if day in schedule:
                self.t_open[day] = schedule[day][0]
                self.t_close[day] = schedule[day][1]
            else:
                self.t_open[day] = 540
                self.t_close[day] = 1080

    def getW(self):
        return self.w

    def getT(self):
        return self.t

    def getId(self):
        return self.id

    def __repr__(self):
        return str(self.getId()) + ", " + str(self.getT()) + ", " + str(self.getW())

# Let each bucket represent each day. This class stores the overall detail of the points visited for a given day.
class Bucket:
    week_day = None
    timeUsed = 0
    start_time = None
    end_time = None
    totalWeight = 0
    plan = None

    def __init__(self, weekday, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.week_day = weekday
        self.plan = []

    def getTime(self, index):
        return self.destinationPoints[index]

    def incrementTime(self, time):
        self.timeUsed += time

    def getWeight(self, index):
        return self.destinationPoints[index]

    def incrementWeight(self, weight):
        self.totalWeight += weight

    def addToPlan(self, id, start_time, activity_time, lon, lat):
        self.plan.append((id, start_time, activity_time, lon, lat))

# The TourManager hold information about all available locations and the distance costs.
class TourManager():

    base = None
    timeCosts = None
    destinationPoints = None

    def __init__(self, origin, timeCosts):
        self.destinationPoints = []
        self.base = origin
        self.timeCosts = timeCosts

    def addPoint(self, point):
        self.destinationPoints.append(point)

    def getPoint(self, index):
        return self.destinationPoints[index]

    def numberOfPoints(self):
        return len(self.destinationPoints)

# The Tour is responsible for generating the schedules randomly as well as calculating the fittness scores for each schedule.
class Tour:
    def __init__(self, tourmanager, timeCosts, days, tour=None):
        self.days = days
        self.plan = []
        self.timeCosts = timeCosts
        self.tourmanager = tourmanager
        self.tour = []
        self.fitness = 0.0
        self.score = 0
        self.base = tourmanager.base
        if tour is not None:
            self.tour = tour
        else:
            for i in range(0, self.tourmanager.numberOfPoints()):
                self.tour.append(None)

    def __len__(self):
        return len(self.tour)

    def __getitem__(self, index):
        return self.tour[index]

    def __setitem__(self, key, value):
        self.tour[key] = value

    def __repr__(self):
        geneString = "|"
        for i in range(0, self.tourSize()):
            geneString += str(self.getPoint(i)) + "|"
        return geneString

    def generateIndividual(self):
        for pointIndex in range(0, self.tourmanager.numberOfPoints()):
            self.setPoint(pointIndex, self.tourmanager.getPoint(pointIndex))
        random.shuffle(self.tour)

    def getPoint(self, tourPosition):
        return self.tour[tourPosition]

    def setPoint(self, tourPosition, point):
        self.tour[tourPosition] = point
        self.fitness = 0.0
        self.score = 0

    def getFitness(self):
        if self.fitness == 0:
            self.fitness = float(self.getScore())
        return self.fitness

    def getScore(self):
        if self.score == 0:
            tourScore = 0
            travelTime = 0
            buckets = []
            for key, value in self.days.items():
                buckets.append(Bucket(value['weekday'], value['start'], value['end']))
            removed = set()
            for bucket in buckets:
                previousPoint = self.base
                for pointIndex in range(0, self.tourSize()):
                    currentPoint = self.getPoint(pointIndex)
                    if currentPoint.id in removed:
                        continue
                    activity_start = bucket.start_time + bucket.timeUsed + self.timeCosts[(previousPoint.id, currentPoint.id)]
                    activity_end = activity_start + currentPoint.t + 0
                    if activity_end + self.timeCosts[(currentPoint.id, self.base.id)] <= bucket.end_time \
                            and currentPoint.t_open[bucket.week_day] <= activity_start \
                            and activity_end <= currentPoint.t_close[bucket.week_day]:
                        bucket.incrementWeight(currentPoint.w)
                        bucket.addToPlan(currentPoint.id, bucket.start_time + bucket.timeUsed + self.timeCosts[(previousPoint.id, currentPoint.id)], currentPoint.t, currentPoint.lat, currentPoint.lon)
                        bucket.incrementTime(currentPoint.t + self.timeCosts[(previousPoint.id, currentPoint.id)])
                        travelTime = travelTime + self.timeCosts[(previousPoint.id, currentPoint.id)]
                        previousPoint = currentPoint
                        removed.add(currentPoint.id)
                    else:
                        continue
                tourScore += bucket.totalWeight
            if len(removed) == self.tourSize():
                tourScore = tourScore + (10000/travelTime + 1)
            self.score = tourScore
            self.plan = buckets
        return self.score


    def tourSize(self):
        return len(self.tour)

    def containsPoint(self, point):
        return point in self.tour

# Initializes and manages population information.
class Population:
    def __init__(self, tourmanager, populationSize, initialise, cost_matrix, days):
        self.cost_matrix = cost_matrix
        self.tours = []
        self.days = days
        for i in range(0, populationSize):
            self.tours.append(None)

        if initialise:
            for i in range(0, populationSize):
                newTour = Tour(tourmanager, self.cost_matrix, self.days)
                newTour.generateIndividual()
                self.saveTour(i, newTour)

    def __setitem__(self, key, value):
        self.tours[key] = value

    def __getitem__(self, index):
        return self.tours[index]

    def saveTour(self, index, tour):
        self.tours[index] = tour

    def getTour(self, index):
        return self.tours[index]

    def getFittest(self):
        fittest = self.tours[0]
        for i in range(0, self.populationSize()):
            if fittest.getFitness() <= self.getTour(i).getFitness():
                fittest = self.getTour(i)
        return fittest

    def populationSize(self):
        return len(self.tours)

    def buckets(self):
        return self.days

# The core of the GA Solution. This class is responsible for generating new populations.
# To generate a new generation for a population a tournament selection evolution is performed.
# Tournament selection ensures that only the fittest schedules evolve to the next generation.
# This class is also responsible for the crossover and mutation between schedules.
class GA:
    def __init__(self, tourmanager, cost_matrix):
        self.cost_matrix = cost_matrix
        self.tourmanager = tourmanager
        self.mutationRate = 0.05
        self.tournamentSize = 5
        self.elitism = True

    def evolvePopulation(self, pop):
        newPopulation = Population(self.tourmanager, pop.populationSize(), False, self.cost_matrix,  pop.buckets())
        elitismOffset = 0
        if self.elitism:
            newPopulation.saveTour(0, pop.getFittest())
            elitismOffset = 1

        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.tournamentSelection(pop)
            parent2 = self.tournamentSelection(pop)
            child = self.crossover(parent1, parent2, pop.buckets())
            newPopulation.saveTour(i, child)

        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getTour(i))

        return newPopulation

    def crossover(self, parent1, parent2, buckets):
        child = Tour(self.tourmanager, self.cost_matrix, buckets)

        startPos = int(random.random() * parent1.tourSize())
        endPos = int(random.random() * parent1.tourSize())

        for i in range(0, child.tourSize()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setPoint(i, parent1.getPoint(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    child.setPoint(i, parent1.getPoint(i))

        for i in range(0, parent2.tourSize()):
            if not child.containsPoint(parent2.getPoint(i)):
                for ii in range(0, child.tourSize()):
                    if child.getPoint(ii) == None:
                        child.setPoint(ii, parent2.getPoint(i))
                        break

        return child

    def mutate(self, tour):
        for tourPos1 in range(0, tour.tourSize()):
            if random.random() < self.mutationRate:
                tourPos2 = int(tour.tourSize() * random.random())

                point1 = tour.getPoint(tourPos1)
                point2 = tour.getPoint(tourPos2)

                tour.setPoint(tourPos2, point1)
                tour.setPoint(tourPos1, point2)

    def tournamentSelection(self, pop):
        tournament = Population(self.tourmanager, self.tournamentSize, False, self.cost_matrix, pop.buckets())
        for i in range(0, self.tournamentSize):
            randomId = int(random.random() * pop.populationSize())
            tournament.saveTour(i, pop.getTour(randomId))
        fittest = tournament.getFittest()
        return fittest

# Calculate the great circle distance between two points on the earth (specified in decimal degrees)
def Haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

# Calculate the cost of time to travel between two points given an arbitrary moving speed.
def calculateCost(coordinates):
    time_cost = {}
    for key1, value1 in coordinates.items():
        for key2, value2 in coordinates.items():
            if value1['id'] == value2['id']:
                time_cost[(value1['id'], value2['id'])] = 0
            else:
                if (value2['id'], value1['id']) in time_cost:
                    time_cost[(value1['id'], value2['id'])] = time_cost[(value2['id'], value1['id'])]
                else:
                    distanceSearch = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(
                        value1['lat']) + "," + str(value1['lon']) + "&destinations=" + str(value2['lat']) + "," + str(
                        value2['lon']) + "&mode=driving&key=AIzaSyAbUR_7faWzM6YBbcDtBXBLOfvpGc6L_Iw"
                    response = urlopen(distanceSearch)
                    string = response.read().decode('utf-8')
                    obj = json.loads(string)
                    time = int(obj['rows'][0]['elements'][0]['duration']['value'] / 60)
                    time_cost[(value1['id'], value2['id'])] = time + 20
    return time_cost


def scheduleRun(input, days):
    cost_matrix = calculateCost(input)
    tourmanager = TourManager(InterestPoint(input[0]['w'], input[0]['t'], input[0]['id'], input[0]['schedule'], input[0]['lat'], input[0]['lon']), cost_matrix)
    for key in input:
        if input[key]['id'] == 0:
            continue
        point = InterestPoint(input[key]['w'], input[key]['t'], input[key]['id'], input[key]['schedule'], input[key]['lat'], input[key]['lon'])
        tourmanager.addPoint(point)
    # Initialize population
    pop = Population(tourmanager, 120, True, cost_matrix, days)

    # Evolve population for 51 generations
    ga = GA(tourmanager, cost_matrix)
    for j in range(0, 51):
        pop = ga.evolvePopulation(pop)
    return pop.getFittest().plan
