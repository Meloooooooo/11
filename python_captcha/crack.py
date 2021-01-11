
#-*- coding:utf8 -*-
from PIL import Image
im = Image.open("captcha.gif")
#(将图片转换为8位像素模式)
im.convert("P")
im2 = Image.new("P", im.size, 255)
#im.histogram()为颜色直方图
his = im.histogram()
values = {}
for i in range(256):
    values[i] = his[i]
for j,k in sorted(values.items(),key = lambda x:x[1],reverse = True)[:10]:
    print(j,k)
print("----------")
print(im.size)

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        if pix == 220 or pix == 227: # these are the numbers to get
            im2.putpixel((y,x),0)
im2.save('new.gif')

inletter = False
foundletter=False
start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter=False
print(letters)

import hashlib
import time

count = 0
for letter in letters:
    # 前两个值为左上角坐标
    # 后两个值为右下角坐标
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    im3.save("./%s.gif"%(count))
    count += 1

import math

class VectorCompare:
    # 计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之间的 cos 值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

# 将图片转换为矢量
def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

import os
# 加载训练集
imageset = []
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})


count = 0
# 对验证码图片进行切割
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))

    guess = []

    # 将切割得到的验证码小片段与每个训练片段进行比较
    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append( ( v.relation(y[0],buildvector(im3)),x) )

    guess.sort(reverse=True)
    print(guess[0])
    count += 1