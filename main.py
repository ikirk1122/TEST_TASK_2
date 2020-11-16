import pytesseract
from PIL import Image
from subprocess import check_output


img = Image.open('test3.jpg')
img2 = Image.open('test6.jpg')
#img = Image.open('captcha.gif')
#img = Image.open('captcha2.png')
#img = Image.open('text.png')


pixels = img.load()
#for i in range(0,100):
    #for j in range (0,100):
        #print(pixels[i,j])
needeed = [(251, 130, 225)]#test3.jpg needed color
#needeed = [(12, 39, 0)]#test.jpg needed color

threshold = 50
threshold_black = 15
threshold_distance = 1#лучше 1 пиксель, с 2мя подает точность, с 3мя и более от символов ничего не остается
needeed_pixels=[]
for y in range(img.size[1]):#цикл проверяет все пиксели изображения на соответствие основному цвету линий +-допустимый диапозон threshold
    for x in range(img.size[0]):
        if abs(pixels[x,y][0] - needeed[0][0]) < threshold and abs(pixels[x,y][1] - needeed[0][1]) < threshold and abs(pixels[x,y][2] - needeed[0][2]) < threshold:
            #print(abs(pixels[x,y][0] - needeed[0][0]),abs(pixels[x,y][1] - needeed[0][1]), abs(pixels[x,y][2] - needeed[0][2]))

            pixels[x,y] = (0, 0, 0)
        else:
            pixels[x,y] = (255, 255, 255)
#print(img)
for y in range(img.size[1]-threshold_distance):#компенсация выхода за пределы изображения
    for x in range(img.size[0]-threshold_distance):#цикл проверяет соседние пиксели с целью устранения шумов и лишних линий, которые мешают тессеракту рапознать текст
        if pixels[x,y][0] < threshold_black and pixels[x,y][1] < threshold_black and pixels[x,y][2] < threshold_black and\
                pixels[abs(x+threshold_distance),abs(y+threshold_distance)][0] < threshold_black and pixels[abs(x+threshold_distance),abs(y+threshold_distance)][1] < threshold_black and pixels[abs(x+threshold_distance),abs(y+threshold_distance)][2] < threshold_black and\
                pixels[abs(x-threshold_distance),abs(y-threshold_distance)][0] < threshold_black and pixels[abs(x-threshold_distance),abs(y-threshold_distance)][1] < threshold_black and pixels[abs(x-threshold_distance),abs(y-threshold_distance)][2] < threshold_black and\
                pixels[abs(x+threshold_distance),abs(y-threshold_distance)][0] < threshold_black and pixels[abs(x+threshold_distance),abs(y-threshold_distance)][1] < threshold_black and pixels[abs(x+threshold_distance),abs(y-threshold_distance)][2] < threshold_black and\
                pixels[abs(x-threshold_distance),abs(y+threshold_distance)][0] < threshold_black and pixels[abs(x-threshold_distance),abs(y+threshold_distance)][1] < threshold_black and pixels[abs(x-threshold_distance),abs(y+threshold_distance)][2] < threshold_black and\
                pixels[abs(x+threshold_distance),y][0] < threshold_black and pixels[abs(x+threshold_distance),y][1] < threshold_black and pixels[abs(x+threshold_distance),y][2] < threshold_black and\
                pixels[abs(x-threshold_distance),y][0] < threshold_black and pixels[abs(x-threshold_distance),y][1] < threshold_black and pixels[abs(x-threshold_distance),y][2] < threshold_black and\
                pixels[x,abs(y-threshold_distance)][0] < threshold_black and pixels[x,abs(y-threshold_distance)][1] < threshold_black and pixels[x,abs(y-threshold_distance)][2] < threshold_black and\
                pixels[x,abs(y+threshold_distance)][0] < threshold_black and pixels[x,abs(y+threshold_distance)][1] < threshold_black and pixels[x,abs(y+threshold_distance)][2] < threshold_black:#выше идут проверки соседних пикселей на соответствие +-черному цвету по 8 направлениям (право вверх ,влево вниз и т.д.)
            #print(x,y)
            needeed_pixels.append((x,y))
            #pixels[x,y] = (0, 0, 0)
       # else:
            #print('else')
          #  pixels[x,y] = (255, 255, 255)

print(needeed_pixels)

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if (x,y) in needeed_pixels:
            print(x,y)
            pixels[x,y] = (0, 0, 0)
        else:
            pixels[x,y] = (255, 255, 255)



img.save('final.jpg')
#with open('img2.jpg','w') as text_file:
    #text_file.write(img)


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


myConfig = r'--cem 5 --psm 50'

captcha = pytesseract.image_to_string(img, lang='eng')
print(captcha)

with open('captcha.txt','w') as text_file:
    text_file.write(captcha)