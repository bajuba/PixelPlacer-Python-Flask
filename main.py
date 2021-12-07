from flask import Flask, render_template, request
from PIL import Image
from random import randint, shuffle
from os import remove, listdir
from re import findall

def cur_pic_num():
  return int(findall("\d+", listdir("static")[1])[0])
app = Flask('app')
# print(listdir("static"))
#get the number from the image
image_number = cur_pic_num()
# print(image_number)
# image_number = 1;



@app.route('/', methods = ['POST', 'GET'])
def home():
  global image_number
  #if the form has not been submitted load the page
  if request.method != 'POST':
    return render_template("index.html",number=image_number)
  #if the form has been submitted create the new image and load the page
  else:
    #getting the info from the form
    x = int(request.form['x'])-1
    y = int(request.form['y'])-1
    color = request.form['color']

    #creating the image
    im = Image.open(f"static/canvas{image_number}.png").convert('RGB')
    image_number = image_number + 1;
    im.load()
    coordinate = (x,y)
    pixel = im.getpixel(coordinate)
    if color == "red":
      pixel = (255,0,0)
    elif color == "green":
      pixel = (0,255,0)
    else:
      pixel = (0,0,255)
    im.putpixel(coordinate, pixel)
    im.save(f"static/canvas{image_number}.png", format=None)
    #saving every 100 pixel changes
    if(cur_pic_num() % 100 == 0):
      im.save(f"static/history/canvas{image_number}.png", format=None)
    #deleting the old image
    remove(f"static/canvas{image_number-1}.png")  
    return render_template("index.html",number=image_number)

@app.route('/history')
def history():
  x = 1
app.run(host='0.0.0.0', port=8080)
