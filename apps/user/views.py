#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/15 10:00
** @Author：Anonymous
** @Description：
**************************************************************
'''
import json
import hashlib
import os
from werkzeug.utils import secure_filename, redirect
import settings
from exts import db
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required, current_user
from flask import request, render_template, jsonify, Blueprint, session, url_for
from exts.common import generate_random_str, send_mail, insert_audit_log
from exts.logHandler import base_logger as logger


user_bp = Blueprint('user_bp', __name__, url_prefix='')
model_name = '登录'


class User(UserMixin):
	def __init__(self, username):
		self.id = username  # 用户名作为登录用户ID


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")
	else:
		role = int(request.json['role'])
		if role == 1:
			result = db.execute_sql('SELECT password,status from admin WHERE username = %s',
									(request.json['username'])).fetchone()
		elif role == 2:
			result = db.execute_sql('SELECT password from teacher WHERE username = %s',
									(request.json['username'])).fetchone()
		elif role == 3:
			result = db.execute_sql('SELECT password,status from user WHERE username = %s',
									(request.json['username'])).fetchone()
		else:
			result = None
		if result:
			if role == 1 or role==3:
				if result['status'] == 0:
					return jsonify({'success': False, 'message': "账号已被禁用，请联系管理员!"})
			if result['password'] == request.json['password']:
				session['username'] = request.json['username']
				session['role'] = role
				user = User(request.json['username'])
				login_user(user)
				insert_audit_log(request.remote_addr, request.get_json()['username'], model_name, '账号登录')
				return jsonify({'success': True, 'message': "登录成功!"})
			else:
				return jsonify({'success': False, 'message': "用户名或密码错误!"})
		else:
			return jsonify({'success': False, 'message': "用户不存在!"})


@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
	session.pop('username', None)
	session.pop('role', None)
	insert_audit_log(request.remote_addr, current_user.id, model_name, '账号退出登录')
	logout_user()
	return jsonify({'success': True, 'message': "退出登录成功!"})


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template("register.html")
	else:
		result = db.execute_sql('SELECT email from user WHERE username = %s', request.json['username']).fetchone()
		if result:
			return jsonify({'success': False, 'message': "用户已存在！"})
		else:
			cmd = "INSERT INTO user(username,password,email,role_id,status) VALUES (%s,%s,%s,%s,%s)"
			params = (request.json['username'], request.json['password'], request.json['email'], 3, 1)
			result = db.execute_sql(cmd, params)
			if result:
				insert_audit_log(request.remote_addr, request.json['username'], "用户注册",
								 '用户名:' + request.json['username'] + '注册，密码:{0}'.format(
									 request.json['password']))
				return jsonify({'success': True, 'message': "注册成功!"})
			else:
				return jsonify({'success': False, 'message': "注册失败!"})


@user_bp.route('/resetpassword', methods=['GET', 'POST'])
def reset_user_password():
	# 此处向数据库查询该用户是否存在
	if request.method == 'GET':
		return render_template("reset_password.html")
	else:
		result = db.execute_sql('SELECT email from user WHERE username = %s', request.json['username']).fetchone()
		if result and result['email'] == request.json['email']:
			new_random_password = generate_random_str(8)
			cmd = "UPDATE user SET password=%s WHERE username=%s"
			params = (new_random_password, request.json['username'])
			result = db.execute_sql(cmd, params)
			if result:
				if send_mail(settings.Config.EMAIL_USERNAME, request.get_json()["email"], '用户密码找回',
							 '重置后的密码是：{0}，请尽快登录后修改密码'.format(new_random_password)):
					insert_audit_log(request.remote_addr, request.json['username'], "重置密码",
									 '用户名:' + request.json['username'] + '重置密码为{0}'.format(
										 new_random_password))
					return jsonify({'success': True, 'message': "密码重置成功，请通过邮件里的新密码登录后尽快更改密码!"})
				else:
					return jsonify({'success': False, 'message': "发送邮件失败!"})
		else:
			return jsonify({'success': False, 'message': "用户信息不正确"})


@user_bp.route('/user', methods=['GET'])
@login_required
def user_list():
	if request.args.get('query') is None:
		user_infos = db.execute_sql('SELECT * from user').fetchall()
		[i.update({'register_time': i['register_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in user_infos]
		[i.update({'last_login_time': i['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')}) if i[
			'last_login_time'] else ''
		 for i in user_infos]
		return render_template("user.html", user_infos=user_infos)
	else:
		user_infos = db.execute_sql(
			'SELECT * from user where username like %s or email like %s or description like %s',
			('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%',
			 '%' + request.args.get('query') + '%')).fetchall()
		[i.update({'register_time': i['register_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in user_infos]
		[i.update({'last_login_time': i['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')}) if i[
			'last_login_time'] else '' for i in user_infos]
		return jsonify({"rows": user_infos, "total": len(user_infos)})


@user_bp.route('/user/add', methods=['POST'])
@login_required
def user_add():
	role=int(request.json['role'])
	if role == 1:
		cmd = "INSERT INTO admin(username,password,email,role_id,status,description) VALUES (%s,%s,%s,%s,%s,%s)"
		params = (request.json['username'], request.json['password'], request.json['email'], request.json['role'],
		          request.json['status'], request.json['description'])
	elif role == 2:
		cmd = "INSERT INTO teacher(username,password,email,description) VALUES (%s,%s,%s,%s,%s)"
		params = (request.json['username'], request.json['password'], request.json['email'], request.json['description'])
	elif role == 3:
		cmd = "INSERT INTO user(username,password,email,role_id,status,description) VALUES (%s,%s,%s,%s,%s,%s)"
		params = (request.json['username'], request.json['password'], request.json['email'], request.json['role'],
		          request.json['status'], request.json['description'])
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, "用户管理", '新增账号' + request.get_json()['username'])
		return jsonify({'success': True, 'message': "添加成功!"})
	else:
		return jsonify({'success': False, 'message': "添加失败!"})


@user_bp.route('/user/update', methods=['POST'])
@login_required
def user_update():
	update_dict = {}
	# 根据request.get_json()中的数据构建一个动态的SQL更新语句
	if request.get_json()["password"] != '':
		update_dict.update({'password': request.get_json()["password"]})
	if request.get_json()["email"] != '':
		update_dict.update({'email': request.get_json()["email"]})
	if request.get_json()["role"] != '':
		update_dict.update({'role_id': request.get_json()["role"]})
	if request.get_json()["status"] != '':
		update_dict.update({'status': request.get_json()["status"]})
	if request.get_json()["description"] != '':
		update_dict.update({'description': request.get_json()["description"]})
	# 构建SQL更新语句
	set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
	cmd = f"UPDATE user SET {set_clause} WHERE username = %s"

	# 准备参数列表
	params = list(update_dict.values()) + [request.get_json()["username"]]
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, "用户管理", '更新用户信息')
		return jsonify({'success': True, 'message': "更新成功!"})
	else:
		return jsonify({'success': False, 'message': "更新失败!"})


@user_bp.route('/user/delete', methods=['POST'])
@login_required
def user_delete():
	if 'id' in request.json:
		cmd = "DELETE FROM user WHERE id=%s;"
		result = db.execute_sql(cmd, request.json['id'])
	elif 'ids' in request.json:
		ids_to_delete = request.json['ids']
		# 构建 SQL 语句
		placeholders = ', '.join(['%s'] * len(ids_to_delete))
		cmd = f"DELETE FROM user WHERE id IN ({placeholders})"
		result = db.execute_sql(cmd, ids_to_delete)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, "用户管理", '删除用户,id:' + request.json['id'])
		return jsonify({'success': True, 'message': "删除成功!"})
	else:
		return jsonify({'success': False, 'message': "删除失败!"})


@user_bp.route('/user_center', methods=['GET', 'POST'])
@login_required
def user_center():
	role = session['role']
	if request.method == 'GET':
		if role == 1:
			user_infos = db.execute_sql('SELECT * from admin WHERE username = %s', current_user.id).fetchone()
		elif role == 2:
			user_infos = db.execute_sql('SELECT * from teacher WHERE username = %s', current_user.id).fetchone()
		elif role == 3:
			user_infos = db.execute_sql('SELECT * from user WHERE username = %s', current_user.id).fetchone()
			user_infos.update({'register_time': user_infos['register_time'].strftime('%Y-%m-%d %H:%M:%S')})
			user_infos.update({'last_login_time': user_infos['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')}) if \
			user_infos[
				'last_login_time'] else ''
		return render_template("user_center.html", userinfos=user_infos)
	else:
		update_dict = {}
		# 根据request.get_json()中的数据构建一个动态的SQL更新语句
		if request.get_json()["nickname"] != '':
			update_dict.update({'name': request.get_json()["nickname"]})
		if request.get_json()["email"] != '':
			update_dict.update({'email': request.get_json()["email"]})
		if request.get_json()["description"] != '':
			update_dict.update({'description': request.get_json()["description"]})
		# 构建SQL更新语句
		set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
		if role == 1:
			cmd = f"UPDATE admin SET {set_clause} WHERE username = %s"
		elif role == 2:
			cmd = f"UPDATE teacher SET {set_clause} WHERE username = %s"
		elif role == 3:
			cmd = f"UPDATE user SET {set_clause} WHERE username = %s"
		# 准备参数列表
		params = list(update_dict.values()) + [current_user.id]
		result = db.execute_sql(cmd, params)
		if result:
			insert_audit_log(request.remote_addr, current_user.id, "用户中心管理", '更新用户信息')
			return jsonify({'success': True, 'message': "更新成功!"})
		else:
			return jsonify({'success': False, 'message': "更新失败!"})


@user_bp.route('/password', methods=['GET', 'POST'])
@login_required
def change_password():
	role = session['role']
	if request.method == 'GET':
		return render_template("user_password.html")
	else:
		if role == 1:
			user_infos = db.execute_sql('SELECT password from admin WHERE username = %s', current_user.id).fetchone()
			cmd = "UPDATE admin SET password=%s WHERE username = %s"
		elif role == 2:
			user_infos = db.execute_sql('SELECT password from teacher WHERE username = %s', current_user.id).fetchone()
			cmd = "UPDATE teacher SET password=%s WHERE username = %s"
		elif role == 3:
			user_infos = db.execute_sql('SELECT password from user WHERE username = %s', current_user.id).fetchone()
			cmd = "UPDATE user SET password=%s WHERE username = %s"
		if user_infos['password'] == request.json['oldpwd']:
			params = (request.json['newpwd'], current_user.id)
			result = db.execute_sql(cmd, params)
			if result:
				insert_audit_log(request.remote_addr, current_user.id, "用户中心管理", '修改用户密码')
				session.pop('username', None)
				session.pop('role', None)
				logout_user()
				return {'success': True, 'message': "密码修改成功!"}
			else:
				return {'success': False, 'message': "密码修改失败!"}
		else:
			return {'success': False, 'message': "原始密码错误，密码修改失败!"}


# 用户头像更新
@user_bp.route('/upload/avatar',methods=['POST'])
@login_required
def file_upload():
	role = session['role']
	# 'file'为前端表单中文件输入字段的名称，返回的的是一个FileStorage容器
	file = request.files['file']
	if file:
		# 上传的文件名
		filename = secure_filename(file.filename)
		# 将文件保存到服务器指定目录
		file_path = settings.Config.UPLOAD_FOLDER + filename
		try:
			file.save(file_path)
			# 计算图片md5值作为图片ID
			md5_obj = hashlib.md5()
			with open(file_path, 'rb') as file_obj:
				md5_obj.update(file_obj.read())
			img_id = md5_obj.hexdigest()
			new_file_name = img_id + "." + file.filename.split('.')[-1]
			# 对服务器存储的资源文件进行重命名并返回该图片的路径
			avatar_image_abs_path = settings.Config.UPLOAD_FOLDER + new_file_name
			avatar_image_path = url_for('static', filename='images/users/'+f'{new_file_name}')
			if not os.path.exists(avatar_image_abs_path):
				os.rename(file_path, avatar_image_abs_path)
				# 更新数据库信息
				if role == 1:
					cmd = f"UPDATE admin SET avatar=%s WHERE username = %s"
				elif role == 2:
					cmd = f"UPDATE teacher SET avatar=%s WHERE username = %s"
				elif role == 3:
					cmd = f"UPDATE user SET avatar=%s WHERE username = %s"
				result = db.execute_sql(cmd, (avatar_image_path, current_user.id))
				if result:
					insert_audit_log(request.remote_addr, current_user.id, "用户中心", '上传了文件并更新了头像: ' + filename)
					response = {'success': True, 'message': '上传成功', 'path': avatar_image_path}
				else:
					return jsonify({'success': False, 'message': "更新头像失败!"})
			else:
				response = {'success': False, 'message': '文件已存在'}
		except Exception as e:
			logger.exception(e)
			response = {'success': False, 'message': '上传失败'}
		logger.debug("接口请求返回:" + json.dumps(response, ensure_ascii=False))
		return jsonify(response)


@user_bp.route('/<path:filename>', methods=['GET'])
def serve_image(filename):
	if filename in settings.Config.ALLOWED_EXTENSIONS:
		image_absolute_url = url_for('static', filename=f'{filename}')
		return image_absolute_url
	else:
		# return jsonify({"message":"当前用户未登录，请重新登录"})
		return redirect(url_for('user_bp.login'))