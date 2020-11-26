import pytesseract
from PIL import Image
from subprocess import check_output

# P A R A M S
img = Image.open('89.jpg')
color_range = 20#частота встечаемости цвета
color_threshold = 15
threshold = 50
threshold_black = 15
threshold_distance = 1#лучше 1 пиксель, с 2мя подает точность, с 3мя и более от символов ничего не остается
colors_final=[]
# P A R A M S
def colors():#определение цвета символов и фона по частоте их встречаемости среди всех пикселей изображения
    colors = {}
    colors2 = []
    for y in range(img.size[1]):#
        for x in range(img.size[0]):
            pixelss = img.load()
            temp = pixelss[x,y]
            if temp in colors:
                colors[temp]=colors[temp]+1
            else:
               colors[temp] = 1

    colors1 = list(colors.items())#упорядочивание
    colors1.sort(key=lambda i: i[1])
    colors1.reverse()

    for i in range(len(colors1)):
        if colors1[i][1] > color_range:
            colors2.append(colors1[i])
    #print(colors2)

    for i in range(len(colors2)):
        if i == 0:
            colors_final.append(colors2[i])
        else:
            n = 0
            if abs(colors2[i][0][0] - colors_final[n][0][0]) > color_threshold and abs(colors2[i][0][1] - colors_final[n][0][1]) > color_threshold and abs(colors2[i][0][2] - colors_final[n][0][2]) > color_threshold:
                colors_final.append(colors2[i])
                break
    print("RGB символов и основного фона на капче распознались как - ",colors_final[0][0]," и ",colors_final[1][0])
colors()#определение границ символов через определение цвета самих символов и цвета фона

def main(needed_index):
    pixels = img.load()
    needeed_pixels = []
    for y in range(img.size[1]):#цикл проверяет все пиксели изображения на соответствие основному цвету линий +-допустимый диапозон threshold
        for x in range(img.size[0]):
            if abs(pixels[x,y][0] - colors_final[needed_index][0][0]) < threshold and abs(pixels[x,y][1] - colors_final[needed_index][0][1]) < threshold and abs(pixels[x,y][2] - colors_final[needed_index][0][2]) < threshold:
                #print(abs(pixels[x,y][0] - needeed[0][0]),abs(pixels[x,y][1] - needeed[0][1]), abs(pixels[x,y][2] - needeed[0][2]))
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = (255, 255, 255)

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

                needeed_pixels.append((x,y))

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (x,y) in needeed_pixels:
                #print('черный пиксель - ',x,y)
                pixels[x,y] = (0, 0, 0)
            else:
                pixels[x,y] = (255, 255, 255)

    if needed_index == 0:
        img.save('final.jpg')
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        myConfig = r'--cem 5 --psm 50'
        captcha = pytesseract.image_to_string(img, lang='eng')
        return captcha
    if needed_index == 1:
        img.save('final1.jpg')
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        myConfig = r'--cem 5 --psm 50'
        captcha = pytesseract.image_to_string(img, lang='eng', config='myConfig')
        return captcha


if len(colors_final)>1:
    answer1 = main(1)
    if len(answer1) >1:
        print("капча распозналась как - ",answer1)#вывод капчи в консоль
    else:
        print("капча не распознана - попытка №2")
        answer0 = main(0)
        if len(answer0) >1:
            print("капча распозналась как - ", answer0)  # вывод капчи в консоль
        else:
            print("капча не распознана")
    with open('captcha.txt','w') as text_file:
        text_file.write(answer1)#текст капчи дополнительно запишем в текстовый файл
else:
    print('символы не распознаны!')
    print('снизьте порог color_range!')
