from PIL import Image
import hashlib
import os
import math

#用python来实现向量空间
class VectorCompare:
    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)
    #计算矢量之间的值
    def relation(self,concordance1, concordance2):

        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        #返回cos值     相似值除两矢量之积
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))


#将图像转变为矢量
def buildvector(im):
    d1 = {}

    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1

    return d1

把类变成实例
v = VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

imageset = []
#letter在此可理解为文件夹
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store": # windows check...
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        #得出训练集中每个图片的像素集，以字典形式打印
        imageset.append({letter:temp})


im = Image.open("captcha.gif")
#生成一个于im大小一样、空白的的图片
im2 = Image.new("P",im.size,255)
#把im转换成8位像素模式
im.convert("P")
temp = {}

#给im2加上指定值的像素，得到im2（即黑白的im）
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix = im.getpixel((y,x))
        temp[pix] = pix
        if pix == 220 or pix == 227: # these are the numbers to get
            im2.putpixel((y,x),0)

#提取单个字符图片
inletter = False
foundletter=False
start = 0
end = 0

letters = []
#遍历黑白图片im2
for y in range(im2.size[0]): # slice across
    for x in range(im2.size[1]): # slice down
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

count = 0
for letter in letters:
    m = hashlib.md5()
    #此处采用PIL的crop函数来裁剪单个字符
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
    guess = []

    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append( ( v.relation(y[0],buildvector(im3)),x) )

    guess.sort(reverse=True)
    print (guess[0])

    count += 1