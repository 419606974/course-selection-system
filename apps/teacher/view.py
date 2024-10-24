#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/19 16:50
** @Author：Anonymous
** @Description：
**************************************************************
'''

from flask_login import login_required, current_user
from exts import db
from flask import request, render_template, Blueprint, jsonify

from exts.common import insert_audit_log

teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='')
model_name = '教师管理'

@teacher_bp.route('/teacher', methods=['GET'])
@login_required
def teacher_query():
	if request.args.get('query') is None:
		teacher_infos = db.execute_sql('SELECT * from teacher').fetchall()
		return render_template('teacher.html', teacher_infos=teacher_infos)
	else:
		teacher_infos = db.execute_sql(
			'SELECT * from teacher where username like %s or name like %s or phone like %s or email like %s',
			('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%',
			 '%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%')).fetchall()
	return jsonify({"rows":teacher_infos,"total":len(teacher_infos)})


@teacher_bp.route('/teacher/add', methods=['POST'])
@login_required
def teacher_add():
	cmd = """INSERT INTO teacher(username, name, password, sex, phone, email, `rank`, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
	params = (request.json['username'], request.json['name'], request.json['password'], request.json['sex'],
	          request.json['phone'], request.json['email'], request.json['rank'], request.json['description'])
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '新增教师信息:'+request.json['username'])
		return jsonify({'success': True, 'message': "添加成功!"})
	else:
		return jsonify({'success': False, 'message': "添加失败!"})


@teacher_bp.route('/teacher/update', methods=['POST'])
@login_required
def teacher_update():
	update_dict = {}
	# 根据request.get_json()中的数据构建一个动态的SQL更新语句
	if request.get_json()["name"] != '':
		update_dict.update({'name': request.get_json()["name"]})
	if request.get_json()["password"] != '':
		update_dict.update({'password': request.get_json()["password"]})
	if request.get_json()["email"] != '':
		update_dict.update({'email': request.get_json()["email"]})
	if request.get_json()["phone"] != '':
		update_dict.update({'phone': request.get_json()["phone"]})
	if request.get_json()["rank"] != '':
		update_dict.update({'`rank`': request.get_json()["rank"]})
	if request.get_json()["sex"] != '':
		update_dict.update({'sex': request.get_json()["sex"]})
	if request.get_json()["description"] != '':
		update_dict.update({'description': request.get_json()["description"]})
	# 构建SQL更新语句
	set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
	cmd = f"UPDATE teacher SET {set_clause} WHERE username = %s"

	# 准备参数列表
	params = list(update_dict.values()) + [request.get_json()["username"]]
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '更新教师信息:' + request.json['username'])
		return jsonify({'success': True, 'message': "更新成功!"})
	else:
		return jsonify({'success': False, 'message': "更新失败!"})





@teacher_bp.route('/teacher/delete', methods=['POST'])
@login_required
def teacher_delete():
	if 'id' in request.json:
		cmd = "DELETE FROM teacher WHERE id=%s;"
		result = db.execute_sql(cmd, request.json['id'])
		ids_to_delete = request.json['id']
	elif 'ids' in request.json:
		ids_to_delete = request.json['ids']
		# 构建 SQL 语句
		placeholders = ', '.join(['%s'] * len(ids_to_delete))
		cmd = f"DELETE FROM teacher WHERE id IN ({placeholders})"
		result = db.execute_sql(cmd, ids_to_delete)

	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '删除教师信息:' + str(ids_to_delete))
		return jsonify({'success': True, 'message': "删除成功!"})
	else:
		return jsonify({'success': False, 'message': "删除失败!"})
