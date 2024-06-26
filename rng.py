import numpy as np
import imageio.v2 as imageio
import math
import matplotlib.pyplot as plt


bitsNeeded      = int(input("Liczba bajtow do wygenerowania: "))*8
lastFrame = 0
lastBit = 0
bitsGenerated   = 0
generatedArray = []
matrixDimension = math.floor(math.sqrt(bitsNeeded)) 
squareArray     = np.zeros([matrixDimension, matrixDimension], dtype=np.uint8) 
bitsInMatrix = matrixDimension*matrixDimension

frames = int(input("Liczba obrazow: ")) 

for frame in range(1, frames+1):

    img = imageio.imread('res/{}.bmp'.format(frame))
    lastFrame = frame
    lastBit = 0                                                                                          
    HEIGHT      = np.shape(img)[0]
    WIDTH       = np.shape(img)[1]
    CHANNELS    = np.shape(img)[2]
    OFFSET      = 2 

    img = img.transpose(1,2,0).ravel()
    dataArray = np.append(dataArray, img)
    if (frame%2): 
        for i in img:
            lastBit+=1
            if (bitsGenerated>=bitsInMatrix):
                break
            elif (i>=OFFSET and i<=255-OFFSET):
                H = bitsGenerated//matrixDimension
                W = bitsGenerated%matrixDimension
                squareArray[H][W] = i&1
                bitsGenerated+=1
    else:
        for i in img:
            lastBit+=1
            if (bitsGenerated>=bitsInMatrix):
                break
            elif (i>=OFFSET and i<=255-OFFSET):
                H = bitsGenerated//matrixDimension
                W = bitsGenerated%matrixDimension
                squareArray[H][W] = (i+1)&1
                bitsGenerated+=1
    
    if (bitsGenerated>=bitsInMatrix):
        break
                         
squareArray = squareArray.ravel(order="F")

bitsLeft = bitsNeeded - bitsGenerated
if bitsGenerated<bitsNeeded:
    squareArray = np.append(squareArray, (img[lastBit:(lastBit+bitsLeft)]&1))
    bitsGenerated = len(squareArray)

bitCount = 0
integer = 0
for i in squareArray:
    if bitCount < 8:
        integer = integer << 1 
        integer += int(i)
        bitCount+=1
    elif bitCount ==  8:
        generatedArray.append(integer)
        integer = 0
        bitCount = 0

weights = np.ones_like(generatedArray) / len(generatedArray)
plt.hist(generatedArray, bins=256, weights=weights)
plt.show()
print("Bytes generated: " + str(bitsGenerated))
print(generatedArray)

    
    

