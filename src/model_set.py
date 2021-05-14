import cv2
import random
from PIL import Image,ImageDraw,ImageFont
from sklearn import *
from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np

# take the target index we focus on 
digits=[' ','1','2','3','4','5','6','7','8','9']
# list of possible font we will using in the sudoku
fonts=[]
fonts+=['AcariSans-Regular.ttf']*3
fonts+=['din1451alt.ttf']*2
fonts+=['GOODDP__.TTF']*1
fonts+=['attack of the cucumbers.ttf']*1
fonts+=['Adamina-Regular.ttf']*5
fonts+=['arial.ttf']*5

# Supporting functions: working with the img RGB gray
def p2l(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)

def like(x,y):
    if y<1.2*x and y>0.8*x:
        return True
    return False

def imshow(image):
    return Image.fromarray(image)

def Drawdigit(txt):
    image = np.zeros(shape=(48,48),dtype=np.uint8)
    x = Image.fromarray(image)
    draw = ImageDraw.Draw(x)
    draw.text((8+random.randint(-4,16),2+random.randint(-4,6)),txt,(255),font=ImageFont.truetype(fonts[random.randint(0,len(fonts)-1)],random.randint(36,42),0))
	p = np.array(x)
    return p

def make_train_data(digits,num):
    x_train=[]
    y_train=[]
    for x in digits:
        for i in range(num):
            x_train.append(np.reshape(Drawdigit(x), (2304)))
            y_train.append(x)
    return x_train,y_train

x_train,y_train=make_train_data(digits,1000)
x_test,y_test=make_train_data(digits,50)
model = KNeighborsClassifier(n_neighbors=5)
model.fit(x_train, y_train)
print(model.score(x_test,y_test))

filename = 'model.sav'
joblib.dump(model, filename)