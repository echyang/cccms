#!/usr/bin/env python
#coding=utf-8
import sys
from flask import render_template, url_for, request, flash, redirect, jsonify, g, session
from flask import Markup
from werkzeug import secure_filename
from app import app
from app import db
from datetime import datetime
import models
from functools import wraps
from sqlalchemy import or_, and_

reload(sys)
sys.setdefaultencoding('utf-8')

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not session.get('user_id'):
			return redirect(url_for('login')) 
		return f(*args, **kwargs)
	return decorated_function
		
def category_common(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		categories = models.Category.query.order_by('lft ASC ').all()
		if not categories:
			lft = 1
			rgt = 2
			layer = 0
			title = 'ROOT'
			keywords = ''
			description = ''
			picture = ''
			content = ''
			category_add = models.Category(lft, rgt, layer, title, keywords,  description, picture, content)		
			db.session.add(category_add)
			db.session.commit()
		return f(*args, **kwargs)
	return decorated_function


def get_categories():
	return models.Category.query.filter(models.Category.layer>0).order_by('lft ASC ').all()


@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')


# Upload file function
# ext_type = ['image', 'office', 'file']
# return_type = ['json', 'text', 'html']
@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload/<ext_type>', methods=['GET', 'POST'])
@app.route('/upload/<ext_type>/<return_type>', methods=['GET', 'POST'])
@app.route('/upload/<ext_type>/<return_type>/<field>', methods=['GET', 'POST'])
@login_required
def upload(ext_type='image', return_type='json', field='file_upload'):
	data = {'stat':False}
	if request.method == 'POST' and field in request.files:
		f = request.files[field]
		extension = f.filename.split('.')[-1].lower()
		data['old_filename']=f.filename
		data['extension'] = extension
		extension = f.filename.split('.')[-1]
		if extension in app.config[('upload_'+ext_type).upper()]:	
			file_name = secure_filename(f.filename)
			if len(file_name)<=3 :
				filename = datetime.now()+"."+extension
			f.save('./app/static/upload/' + file_name)
			data['stat'] = True
			data['url'] = '/static/upload/'+file_name 
			data['filename']=file_name
			data['upload_time'] = datetime.utcnow()
		else: 
			data['msg'] = '不允许上传此类文件'
		return jsonify(data)
	else:
		data['msg'] = '上传文件不存在'
	#return jsonify(data)
	return render_template('upload.html')


@app.route('/group')
@login_required
def group():
	setting = {'url':'group'}
	groups = models.Group.query.order_by('create_at ASC').all()
	return render_template('group_list.html', setting=setting, groups=groups)


@app.route('/group/add', methods=['GET', 'POST'])
@login_required
def group_add():
	setting = {'url':'group'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Group.query.filter_by(name=request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			group_add = models.Group(request.form['name'], request.form['description'])		
			db.session.add(group_add)
			db.session.commit()
			flash('添加用户组"%s"成功' % request.form['name'])
			return redirect(url_for('group'))
		
	return render_template('group_add.html', setting=setting, error=error)


@app.route('/group/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def group_edit(id=0):
	setting = {'url':'group'}
	error = {} 
	group = models.Group.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Group.query.filter(models.Group.id!=id).filter(models.Group.name==request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			group.name = request.form['name']
			group.description = request.form['description']
			group.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改用户组"%s"成功' % group.name)
			return redirect(url_for('group'))
		
	return render_template('group_edit.html', setting=setting, error=error, group=group)


@app.route('/group/delete/<int:id>')
@login_required
def group_delete(id=0):
	group = models.Group.query.get_or_404(id)
	flash('删除用户组"%s"成功' % group.name)
	db.session.delete(group)
	db.session.commit()
	return redirect(url_for('group'))


@app.route('/user')
@app.route('/user/page/<int:page>')
@login_required
def user(page=1):	
	setting = {'url':'user'}
	pagination = models.User.query.paginate(page, app.config['PAGINATION'])
	users = models.User.query.order_by('create_at DESC').offset((pagination.page-1)*app.config['PAGINATION']).limit(app.config['PAGINATION']).all()
	return render_template('user_list.html', setting=setting, users=users, pagination=pagination)


@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
	setting = {'url':'user'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['username']:
			error['username'] = ['用户名不能为空']
			stat = False
		elif models.User.query.filter_by(username=request.form['username']).first():
			error['username'] = ['用户名已经存在']
			stat = False
		if not request.form['email']:
			error['email'] = ['邮箱地址不能为空']
			stat = False
		if not request.form['password']:
			error['password'] = ['密码不能为空']
			stat = False
		if not request.form['password_confirm']:
			error['password_confirm'] = ['重复密码不能为空']
			stat = False
		if request.form['password']<>request.form['password_confirm']:
			error['password_confirm'] = ['两次密码不一致']
			stat = False
		if stat:
			group = models.Group.query.get(request.form['group_id'])
			user_add = models.User(group, request.form['username'], request.form['email'], request.form['password'], request.form['is_active'])
			db.session.add(user_add)
			db.session.commit()
			flash('添加用户"%s"成功' % request.form['username'])
			return redirect(url_for('user'))
		
	groups = models.Group.query.order_by('create_at ASC').all()
	return render_template('user_add.html', setting=setting, error=error, groups=groups)


@app.route('/user/<int:id>')
@login_required
def user_detail(id=0):
	setting = {'url':'user'}
	user = models.User.query.get(id)
	return render_template('user_detail.html', setting=setting, user=user)


@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def user_edit(id=0):
	setting = {'url':'user'}
	error = {} 
	user = models.User.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['username']:
			error['username'] = ['用户名不能为空']
			stat = False
		elif models.User.query.filter(models.User.id!=id).filter_by(username=request.form['username']).first():
			error['name'] = ['用户名已经存在,请使用其他用户名']
			stat = False
		if not request.form['email']:
			error['email'] = ['邮箱不能为空']
			stat = False
		elif models.User.query.filter(models.User.id!=id).filter_by(email=request.form['email']).first():
			error['name'] = ['邮箱已经注册过，请使用其他邮箱']
			stat = False
		if request.form['password_old']:
			if not request.form['password']:
				error['password'] = ['新密码不能为空']
				stat = False
			if not request.form['password_confirm']:
				error['password_confirm'] = ['重复新密码不能为空']
				stat = False
			if request.form['password']<>request.form['password_confirm']:
				error['password_confirm'] = ['两次新密码不一致']
				stat = False
		if stat:
			group = models.Group.query.get(request.form['group_id'])
			user.group = group
			user.username = request.form['username']
			if request.form['password_old']==user.password and request.form['password']: 
				user.password = request.form['password']
			user.email = request.form['email']
			user.is_active = request.form['is_active']
			user.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改用户"%s"成功' % user.username)
			return redirect(url_for('user'))
	groups = models.Group.query.order_by('create_at ASC').all()
	return render_template('user_edit.html', setting=setting, error=error, groups=groups, user=user)


@app.route('/user/delete/<int:id>')
@login_required
def user_delete(id=0):
	user = models.User.query.get_or_404(id)
	flash('删除用户"%s"成功' % user.username)
	db.session.delete(user)
	db.session.commit()
	return redirect(url_for('user'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user_id' in session:
		return redirect(url_for('/login/success')) 
	if request.method == 'POST':
		if request.form['username'] and request.form['password']:
			user = models.User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
			if user:
				user.update_at = datetime.utcnow()
				db.session.add(user)
				db.session.commit()
				session['user_id'] = user.id
				session['username'] = user.username
				session['group_id'] = user.group.id
				session['group_name'] = user.group.name
				return redirect(url_for('login_success'))
			else:
				flash('用户名或密码不正确,请重新登录!')

	return render_template('login.html')


@app.route('/login/success')
def login_success():
	if not 'user_id' in session:
		return redirect(url_for('login')) 
	user = models.User.query.get(session['user_id'])
	return render_template('login_success.html', user=user)


@app.route('/logout')
@login_required
def logout():
	session.pop('user_id', None)
	session.pop('username', None)
	session.pop('group_id', None)
	session.pop('group_name', None)
	return render_template('logout.html')

@app.route('/password', methods=['GET','POST',])
@login_required
def password():
	setting = {'url':'password'}
	error = {} 
	user = models.User.query.get(session['user_id'])

	if request.method == 'POST':
		stat = True
		if not request.form['password_old']:
			error['password_old'] = '旧密码不能为空'
			stat = False
		if not request.form['password']:
			error['password'] = '新密码不能为空'
			stat = False
		if not request.form['password_confirm']:
			error['password_confirm'] = '重复新密码不能为空'
			stat = False
		if request.form['password']<>request.form['password_confirm']:
			error['password_confirm'] = '两次新密码不一致'
			stat = False
		if request.form['password_old'] <> user.password:
			error['password_old'] = '旧密码输入错误'
			stat = False
		if stat:
			user.password = request.form['password']
			user.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改%s密码成功' % user.username)
			return redirect(url_for('password'))
	return render_template('password_change.html', setting=setting, error=error, user=user)

@app.route('/config', methods=['GET','POST'])
@login_required
def config():
	config = models.Config.query.limit(1).first()	
	if not config:
		config = models.Config('', '', '', '', '', '', '', '', '') 
		db.session.add(config)
		db.session.commit()
	error = []
	if request.method == 'POST':
		config.sitename = request.form['sitename']
		config.keywords = request.form['keywords']
		config.description = request.form['description']
		config.domain = request.form['domain']
		config.company = request.form['company']
		config.company_site = request.form['company_site']
		config.linkman = request.form['linkman']
		config.tel = request.form['tel']
		config.icp = request.form['icp']
		config.update_at = datetime.utcnow()
		db.session.commit()
		flash('修改"站点设置"成功')
		return redirect(url_for('config'))
	return render_template('config.html', config=config, error=error)

@app.route('/category')
@login_required
@category_common
def category():
	setting = {'url':'category'}
	categories = models.Category.query.filter(models.Category.layer>0).order_by('lft ASC ').all()
	return render_template('category_list.html', setting=setting, categories=categories)


@app.route('/category/add', methods=['GET', 'POST'])
@login_required
@category_common
def category_add():
	setting = {'url':'category'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['名称不能为空']
			stat = False
		elif models.Category.query.filter_by(title=request.form['title']).first():
			error['title'] = ['分类名称已经存在.']
			stat = False
		if stat:
			o_row = models.Category.query.get(request.form['parent_id'])
			pos = 0
			lft = 0
			rgt = 0
			layer = 0
			if o_row:
				if request.form['pos'] == 'first_child':
					lft = o_row.lft+1
					rgt = o_row.lft+2
					layer = o_row.layer+1
					pos = o_row.lft
				elif request.form['pos'] == 'last_child':
					lft = o_row.rgt
					rgt = o_row.rgt+1
					layer = o_row.layer+1
					pos = o_row.rgt-1
				elif request.form['pos'] == 'previous_sibling':
					lft = o_row.lft
					rgt = o_row.lft+1
					layer = o_row.layer
					pos = o_row.lft-1
				elif request.form['pos'] == 'next_sibling':
					lft = o_row.rgt+1
					rgt = o_row.rgt+2
					layer = o_row.layer
					pos = o_row.rgt

			if lft and rgt and layer:
				models.Category.query.filter(models.Category.lft>pos).update({models.Category.lft:models.Category.lft+2})
				models.Category.query.filter(models.Category.rgt>pos).update({models.Category.rgt:models.Category.rgt+2})
				db.session.commit()

				data_model = models.Data_model.query.get(request.form['data_model_id'])
				category = models.Category(lft, rgt, layer, request.form['title'], data_model, request.form['keywords'], request.form['description'], '', '')		
				db.session.add(category)
				db.session.commit()

				flash('添加分类"%s"成功' % request.form['title'])
				return redirect(url_for('category'))
		
	categories = models.Category.query.order_by('lft ASC').all()
	data_model = models.Data_model.query.order_by('id ASC').all()
	return render_template('category_add.html', setting=setting, categories=categories, data_model=data_model, error=error)


@app.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def category_edit(id=0):
	setting = {'url':'category'}
	error = {} 
	category = models.Category.query.get_or_404(id)
	o_row = models.Category.query.filter(or_(models.Category.lft==category.lft-1, models.Category.rgt==category.lft-1)).first()
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['分类名称不能为空']
			stat = False
		elif models.Category.query.filter(models.Category.id!=id).filter_by(title=request.form['title']).first():
			error['title'] = ['分类名称已经存在']
			stat = False
		else:
			b_parent = False 
			p_row = models.Category.query.filter(or_(models.Category.lft==category.rgt+1, models.Category.rgt==category.rgt+1)).first()
			n_row = models.Category.query.get(request.form['parent_id'])
			if request.form['pos'] == 'first_child':
				if o_row.layer == n_row.layer and n_row.id==o_row.id:	
					b_parent = True
			elif request.form['pos'] == 'last_child':
				if p_row.layer == n_row.layer and n_row.id==p_row.id:	
					b_parent = True
			elif request.form['pos'] == 'previous_sibling':
				if p_row.layer == n_row.layer and n_row.id == p_row.id:	
					b_parent = True
			elif request.form['pos'] == 'next_sibling':
				if o_row.layer == n_row.layer and n_row.id == o_row.id:	
					b_parent = True
			if b_parent:
				stat = False
				error['title'] = ['记录位置没有改变']
		if stat:
			lft = category.lft
			rgt = category.rgt
			layer = category.layer
			#伪删除
			models.Category.query.filter(and_(models.Category.lft>=lft, models.Category.rgt<=rgt)).update({models.Category.lft:models.Category.lft-rgt-1, models.Category.rgt:models.Category.rgt-rgt-1})
			models.Category.query.filter(models.Category.lft>rgt).update({models.Category.lft:models.Category.lft-(rgt-lft+1)})
			models.Category.query.filter(models.Category.rgt>rgt).update({models.Category.rgt:models.Category.rgt-(rgt-lft+1)})
			#开辟新位置
			if request.form['pos'] == 'first_child':
				o_pos = n_row.lft
				o_layer = n_row.layer+1
			elif request.form['pos'] == 'last_child':
				o_pos = n_row.rgt-1
				o_layer = n_row.layer+1
			elif request.form['pos'] == 'previous_sibling':
				o_pos = n_row.lft-1
				o_layer = n_row.layer
			elif request.form['pos'] == 'next_sibling':
				o_pos = n_row.rgt
				o_layer = n_row.layer
			models.Category.query.filter(models.Category.lft>o_pos).update({models.Category.lft:models.Category.lft+(rgt-lft+1)})
			models.Category.query.filter(models.Category.rgt>o_pos).update({models.Category.rgt:models.Category.rgt+(rgt-lft+1)})
			#移动到新的位置
			models.Category.query.filter(and_(models.Category.lft<0, models.Category.rgt<0)).update({models.Category.lft:models.Category.lft+rgt-lft+2+o_pos, models.Category.rgt:models.Category.rgt+rgt-lft+2+o_pos, models.Category.layer:models.Category.layer+o_layer-layer})
		#更新
		data_model = models.Data_model.query.get(request.form['data_model_id'])
		category.title = request.form['title']
		category.data_model = models.Data_model.query.get(request.form['data_model_id'])
		category.keywords = request.form['keywords']
		category.description = request.form['description']
		#category.picture = request.form['picture']
		#category.content = request.form['content']
		category.update_at = datetime.utcnow()
		db.session.commit()
		flash('修改分类"%s"成功' % request.form['title'])
		return redirect(url_for('category'))
	
	categories = models.Category.query.filter(or_(models.Category.lft<category.lft, models.Category.rgt>category.rgt)).order_by('lft ASC').all()
	data_model = models.Data_model.query.order_by('id ASC').all()
	return render_template('category_edit.html', setting=setting, error=error, category=category, categories=categories, data_model=data_model, o_row=o_row)


@app.route('/category/delete/<int:id>')
@login_required
def category_delete(id=0):
	category = models.Category.query.get_or_404(id)
	lft = category.lft
	rgt = category.rgt
	models.Category.query.filter(and_(models.Category.lft>=lft, models.Category.rgt<=rgt)).delete()
	models.Category.query.filter(models.Category.lft>rgt).update({models.Category.lft:models.Category.lft-(rgt-lft+1)})
	models.Category.query.filter(models.Category.rgt>rgt).update({models.Category.rgt:models.Category.rgt-(rgt-lft+1)})
	db.session.commit()
	flash('删除分类"%s"成功' % category.title)
	return redirect(url_for('category'))


@app.route('/admin/content')
def content():
	setting = {}
	setting['categories'] = get_categories()	
	return render_template('content.html', setting=setting)

@app.route('/article', methods=['GET',])
@app.route('/article/page/<int:page>', methods=['GET',])
@app.route('/article/category/<int:category_id>', methods=['GET',])
@app.route('/article/category/int:category_id>/page/<int:page>', methods=['GET',])
@login_required
def article(page=1, category_id=0):	
	setting = {'url':'article'}
	setting['categories'] = get_categories()	
	#Search Form
	search = {'category_id':int(request.args.get('category_id', '') or '0'), 'title':request.args.get('title', ''),}
	url_get = '?category_id='+str(search['category_id'])+'&title='+search['title']
	categories = models.Category.query.all()
	search_list = []
	if search['category_id'] and int(search['category_id']) :
		search_list.append(models.Article.category_id==search['category_id'])
	if search['title']:
		search_list.append(models.Article.title.like('%'+search['title']+'%'))
	pagination = models.Article.query.filter(*search_list).paginate(page, app.config['PAGINATION'])
	articles = models.Article.query.filter(*search_list).order_by('create_at DESC').offset((pagination.page-1)*app.config['PAGINATION']).limit(app.config['PAGINATION']).all()

	setting['categories'] = get_categories()
	return render_template('article_list.html', setting=setting, articles=articles, pagination=pagination, categories=categories, search=search, url_get=url_get)


@app.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
	setting = {'url':'article'}
	setting['categories'] = get_categories()	
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['标题不能为空']
			stat = False
		elif models.Article.query.filter_by(title=request.form['title']).first():
			error['title'] = ['标题已经存在']
			stat = False
		if stat:
			category = models.Category.query.get(request.form['category_id'])
			article = models.Article(category, request.form['title'], request.form['content'], request.form['picture'], request.form['keywords'], request.form['description'], request.form['posi'])
			db.session.add(article)
			db.session.commit()
			flash('添加文章"%s"成功' % request.form['title'])
			return redirect(url_for('article'))
		
	data_model = models.Data_model.query.filter_by(code='article').first()
	categories = models.Category.query.filter_by(data_model_id=data_model.id).all()
	return render_template('article_add.html', setting=setting, error=error, categories=categories)


@app.route('/article/<int:id>')
@login_required
def article_detail(id=0):
	setting = {'url':'article'}
	setting['categories'] = get_categories()	
	article = models.Article.query.get(id)
	return render_template('article_detail.html', setting=setting, article=article)


@app.route('/article/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def article_edit(id=0):
	setting = {'url':'article'}
	setting['categories'] = get_categories()	
	error = {} 
	article = models.Article.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['标题不能为空']
			stat = False
		elif models.Article.query.filter(models.Article.id!=id).filter_by(title=request.form['title']).first():
			error['title'] = ['标题已经存在']
			stat = False
		if stat:
			article.category = models.Category.query.get(request.form['category_id'])
			article.title = request.form['title']
			article.picture = request.form['picture']
			article.content = request.form['content']
			article.keywords = request.form['keywords']
			article.description = request.form['description']
			article.posi = request.form['posi']
			article.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改文章"%s"成功, <a href="%s">继续修改</a><a href="%s">删除</a>' % (article.title, url_for('article_edit', id=id), url_for('article_delete', id=id)))
			return redirect(url_for('article'))
		
	data_model = models.Data_model.query.filter_by(code='article').first()
	categories = models.Category.query.filter_by(data_model_id=data_model.id).all()
	return render_template('article_edit.html', setting=setting, error=error, categories=categories, article=article)


@app.route('/article/delete/<int:id>')
@app.route('/article/delete/<id>')
@login_required
def article_delete(id):
	if type(id) is int:
		article = models.Article.query.get_or_404(id)
		if article:
			flash('删除文章"%s"成功' % article.title)
			db.session.delete(article)
			db.session.commit()
	else:
		for cur_id in id.split(','):	
			if id:
				article = models.Article.query.get(cur_id)
				if article:
					flash('删除文章"%s"成功' % article.title)
					db.session.delete(article)
					db.session.commit()
	return redirect(url_for('article'))


@app.route('/product')
@app.route('/product/page/<int:page>')
@app.route('/product/category/<int:category_id>', methods=['GET',])
@app.route('/product/category/int:category_id>/page/<int:page>', methods=['GET',])
@login_required
def product(page=1, category_id=0):	
	setting = {'url':'product'}
	setting['categories'] = get_categories()	
	pagination = models.Product.query.paginate(page, app.config['PAGINATION'])
	products = models.Product.query.order_by('create_at DESC').offset((pagination.page-1)*app.config['PAGINATION']).limit(app.config['PAGINATION']).all()
	return render_template('product_list.html', setting=setting, products=products, pagination=pagination)


@app.route('/product/add', methods=['GET', 'POST'])
@login_required
def product_add():
	setting = {'url':'product'}
	setting['categories'] = get_categories()	
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Product.query.filter_by(name=request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			category = models.Category.query.get(request.form['category_id'])
			product = models.Product(category, request.form['name'], request.form['content'], request.form['picture'], request.form['keywords'], request.form['description'], request.form['posi'])
			db.session.add(product)
			db.session.commit()
			flash('添加产品" %s "成功' % request.form['name'])
			return redirect(url_for('product'))
		
	data_model = models.Data_model.query.filter_by(code='product').first()
	categories = models.Category.query.filter_by(data_model_id=data_model.id).all()
	return render_template('product_add.html', setting=setting, error=error, categories=categories)


@app.route('/product/<int:id>')
@login_required
def product_detail(id=0):
	setting = {'url':'product'}
	setting['categories'] = get_categories()	
	product = models.Product.query.get_or_404(id)
	return render_template('product_detail.html', setting=setting, product=product)


@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def product_edit(id=0):
	setting = {'url':'product'}
	setting['categories'] = get_categories()	
	error = {} 
	product = models.Product.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Product.query.filter(models.Product.id!=id).filter_by(name=request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			product.category = models.Category.query.get(request.form['category_id'])
			product.name = request.form['name']
			product.picture = request.form['picture']
			product.content = request.form['content']
			product.keywords = request.form['keywords']
			product.description = request.form['description']
			product.posi = request.form['posi']
			product.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改产品" %s "成功' % product.name)
			return redirect(url_for('product'))
		
	data_model = models.Data_model.query.filter_by(code='product').first()
	categories = models.Category.query.filter_by(data_model_id=data_model.id).all()
	return render_template('product_edit.html', setting=setting, error=error, categories=categories, product=product)


@app.route('/product/delete/<int:id>')
@login_required
def product_delete(id=0):
	product = models.Product.query.get_or_404(id)
	flash('删除产品" %s "成功' % product.name)
	db.session.delete(product)
	db.session.commit()
	return redirect(url_for('product'))


@app.route('/picture')
@app.route('/picture/page/<int:page>')
@app.route('/picture/category/<int:category_id>', methods=['GET',])
@app.route('/picture/category/int:category_id>/page/<int:page>', methods=['GET',])
@login_required
def picture(page=1, category_id=0):	
	setting = {'url':'picture'}
	setting['categories'] = get_categories()	
	pagination = models.Picture.query.paginate(page, app.config['PAGINATION'])
	pictures = models.Picture.query.order_by('create_at DESC').offset((pagination.page-1)*app.config['PAGINATION']).limit(app.config['PAGINATION']).all()
	return render_template('picture_list.html', setting=setting, pictures=pictures, pagination=pagination)


@app.route('/picture/add', methods=['GET', 'POST'])
@login_required
def picture_add():
	setting = {'url':'picture'}
	setting['categories'] = get_categories()	
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['标题不能为空']
			stat = False
		elif models.Picture.query.filter_by(title=request.form['title']).first():
			error['title'] = ['标题已经存在']
			stat = False
		if stat:
			category = models.Category.query.get(request.form['category_id'])
			picture = models.Picture(category, request.form['title'], request.form['content'], request.form['picture'], request.form['keywords'], request.form['description'], request.form['posi'])
			db.session.add(picture)
			db.session.commit()
			flash('添加图库" %s "成功' % request.form['title'])
			return redirect(url_for('picture'))
		
	categories = models.Category.query.all()
	data_model = models.Data_model.query.filter_by(code='article').first()
	return render_template('picture_add.html', setting=setting, error=error, categories=categories)


@app.route('/picture/<int:id>')
@login_required
def picture_detail(id=0):
	picture = models.Picture.query.get(id)
	setting['categories'] = get_categories()	
	return render_template('picture_detail.html', setting=setting, picture=picture)


@app.route('/picture/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def picture_edit(id=0):
	setting = {'url':'picture'}
	setting['categories'] = get_categories()	
	error = {} 
	picture = models.Picture.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['title']:
			error['title'] = ['标题不能空']
			stat = False
		elif models.Picture.query.filter(models.Picture.id!=id).filter_by(title=request.form['title']).first():
			error['title'] = ['标题已经存在']
			stat = False
		if stat:
			picture.category = models.Category.query.get(request.form['category_id'])
			picture.title = request.form['title']
			picture.picture = request.form['picture']
			picture.content = request.form['content']
			picture.keywords = request.form['keywords']
			picture.description = request.form['description']
			picture.posi = request.form['posi']
			picture.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改图库" %s "成功' % picture.title)
			return redirect(url_for('picture'))
		
	categories = models.Category.query.all()
	data_model = models.Data_model.query.filter_by(code='article').first()
	return render_template('picture_edit.html', setting=setting, error=error, categories=categories, picture=picture)


@app.route('/picture/delete/<int:id>')
@login_required
def picture_delete(id=0):
	picture = models.Picture.query.get_or_404(id)
	flash('删除图库" %s "成功' % picture.title)
	db.session.delete(picture)
	db.session.commit()
	return redirect(url_for('picture'))



@app.route('/field', methods=['GET',])
def field_value_check():
    stats = { 'stat':False, 'error':'', 'has':False }
    stats['table'] = request.args.get('table', '')
    stats['field'] = request.args.get('field', '')
    stats['value'] = request.args.get('value', '')
    if request.args.get('id', ''):
        stats['id'] = int(request.args.get('id', ''))
    else:
        stats['id'] = 0
    check = {
		'group':['name',],
		'user':['username', 'email',],
		'category':['name',],
		'article':['title',],
		'category':['name',],
		'product':['name',],
		'category':['name',],
		'picture':['name',],
	}	
    print stats['table'] in check
    print stats['field'] in check[stats['table']]
    if stats['table'] in check and stats['field'] in check[stats['table']]:
		stats['stat'] = True
		if stats['id']==0:
			exec("one = models."+stats['table'].capitalize()+".query.filter_by("+stats['field']+"='"+stats['value']+"').first()")	
		else:
			exec("one = models."+stats['table'].capitalize()+".query.filter(models."+stats['table'].capitalize()+".id!='"+str(stats['id'])+"').filter_by("+stats['field']+"='"+stats['value']+"').first()")	
		if one:
			stats['has'] = True
    return jsonify(stats)


# Kindeditor Upload Function
@app.route('/kindeditor/upload', methods=['GET', 'POST'])
@login_required
def kindeditor_upload():
	ext_type = request.args.get('dir', '') 
	field = 'imgFile'
	data = {'error':1}
	if request.method == 'POST' and field in request.files:
		f = request.files[field]
		extension = f.filename.split('.')[-1].lower()
		data['old_filename']=f.filename
		data['extension'] = extension
		extension = f.filename.split('.')[-1]
		if extension in app.config[('upload_'+ext_type).upper()]:	
			file_name = secure_filename(f.filename)
			if len(file_name)<=3:
				file_name = str(datetime.now())+"."+extension
			f.save('./app/static/upload/'+ext_type+'/' + file_name)
			data['error'] = 0 
			data['url'] = '/static/upload/'+ext_type+'/'+file_name 
			data['filename']=file_name
			data['upload_time'] = datetime.utcnow()
		else: 
			data['message'] = '不允许上传此类文件'
	else:
		data['message'] = '上传文件不存在'
	return jsonify(data)

@app.route('/kindeditor/filemanager', methods=['GET',])
@login_required
def kindeditor_filemanager():	
	data = {}
	upload_url = '/static/upload/'
	upload_dir = './app/static/upload/' 
	dir_ = request.args.get('dir', '')
	path = request.args.get('path', '')
	order = request.args.get('order', '')
	#cur_dir = ''
	if dir_ in ['', 'image', 'flash', 'media', 'file']:
		if path:
			cur_path = upload_dir + path + '/'
			cur_url = upload_url + path	 + '/'
		else:
			cur_path = upload_dir
			cur_url = upload_url
		import re
		import os
		import os.path
		if re.search(r'/\.\./', cur_path):
			data['message'] = '操作不允许'
		elif re.search(r'/\/$/', cur_path):
			data['message'] = '无效的参数'
		elif not os.path.isdir(cur_path):
			data['message'] = '目录不存在'
		else:
			items = []
			for item in os.listdir(cur_path):	
				file_item = {}
				extension = item.split('.')[-1].lower()
				if os.path.isdir(cur_path+item) or extension in app.config[('upload_'+dir_).upper()]:	
					if os.path.isdir(cur_path+item):
						file_item['is_dir'] = True
						file_item['has_file'] = len(os.listdir(cur_path+item)) 
						file_item['filesize'] = 0 
						file_item['is_photo'] = False
						file_item['filetype'] = ''
					else:
						file_item['is_dir'] = False 
						file_item['has_file'] = False 
						file_item['filesize'] = os.path.getsize(cur_path+item) 
						file_item['filetype'] = item.split('.')[-1].lower()
						file_item['is_photo'] = file_item['filetype'] in app.config['UPLOAD_IMAGE'] 
					file_item['filename'] = item
					import time
					file_item['datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(cur_path+item)))
					items.append(file_item)
			#order file
			if order == 'SIZE':
			    items.sort(cmp=lambda x,y:cmp(x['filesize'],y['filesize']))	
			elif order == 'TYPE':
				items.sort(cmp=lambda x,y:cmp(x['filetype'],y['filetype']))	
			else:
				items.sort(cmp=lambda x,y:cmp([not x['is_dir'],x['filename']],[not y['is_dir'],y['filename']]))	

			data['file_list'] = items
			data['moveup_dir_path'] = cur_path.split('/')[-2] 
			data['current_dir_path'] = path 
			data['current_url'] = cur_url 
			data['total_count'] = data['file_list'] and len(data['file_list']) or 0
	else:
		data['message'] = '显示文件夹有错误'
	return jsonify(data)

@app.route('/data_model')
@login_required
def data_model():
	setting = {'url':'data_model'}
	data_models = models.Data_model.query.order_by('create_at ASC').all()
	return render_template('data_model_list.html', setting=setting, data_models=data_models)


@app.route('/data_model/add', methods=['GET', 'POST'])
@login_required
def data_model_add():
	setting = {'url':'data_model'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Data_model.query.filter_by(name=request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			data_model_add = models.Data_model(request.form['name'], request.form['code'], request.form['description'])		
			db.session.add(data_model_add)
			db.session.commit()
			flash('添加数据模型"%s"成功' % request.form['name'])
			return redirect(url_for('data_model'))
		
	return render_template('data_model_add.html', setting=setting, error=error)


@app.route('/data_model/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def data_model_edit(id=0):
	setting = {'url':'data_model'}
	error = {} 
	data_model = models.Data_model.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Data_model.query.filter(models.Data_model.id!=id).filter(models.Data_model.name==request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			data_model.name = request.form['name']
			data_model.code = request.form['code']
			data_model.description = request.form['description']
			data_model.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改数据模型"%s"成功' % data_model.name)
			return redirect(url_for('data_model'))
		
	return render_template('data_model_edit.html', setting=setting, error=error, data_model=data_model)


@app.route('/data_model/delete/<int:id>')
@login_required
def data_model_delete(id=0):
	data_model = models.Data_model.query.get_or_404(id)
	flash('删除数据模型"%s"成功' % data_model.name)
	db.session.delete(data_model)
	db.session.commit()
	return redirect(url_for('data_model'))

@app.route('/member_group')
@login_required
def member_group():
	setting = {'url':'member_group'}
	member_groups = models.Member_group.query.order_by('create_at ASC').all()
	return render_template('member_group_list.html', setting=setting, member_groups=member_groups)


@app.route('/member_group/add', methods=['GET', 'POST'])
@login_required
def member_group_add():
	setting = {'url':'member_group'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Member_group.query.filter_by(name=request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			member_group_add = models.Member_group(request.form['name'], request.form['description'])		
			db.session.add(member_group_add)
			db.session.commit()
			flash('添加会员组"%s"成功' % request.form['name'])
			return redirect(url_for('member_group'))
		
	return render_template('member_group_add.html', setting=setting, error=error)


@app.route('/member_group/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def member_group_edit(id=0):
	setting = {'url':'member_group'}
	error = {} 
	member_group = models.Member_group.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['name']:
			error['name'] = ['名称不能为空']
			stat = False
		elif models.Member_group.query.filter(models.Member_group.id!=id).filter(models.Member_group.name==request.form['name']).first():
			error['name'] = ['名称已经存在']
			stat = False
		if stat:
			member_group.name = request.form['name']
			member_group.description = request.form['description']
			member_group.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改会员组"%s"成功' % member_group.name)
			return redirect(url_for('member_group'))
		
	return render_template('member_group_edit.html', setting=setting, error=error, member_group=member_group)


@app.route('/member_group/delete/<int:id>')
@login_required
def member_group_delete(id=0):
	member_group = models.Member_group.query.get_or_404(id)
	flash('删除会员组"%s"成功' % member_group.name)
	db.session.delete(member_group)
	db.session.commit()
	return redirect(url_for('member_group'))


@app.route('/member')
@app.route('/member/page/<int:page>')
@login_required
def member(page=1):	
	setting = {'url':'member'}
	pagination = models.Member.query.paginate(page, app.config['PAGINATION'])
	members = models.Member.query.order_by('create_at DESC').offset((pagination.page-1)*app.config['PAGINATION']).limit(app.config['PAGINATION']).all()
	return render_template('member_list.html', setting=setting, members=members, pagination=pagination)


@app.route('/member/add', methods=['GET', 'POST'])
@login_required
def member_add():
	setting = {'url':'member'}
	error = {} 
	if request.method == 'POST':
		stat = True
		if not request.form['username']:
			error['userrname'] = ['会员名不能为空']
			stat = False
		elif models.Member.query.filter_by(username=request.form['username']).first():
			error['username'] = ['会员名已经存在']
			stat = False
		if not request.form['email']:
			error['email'] = ['邮箱地址不能为空']
			stat = False
		if not request.form['password']:
			error['password'] = ['密码不能为空']
			stat = False
		if not request.form['password_confirm']:
			error['password_confirm'] = ['重复密码不能为空']
			stat = False
		if request.form['password']<>request.form['password_confirm']:
			error['password_confirm'] = ['两次密码不一致']
			stat = False
		if stat:
			member_group = models.Member_group.query.get(request.form['member_group_id'])
			member_add = models.Member(member_group, request.form['username'], request.form['email'], request.form['password'], request.form['is_active'])
			db.session.add(member_add)
			db.session.commit()
			flash('添加会员"%s"成功' % request.form['username'])
			return redirect(url_for('member'))
		
	member_groups = models.Member_group.query.order_by('create_at ASC').all()
	return render_template('member_add.html', setting=setting, error=error, member_groups=member_groups)


@app.route('/member/<int:id>')
@login_required
def member_detail(id=0):
	setting = {'url':'member'}
	member = models.Member.query.get(id)
	return render_template('member_detail.html', setting=setting, member=member)


@app.route('/member/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def member_edit(id=0):
	setting = {'url':'member'}
	error = {} 
	member = models.Member.query.get_or_404(id)
	if request.method == 'POST':
		stat = True
		if not request.form['username']:
			error['username'] = ['会员名不能为空']
			stat = False
		elif models.Member.query.filter(models.Member.id!=id).filter_by(username=request.form['username']).first():
			error['name'] = ['会员名已经存在,请使用其他会员']
			stat = False
		if not request.form['email']:
			error['email'] = ['邮箱不能为空']
			stat = False
		elif models.Member.query.filter(models.Member.id!=id).filter_by(email=request.form['email']).first():
			error['name'] = ['邮箱已经注册过，请使用其他邮箱']
			stat = False
		if request.form['password_old']:
			if not request.form['password']:
				error['password'] = ['新密码不能为空']
				stat = False
			if not request.form['password_confirm']:
				error['password_confirm'] = ['重复新密码不能为空']
				stat = False
			if request.form['password']<>request.form['password_confirm']:
				error['password_confirm'] = ['两次新密码不一致']
				stat = False
		if stat:
			member_group = models.Member_group.query.get(request.form['member_group_id'])
			member.member_group = member_group
			member.username = request.form['username']
			if request.form['password_old']==member.password and request.form['password']: 
				member.password = request.form['password']
			member.email = request.form['email']
			member.is_active = request.form['is_active']
			member.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改会员"%s"成功' % member.username)
			return redirect(url_for('member'))
	member_groups = models.Member_group.query.order_by('create_at ASC').all()
	return render_template('member_edit.html', setting=setting, error=error, member_groups=member_groups, member=member)


@app.route('/member/delete/<int:id>')
@login_required
def member_delete(id=0):
	member = models.Member.query.get_or_404(id)
	flash('删除会员"%s"成功' % member.username)
	db.session.delete(member)
	db.session.commit()
	return redirect(url_for('member'))


@app.route('/single_page/edit/<int:id>', methods=['GET', 'POST'])
@app.route('/single_page/category/<int:category_id>', methods=['GET', 'POST'])
@login_required
def single_page_edit(id=0, category_id=0):
	setting = {'url':'single_page'}
	error = {} 
	if id:
		single_page = models.Single_page.query.get_or_404(id)
	if category_id:
		single_page = models.Single_page.query.filter_by(category_id=category_id).first()
	if not single_page and category_id:
		category = models.Category.query.get_or_404(category_id)
		if category: 
			single_page = models.Single_page(category, '', '', '')	
			db.session.add(single_page)
			db.session.commit()
	if request.method == 'POST':
		stat = True
		if stat:
			single_page.content = request.form['content']
			single_page.keywords = request.form['keywords']
			single_page.description = request.form['description']
			single_page.update_at = datetime.utcnow()
			db.session.commit()
			flash('修改单页"%s"成功' % (single_page.category.title))
			return redirect(url_for('single_page_edit', category_id=single_page.category_id))
		
	return render_template('single_page_edit.html', setting=setting, error=error, single_page=single_page)



