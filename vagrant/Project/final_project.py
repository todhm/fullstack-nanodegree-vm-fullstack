from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import re
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def totalrestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html',items = restaurants)


@app.route('/restaurants/new/',methods = ['GET','POST'])
def newrestaurant():
    if request.method == 'POST':
        restaurant_name = request.form.get('name')
        newrestaurant = Restaurant(name = restaurant_name)
        session.add(newrestaurant)
        flash("New Restaurant added")
        session.commit()
        return redirect(url_for('totalrestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/',methods = ['GET','POST'])
def editrestaurant(restaurant_id):
    item = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        new_name = request.form.get('name')
        item.name= new_name
        session.commit()
        flash("The name of restaurant have been changed")
        return redirect(url_for('totalrestaurants'))
    return render_template('editrestaurant.html',restaurant_id = restaurant_id,item = item)

@app.route('/restaurants/<int:restaurant_id>/delete/',methods = ['GET','POST'])
def deleterestaurant(restaurant_id):
    item = session.query(Restaurant).filter_by(id = restaurant_id).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('totalrestaurants'))
    return render_template('deleterestaurant.html',item = item )


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/new/',methods = ['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        print request.form['price']
        newItem = MenuItem(name=request.form['name'],description = request.form['description'],
                            price = request.form['price'],course = request.form['course'],
                            restaurant_id = restaurant_id)
        session.add(newItem)
        flash("New menu item added")
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))

    return render_template('newmenuitem.html',restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        item.name = request.form['name']
        session.commit()
        flash("Changed menu name")
        return redirect(url_for('restaurantMenu',restaurant_id = item.restaurant_id))

    else:
        return render_template('editmenuitem.html',restaurant_id= restaurant_id, menu_id = menu_id,item = item)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',methods =['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.query(MenuItem).filter_by(id = menu_id).delete()
        session.commit()
        flash("Delete name of the menu")
        return redirect(url_for('restaurantMenu',restaurant_id = restaurant_id))
    else:
        return  render_template('deletemenuitem.html',restaurant_id= restaurant_id, menu_id = menu_id,item = item)

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant = [ x.serialize for x in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id =restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def getmenuJSON(restaurant_id,menu_id):
    items = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = items.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
