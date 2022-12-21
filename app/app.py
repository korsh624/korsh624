from flask import Flask, render_template
result=''
def readTable():
    
    return 'data'

readTable()
app = Flask(__name__)

name='Имя'
@app.route("/")
def home():
    data=readTable()
    return render_template('index.html')

@app.route("/arduino")
def arduino():
    data=readTable()
    counter=len(data)
    return render_template('arduino.html',data=data, counter=counter)


@app.route("/opencv")
def opencv():
    data=readTable()
    counter=len(data)
    return render_template('opencv.html',data=data, counter=counter)

@app.route("/ros")
def ros():
    data=readTable()
    counter=len(data)
    return render_template('ros.html',data=data, counter=counter)

@app.route("/allinfo")
def allinfo():
    data=readTable()
    counter=len(data)
    return render_template('allinfo.html',data=data, counter=counter)

@app.route("/python")
def python():
    data=readTable()
    counter=len(data)
    return render_template('python.html',data=data, counter=counter)

if __name__=="__main__":
    app.run(debug=True)



