from PIL import Image, ImageDraw
import math

read_text = open("coke_22.txt")
text_line = read_text.readline()
text_words = text_line.split()
cx = float(text_words[1])
cy = float(text_words[2])
width = float(text_words[3])
height = float(text_words[4])
xy = [int((cx - width/2)*640), int((cy - height/2)*480), int((cx+width/2)*640), int((cy+height/2)*480)]

background = Image.open("coke_22.png")
background1 = ImageDraw.Draw(background)
background1.rectangle(xy, outline = "green")
##background.show()

background2 = Image.open("coke_22.png")
paste_point = (-xy[0] + 20, -xy[1] + 20)
background.paste(background2, paste_point, background2)


fix_box =[]
fix_box.append(float(20)/640)
fix_box.append(float(20)/480)
print(fix_box)
xy2 = [int((fix_box[0])*640), int((fix_box[1])*480), int((fix_box[0]+width)*640), int((fix_box[1]+height)*480)]

background1.rectangle(xy2, outline = "green")
background.show()
