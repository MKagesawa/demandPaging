import sys

machineSize = sys.argv[1]
pageSize = sys.argv[2]
processSize = sys.argv[3]
jobMix = sys.argv[4]
numRef = sys.argv[5]
replacementAlgo = sys.argv[6]
debugLevel = sys.argv[7]

print("The machine size is " + machineSize + ".")
print("The page size is " + pageSize + ".")
print("The process size size is " + processSize + ".")
print("The job mix number is " + jobMix + ".")
print("The number of references per process is " + numRef + ".")
print("The replacement algorithm is " + replacementAlgo + ".")
print("The level of debugging output is " + debugLevel + ".")

randomNumbers = None
with open("random-numbers.txt") as f:
    randomNumbers = f.readlines()

counter = 0
def randomOS(counter):
    num = int(randomNumbers[int(counter)])
    if debugLevel == "11":
        print(int(randomNumbers[int(counter)]))
    return num


class Process:
    def __init__(self, processSize, processNum):
        self.processSize = processSize
        self.numFault = 0
        self.numEvict = 0
        self.resTime = 0
        self.nextRef = (111 * processNum) % processSize

    def nextRef(self, A, B, C):
        global counter
        randomNum = randomOS(counter)
        counter += 1
        ratio = randomNum / 2147483648
        if ratio < A:
            self.nextRef = (self.nextRef + 1) % processSize
        elif ratio < A + B:
            self.nextRef = (self.nextRef -5 + processSize) % processSize
        elif ratio < A + B + C:
            self.nextRef = (self.nextRef + 4) % processSize
        else:
            self.nextRef = randomNum % processSize
            counter += 1




















