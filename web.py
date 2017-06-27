from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, EqualTo, ValidationError 

app = Flask(__name__,  static_url_path='/static')
app.config.from_object('config')

class InputForm(Form):
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    city = StringField('city', validators=[DataRequired()])

    def validate_city(form, field):
        print "Validate city"
        print form
        print field
	if check_city_name(field.data):
	    return 
        raise ValidationError('You have entered a city that is not in the database')

class InputFormCit(Form):
    city = StringField('name', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])

def check_city_name(data):
    a_file = open("cities","r")
    for line in a_file:
	if line.split(";")[1].lower()==data.lower():
	    return True
    return False


def array_from_file(fileName, lenght):
    file_inst = open(fileName, "r")
    arr= []
    for line in file_inst:
	current = line.split(";")
	if lenght==4 and len(current)==4:
	       arr.append({"id":current[0], "name":current[1], "age":current[2], "city":current[3].strip()})
	if lenght==3 and len(current)==3:
	       arr.append({"id":current[0], "name":current[1], "country":current[2].strip()})
    return arr

def add_to_table(fileName, form, arr):
    result = False
    i=0
    file_inst = open(fileName,"r")
    for line in file_inst:
	curr = line
    file_inst.seek(0)
    id_line = curr.split(";")
    i = int(id_line[0])
    i+=1
    id_inst = i
    file_inst.close()
    if fileName == "cities":
	file_inst = open(fileName,"a")
	c = ";".join([str(id_inst), form.city.data.encode('utf-8'), form.country.data.encode('utf-8').strip()])
	file_inst.write(c + "\r\n")
    if fileName == "people":
	file_inst = open(fileName,"a")
	c = ";".join([str(id_inst), form.name.data.encode('utf-8'), str(form.age.data), form.city.data.encode('utf-8').strip()])
	file_inst.write(c + "\r\n")
    file_inst.close()


@app.route('/cities', methods=['GET', 'POST'])
def cities():
    form = InputFormCit()
    c_arr=[]

    c_arr = array_from_file("cities",3)

    if form.validate_on_submit():
	add_to_table("cities", form, c_arr)

    c_arr = array_from_file("cities",3)

    return render_template('cities.html', c_arr= c_arr, title='Cities',form=form)


    
@app.route('/people', methods=['GET', 'POST'])
def people():
    form = InputForm()
    arr=[]
    cities()
    arr = array_from_file("people", 4)

    if form.validate_on_submit():
	add_to_table("people", form, arr)

    arr = array_from_file("people", 4)

    return render_template('people.html', arr= arr, title='People',form=form)

@app.route('/people/<int:people_id>', methods=['GET'])
def peopleDel(people_id):
    index = 0
    file_inst = open("people","r")
    lines = file_inst.readlines()
    file_inst.close()
    file_inst = open("people","w")
    for line in  lines:
	if int(line.split(";")[0]) != people_id:
	    file_inst.write(line)

    return redirect(url_for('people'))

@app.route('/cities/<int:city_id>', methods=['GET'])
def cityDel(city_id):
    index = 0
    file_inst = open("cities","r")
    lines = file_inst.readlines()
    file_inst.close()
    file_inst = open("cities","w")
    for line in  lines:
	if int(line.split(";")[0]) != city_id:
	    file_inst.write(line)

    return redirect(url_for('cities'))

if __name__ == "__main__":
    app.run()
