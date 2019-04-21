from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# CLIENT_ID = json.loads(
#     open('client_secrets.json', 'r').read())['web']['client_id']
# APPLICATION_NAME = "Item Category"


# Connect to Database and create database session
engine = create_engine('sqlite:///categoryitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON APIs to view Category information
@app.route('/categories/JSON')
def showCategoriesJson():
	categories= session.query(Category).all()
	return jsonify(categories=[i.serialize for i in categories])

# route to get the items in a category in JSON format
@app.route('/categories/<int:category_id>/category_item/JSON')
def categoryItemsJson(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	category_items = session.query(categoryItem).filter_by(
		category_id=category_id).all()
	return jsonify(categoryItems=[i.serialize for i in category_items])    

# route to get all categories
@app.route('/')
@app.route('/categories')
def showCategories():
	categories = session.query(Category).all()
	return render_template('publicCategory.html', categories=categories)

# create a new category
@app.route('/category/new', methods=['GET', 'POST'])
def newCategory():
	if request.method == 'POST':
		newCategory = Category(name=request.form['name'],
		 description=request.form['description'])
		session.add(newCategory)
		flash('New Category %s Successfully Created' % newCategory.name)
		session.commit()
		return redirect(url_for('showCategories'))
	else:
		return render_template('newCategory.html')

# edit an existing category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
	editedCategory = session.query(
		Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedCategory.name = request.form['name']
			flash('Category Successfully Edited %s' % editedCategory.name)
			return redirect(url_for('showCategories'))
	else:
		return render_template('editCategory.html', category=editedCategory)

# delete an existing category
@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
	categoryToDelete = session.query(
		Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		session.delete(categoryToDelete)
		flash('%s Successfully Deleted' % categoryToDelete.name)
		session.commit()
		return redirect(url_for('showCategories', category_id=category_id))
	else:
		return render_template('deleteCategory.html', category=categoryToDelete)


# route to get category items in a particular category
@app.route('/category/<int:category_id>/')
@app.route('/categories/<int:category_id>/category_item')
def showCategoryItems(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	categoryItems = session.query(CategoryItem).filter_by(
		category_id=category_id).all()
	return render_template(
		'publicCategoryItem.html', category=category, category_items=categoryItems, category_id=category_id)


# route to create a new category item
@app.route('/category/<int:category_id>/category_item/new/', methods=['GET', 'POST'])
def newCategoryItem(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
			newCategoryItem = CategoryItem(name=request.form['name'], description=request.form['description'], price=request.form[
							   'price'], category_id=category_id)
			session.add(newItem)
			session.commit()
			flash('New Category %s Item Successfully Created' % (newItem.name))
			return redirect(url_for('showCategoryItems', category_id=category_id))
	else:
		return render_template('newCategoryItem.html', category_id=category_id)

# route to edit a category item
@app.route('/category/<int:category_id>/<int:category_item_id>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_id, category_item_id):
	editedItem = session.query(CategoryItem).filter_by(id=category_item_id).one()
	category = session.query(Category).filter_by(id=category_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		if request.form['description']:
			editedItem.description = request.form['description']
		if request.form['price']:
			editedItem.price = request.form['price']
		if request.form['course']:
			editedItem.course = request.form['course']
		session.add(editedItem)
		session.commit()
		flash('Item Successfully Edited')
		return redirect(url_for('showCategoryItems', category_id=category_id))
	else:
		return render_template('editCategoryItem.html', category_id=category_id, item=editedItem)



@app.route('/categories/<int:category_id>/<int:category_item_id>/delete/',
		   methods=['GET', 'POST'])
def deleteCategoryItem(category_id, category_item_id):
	deletedItem = session.query(CategoryItem).filter_by(id=category_item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			deletedItem.name = request.form['name']
		session.delete(deletedItem)
		session.commit()
		flash("Category Item has been deleted!")

		return redirect(url_for('category', category_id=category_id))
	else:
		# USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
		# SHOULD USE IN YOUR EDITITEM TEMPLATE
		return render_template(
			'deletedCategoryItem.html', category_id=category_id, category_item_id=category_item_id, item=deletedItem)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)