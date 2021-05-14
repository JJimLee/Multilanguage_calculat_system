import numpy as np
import cv2
import math
import random
import json
import base64
import io
from werkzeug import secure_filename
from PIL import Image,ImageDraw,ImageFont
from sklearn import *
from sklearn.neighbors import KNeighborsClassifier
import joblib
from flask import Flask, jsonify, request,send_from_directory
import requests

model = joblib.load('src/model.sav')

def p2l(x,y):
    return math.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)
def like(x,y):
    if y<1.2*x and y>0.8*x:
        return True
    return False
def imshow(image):
    return Image.fromarray(image)

def sortreg(ang):
    ans=[]
    l=len(ang)
    a=0
    for x in range(l):
        if ang[x][0]+ang[x][1]<=ang[a][0]+ang[a][1]: 
            a=x
    ans.append(ang[a])
    del ang[a]
    l=len(ang)
    b=0
    for x in range(l):
        if ang[x][1]-ans[0][1] <= ang[b][1]-ans[0][1]:
            b=x
    ans.append(ang[b])
    del ang[b]
    l=len(ang)
    c=0
    for x in range(l):
        if ang[x][0]-ans[0][0] <= ang[c][0]-ans[0][0]:
            c=x  
    ans.append(ang[c])
    del ang[c]
    l=len(ang)
    ans.append(ang[0])
    print(ans)
    return ans

def enhance(x):
    i,j=np.shape(x)
    i=int(i*0.1)
    j=int(j*0.1)
    return x[i:-i,j:-j]

# virtical
def virticalErase(box,line):
    temp = box
    for i in range (9):
        temp[i][line]=0
    return temp
def horizontalErase(box,line):
    temp = box
    for i in range (9):
        temp[line][i]=0
    return temp
# horizontal
def cleanBox(box):
#     temp = []
    up=False
    down=False
    right=False
    left=False
    for i in range (1,8):
        if box[0][i]!=225:
            #make this line = [0 for i in range 9].
            up = True
        if box[8][i]!=225:
            down = True
        if box[i][0]!=225:
            left = True
        if box[i][8]!=225:
            right = True
    if up == False:
        box=horizontalErase(box,0)
    if down == False:
        box=horizontalErase(box,8)
    if right == False:
        box=virticalErase(box,8)
    if left == False:
        box=virticalErase(box,0)
    print("done check")
    return box

def read_sudo(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #edges = cv2.Canny(img,100,200)
    ret,thresh = cv2.threshold(gray,127,255,1)
    contours,h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     cv2.drawContours(img,contours,4,(0,0,255),1)
    rantList=[]
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.03*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            if like(p2l(approx[0][0],approx[1][0]),p2l(approx[1][0],approx[2][0])):
                rantList.append([approx,p2l(approx[0][0],approx[1][0])*p2l(approx[1][0],approx[2][0])])
                cv2.drawContours(img,[cnt],0,(255,0,0),1)
    biggest=rantList[0]
    for x in rantList:
        if x[1]>biggest[1]:
            biggest=x
#     cv2.drawContours(img,biggest,0,(0,255,0),1)
#     cv2.imshow('img',img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
    ang=[biggest[0][0][0],biggest[0][1][0],biggest[0][2][0],biggest[0][3][0]]
    ans=sortreg(ang)
    a,b,c,d=ans
    ix=(b[0]-a[0])//9
    iy=(b[1]-a[1])//9
    jx=(c[0]-a[0])//9
    jy=(c[1]-a[1])//9
    box=[]
    for y in range(9):
        temp=[]
        for x in range(9):
            ax=a[0]+x*ix+jx*y
            ay=a[1]+x*iy+jy*y
            bx=ax+ix+jx
            by=ay+iy+jy
            temp.append(thresh[ay:by,ax:bx])
        box.append(temp)

    print(box)
    sudo=[]
    for i in range(9):
        temp=[]
        for j in range(9):
            temp.append(ocr(box[i][j]))
        print(ocr(box[i][j]))
        sudo.append(temp)
    new = []
    for i in sudo:
        temp = []
        for j in i :
            if j == ' ':
                temp.append(0)
            else:
                temp.append(j)
        new.append(temp)
    my_array = np.asarray(new)
    
    return my_array

sudo=read_sudo(cv2.imread('sudoku2.jpg'))

def SimpleEncode(ndarray):
    return json.dumps(ndarray.tolist())
def SimpleDecode(jsonDump):
    return np.array(json.loads(jsonDump))

jsonArray =  SimpleEncode(my_array)
print(my_array)

url = "http://localhost:8081/"
myobj = {'board':jsonArray}
x = requests.post(url, data = myobj)

print(x.text)