

from flask import Flask, render_template, request
from random import random
import numpy
import cv2
import os
from datetime import datetime
from zipfile import ZipFile

app = Flask(__name__)
name_list = []


@app.route("/")
def teti_lessons():
    return render_template("teti_victor.html")


@app.route("/index")
def data_manipulation():
    students_list = ["victor", "caio", "dudu", "luis", "Alexandre"]
    return render_template("index.html", students_list=students_list)


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    if request.method == "POST":
        name = request.form.get('Name')
        return render_template("cadastro.html", name=name)


@app.route("/list", methods=["GET"])
def list():
    if request.method == "GET":
        name_list.clear()
        return render_template("list.html")


@app.route("/add-name", methods=["POST"])
def add_name():
    if request.method == "POST":
        name = request.form.get('Name')
        name_list.append(name)
        return render_template("list.html", name_list=name_list)


@app.route("/calculator", methods=["GET", "POST"])
def simple_calculator():
    if request.method == "GET":
        return render_template("calculator.html")
    if request.method == "POST":
        expression = request.form.get('expression')
        expression = expression.replace(
            '÷', '/').replace('𝗑', '*').replace(',', '.')
        try:
            result = eval(expression)
            binnary = bin(int(result)).removeprefix('0b')
            mensage = None
        except:
            mensage = 'Comando Inválido !'
            result = binnary = None
        return render_template("calculator.html", result=result, binnary=binnary, mensage=mensage)


@app.route("/alfa-calc",
           methods=["GET", "POST"])
def alphanum_calculator():
    if request.method == "GET":
        return render_template("alfa_calc.html")
    if request.method == "POST":
        expression = request.form.get('expression')
        try:
            binnary = ''.join(format(ord(caractere), '08b')
                              for caractere in expression)
            size = len(binnary)
            separator = 480
            array_2d = [[binnary[n:n + separator]]
                for n in range(0, size, separator) if n < size]
            mensage = False
        except: 
            mensage = True
            binnary = None
        return render_template("alfa_calc.html", binnary=array_2d, mensage=mensage)


@app.route("/div")
def array_divs_1_pixel():
    return render_template("div.html")


@app.route("/div_colored")
def array_divs_1_pixel_colored():
    def row(): return [
            f'#{round(random() * 0xffffff):06X}' for _ in range(512)]
    col = [row() for _ in range(512)]
    return render_template("div_colored.html", colors=col)


@app.route("/galeria", methods=["GET", "POST"])
def myGaleria():

    path_prefix = './' if os.path.exists('./static') else 'teti_victor/'
    path = f'{path_prefix}static/images/galeria'

    if request.method == "GET":
        for nick_img in os.listdir(path):
            os.remove(f'{path}/{nick_img}')
        return render_template("galeria.html")

    if request.method == "POST":

        try:
            buffer_file = request.files['input-file-image']

            bytes_array = numpy.frombuffer(buffer_file.read(), numpy.uint8)

            image: numpy.ndarray = cv2.imdecode(bytes_array, cv2.IMREAD_COLOR)

            cv2.imwrite(f'{path}/image_{datetime.now()}.jpg', image)

            if os.path.exists(f'{path}/imagespy.zip'):
                os.remove(f'{path}/imagespy.zip')

            with ZipFile(f'{path}/imagespy.zip', 'w') as zip_obj:
                images_list = os.listdir(path)
                images_list.remove('imagespy.zip')
                for nick_img in images_list:
                    zip_obj.write(f'{path}/{nick_img}')

            images_list = os.listdir(path)
            images_list.remove('imagespy.zip')
            return render_template("galeria.html", images_list=images_list, zip_file_exists=True)
        except:
            return render_template("galeria.html")


@app.route("/transferencia", methods=["GET", "POST"])
def transferencia_px():
    if request.method == "GET":
        return render_template("transferenciapx.html")
    if request.method == "POST":
        try:
            buffer_file = request.files['input-file-image']

            bytes_array = numpy.frombuffer(buffer_file.read(), numpy.uint8)

            image: numpy.ndarray = cv2.imdecode(bytes_array, cv2.IMREAD_COLOR)

            def rgb_to_hex(row): return [
                           f'#{pixel[2]:02X}{pixel[1]:02X}{pixel[0]:02X}' for pixel in row]

            matriz = [rgb_to_hex(row) for row in image]

            return render_template("transferenciapx.html", image=matriz)
        except:
            return render_template("transferenciapx.html")


@app.route("/funcao-imagem", methods=["GET", "POST"])
def rotacao_imagem():
       if request.method == "GET":
            return render_template("funcao_imagem.html")
       if request.method == "POST":
            try:

                dist = ((x1-x2) **2 + (y1 - y2)**2) **0.5
                print("TESTE", dist)
                
                return render_template("funcao_imagem.html")

            except:
                print("TESTE 02")
                return render_template("funcao_imagem.html")

if __name__ == '__main__':
    app.run(debug= True)
