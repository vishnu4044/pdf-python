from wand.image import Image as wi
from PIL import Image
import shutil, os
import random
import img2pdf
from uuid import uuid4

from flask import Flask, request, render_template, send_from_directory,send_file


app = Flask(__name__)
# app = Flask(__name__, static_folder="images")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("flask.html")

@app.route("/upload", methods=["POST"])
def upload():
    nrt = random.randint(1, 10000000000000)
    nrt2 = str(nrt)
    nrt3 = nrt2 + "fld/"
    i = 0
    folder = 'C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except :
            pass
    n=request.form['id']
    if os.path.exists('C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt3+'/comp.pdf'):
        os.remove('C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt3+'/comp.pdf')
    else:
        os.mkdir('C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt3)
    target = os.path.join(APP_ROOT,"fld/"+nrt2)
    # target = os.path.join(APP_ROOT, 'static/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename ="comp.pdf"
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
        os.chdir('C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt2)
        pdf = wi(filename=filename, resolution=100)
        pdfimage = pdf.convert("jpeg")
    for img in pdfimage.sequence:
        page = wi(image=img)
        page.save(filename=str(i) + ".jpg")
        print(str(i) + ".jpg")
        path = str(i) + ".jpg"
        gh = Image.open(path)
        if n=="sai":
            gh.save(str(i) + ".jpg", quality=80)
            i += 1
        elif n=="sai2":
            gh.save(str(i) + ".jpg", quality=70)
            i += 1
        elif n=="sai3":
            gh.save(str(i) + ".jpg", quality=50)
            i += 1
    with open("comp.pdf", "wb") as f:
            f.write(img2pdf.convert([i for i in os.listdir(
                'C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt2) if
                                     i.endswith(".jpg")]))
            f.close()
            files = ['comp.pdf']
            for f in files:
                shutil.move(f, 'C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt3)
                ht=open('C:/Users/vishnu sai/Desktop/my projectes/pdf/store.txt','w')
                ht.write(nrt2)
                ht.close()
            return render_template("pass.html", name=filename)

@app.route('/upload')
def send_image():
    ht=open('C:/Users/vishnu sai/Desktop/my projectes/pdf/store.txt','r')
    nrt2=ht.read()
    ht.close
    nrt3 = nrt2 + "fld/"
    path ="C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/"+nrt3+"/comp.pdf"
    try:
        shutil.rmtree('C:/Users/vishnu sai/Desktop/my projectes/pdf/fld/'+nrt2)
    except:
        pass
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(port=4555, debug=True)