#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/20 16:37
** @Author：Anonymous
** @Description：
**************************************************************
'''
from flask_login import login_required, current_user
from exts import db
from flask import request, render_template, Blueprint, jsonify, session

from exts.common import insert_audit_log

course_bp = Blueprint('course_bp', __name__, url_prefix='')
model_name = '选课管理'

@course_bp.route('/course', methods=['GET', 'POST'])
@login_required
def course_query():
	if request.method == 'GET':
		if request.args.get('query') is None:
			if current_user.id != "admin":
				course_infos = db.execute_sql(
					'SELECT course.*, teacher.name AS teacher_name FROM course JOIN teacher ON course.teacher_id = teacher.id WHERE teacher.username=%s ',
					current_user.id).fetchall()
			else:
				course_infos = db.execute_sql(
					'SELECT course.*, teacher.name AS teacher_name FROM course JOIN teacher ON course.teacher_id = teacher.id').fetchall()
			return render_template('course.html', course_infos=course_infos)
		else:
			course_infos = db.execute_sql(
				'SELECT * from course where name like %s or teaching_time like %s or teaching_place like %s',
				('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%',
				 '%' + request.args.get('query') + '%')).fetchall()
			return jsonify({"rows": course_infos, "total": len(course_infos)})
	else:
		course_infos = db.execute_sql('SELECT * from course').fetchall()
		return jsonify(course_infos)


# 根据课程id查询选择该课程的学生信息
@course_bp.route('/courseByStudent', methods=['POST'])
@login_required
def course_query_by_student():
	if 'course_id' not in request.json:
		course_infos = db.execute_sql(
			'SELECT achievement.*, user.name AS student_name FROM achievement JOIN user ON achievement.student_id = user.id').fetchall()
	else:
		course_infos = db.execute_sql(
			'SELECT achievement.*, user.name AS student_name FROM achievement JOIN user ON achievement.student_id = user.id WHERE achievement.course_id = %s',
			(request.json['course_id'])).fetchall()
	return jsonify(course_infos)


@course_bp.route('/course/add', methods=['POST'])
@login_required
def course_add():
	cmd1 = """SELECT * from teacher WHERE username=%s"""
	params1 = (current_user.id)
	result = db.execute_sql(cmd1, params1)
	row = result.fetchone()
	if row:
		cmd2 = """INSERT INTO course(name, teaching_time, teaching_place,allow_stu_num, teacher_id) VALUES (%s, %s, %s, %s, %s)"""
		params2 = (
			request.json['name'], request.json['teachingTime'], request.json['teachingPlace'],
			request.json['allowNumber'],
			row['id'])
		result = db.execute_sql(cmd2, params2)
		if result:
			insert_audit_log(request.remote_addr, current_user.id, model_name, '新增课程:' + request.json['name'])
			return jsonify({'success': True, 'message': "添加成功!"})
		else:
			return jsonify({'success': False, 'message': "添加失败!"})
	else:
		return jsonify({'success': False, 'message': "您不是老师，无法添加课程!"})


@course_bp.route('/course/update', methods=['POST'])
@login_required
def course_update():
	update_dict = {}
	# 根据request.get_json()中的数据构建一个动态的SQL更新语句
	if request.get_json()["name"] != '':
		update_dict.update({'name': request.get_json()["name"]})
	if request.get_json()["updateTime"] != '':
		update_dict.update({'teaching_time': request.get_json()["updateTime"]})
	if request.get_json()["updatePlace"] != '':
		update_dict.update({'teaching_place': request.get_json()["updatePlace"]})
	if request.get_json()["updateNumber"] != '':
		update_dict.update({'allow_stu_num': request.get_json()["updateNumber"]})
	# 构建SQL更新语句
	set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
	cmd = f"UPDATE course SET {set_clause} WHERE name = %s"
	# 准备参数列表
	params = list(update_dict.values()) + [request.get_json()["name"]]
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '更新课程:' + request.json['name'])
		return jsonify({'success': True, 'message': "更新成功!"})
	else:
		return jsonify({'success': False, 'message': "更新失败!"})

@course_bp.route('/course/delete', methods=['POST'])
@login_required
def course_delete():
	if 'id' in request.json:
		cmd = "DELETE FROM course WHERE id=%s;"
		result = db.execute_sql(cmd, request.json['id'])
		ids_to_delete = request.json['id']
	elif 'ids' in request.json:
		ids_to_delete = request.json['ids']
		# 构建 SQL 语句
		placeholders = ', '.join(['%s'] * len(ids_to_delete))
		cmd = f"DELETE FROM course WHERE id IN ({placeholders})"
		result = db.execute_sql(cmd, ids_to_delete)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '删除课程条目:' + str(ids_to_delete))
		return jsonify({'success': True, 'message': "删除成功!"})
	else:
		return jsonify({'success': False, 'message': "删除失败!"})

# 查询成绩
@course_bp.route('/achievement', methods=['GET'])
@login_required
def achievement_query():
	if request.args.get('query') is None:
		# 管理员角色查询
		if session['role'] == 1 or session['role'] == 2:
			achievement_infos = db.execute_sql(
				'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
		return render_template('achievement.html', achievement_infos=achievement_infos)
	else:
		if 'all' not in request.args.get('query'):
			achievement_infos = db.execute_sql('SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s',(request.args.get('query'))).fetchall()
		else:
			achievement_infos = db.execute_sql('SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
		return jsonify({"rows": achievement_infos, "total": len(achievement_infos)})


# 添加成绩
@course_bp.route('/achievement/add', methods=['POST'])
@login_required
def achievement_add():
	cmd1 = """SELECT * from user WHERE id=%s"""
	params1 = (request.json['studentId'])
	row1 = db.execute_sql(cmd1, params1).fetchone()
	if row1:
		cmd2 = """SELECT * from course WHERE id=%s"""
		params2 = (request.json['courseId'])
		row2 = db.execute_sql(cmd2, params2).fetchone()
		if row2:
			isExistFlag = db.execute_sql("SELECT COUNT(*) AS count FROM achievement WHERE course_id = %s AND student_id = %s",(request.json['courseId'], request.json['studentId'])).fetchone()
			if isExistFlag and isExistFlag['count'] == 0:
				cmd3 = """INSERT INTO achievement(score, course_id, student_id) VALUES (%s, %s, %s)"""
				params3 = (
					request.json['score'], request.json['courseId'], request.json['studentId'])
				result = db.execute_sql(cmd3, params3)
				if result:
					insert_audit_log(request.remote_addr, current_user.id, model_name,
					                 '添加成绩:' + request.json['score'])
					return jsonify({'success': True, 'message': "添加成功!"})
				else:
					return jsonify({'success': False, 'message': "添加失败!"})
			else:
				return jsonify({'success': False, 'message': "该学生已登记成绩!"})
		else:
			return jsonify({'success': False, 'message': "课程信息不存在!"})
	else:
		return jsonify({'success': False, 'message': "学生信息不存在!"})



@course_bp.route('/achievement/update', methods=['POST'])
@login_required
def achievement_update():
	cmd1 = """SELECT * from user WHERE name=%s"""
	params1 = (request.json['studentName'])
	row1 = db.execute_sql(cmd1, params1).fetchone()
	if row1:
		cmd2 = """SELECT * from course WHERE name=%s"""
		params2 = (request.json['courseName'])
		row2 = db.execute_sql(cmd2, params2).fetchone()
		if row2:
			cmd3 = """UPDATE achievement SET score=%s WHERE id=%s"""
			params3 = (request.json['newScore'], request.json['id'])
			result = db.execute_sql(cmd3, params3)
			if result:
				insert_audit_log(request.remote_addr, current_user.id, model_name, '更新课程' + request.json['id']+'成绩')
				return jsonify({'success': True, 'message': "更新成功!"})
			else:
				return jsonify({'success': False, 'message': "更新失败!"})

		else:
			return jsonify({'success': False, 'message': "课程信息不存在!"})
	else:
		return jsonify({'success': False, 'message': "用户信息不存在!"})



@course_bp.route('/achievement/delete', methods=['POST'])
@login_required
def achievement_delete():
	if 'id' in request.json:
		cmd = "DELETE FROM achievement WHERE id=%s;"
		result = db.execute_sql(cmd, request.json['id'])
		ids_to_delete = request.json['id']
	elif 'ids' in request.json:
		ids_to_delete = request.json['ids']
		# 构建 SQL 语句
		placeholders = ', '.join(['%s'] * len(ids_to_delete))
		cmd = f"DELETE FROM achievement WHERE id IN ({placeholders})"
		result = db.execute_sql(cmd, ids_to_delete)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '删除成绩条目:' + str(ids_to_delete))
		return jsonify({'success': True, 'message': "删除成功!"})
	else:
		return jsonify({'success': False, 'message': "删除失败!"})


@course_bp.route('/score', methods=['GET'])
@login_required
def score_query():
	if session['role'] == 1 or session['role'] == 2:
		# 管理员、教师角色查询
		if request.args.get('query') is None:
			score_infos = db.execute_sql(
				'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
			return render_template('score.html', score_infos=score_infos)
		else:
			if 'all' not in request.args.get('query'):
				score_infos = db.execute_sql('SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s',request.args.get('query')).fetchall()
			else:
				score_infos = db.execute_sql(
					'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
			return jsonify({"rows": score_infos, "total": len(score_infos)})
	else:
		if request.args.get('query') is None:
			score_infos = db.execute_sql(
				'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id  WHERE user.username=%s',current_user.id).fetchall()
			return render_template('score.html', score_infos=score_infos)
		if 'all' not in request.args.get('query'):
			score_infos = db.execute_sql(
				'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s AND username=%s',
				(request.args.get('query'),current_user.id)).fetchall()
		else:
			score_infos = db.execute_sql(
				'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE user.username=%s',current_user.id).fetchall()
		return jsonify({"rows": score_infos, "total": len(score_infos)})


@course_bp.route('/course_select', methods=['GET', 'POST'])
@login_required
def course_select():
	if request.method == 'GET':
		if request.args.get('query') is None:
			course_infos = db.execute_sql(
					'SELECT course.*, teacher.name AS teacher_name FROM course JOIN teacher ON course.teacher_id = teacher.id').fetchall()
			return render_template('course_select.html', course_infos=course_infos)
		else:
			course_infos = db.execute_sql(
				'SELECT * from course where name like %s or teaching_time like %s or teaching_place like %s',
				('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%',
				 '%' + request.args.get('query') + '%')).fetchall()
			return jsonify({"rows": course_infos, "total": len(course_infos)})
	else:
		row1 = db.execute_sql("SELECT * from user WHERE username=%s",current_user.id).fetchone()
		if row1:
			studentId=row1['id']
			# 首先检查是否存在相同的记录
			check_sql = """
			        SELECT COUNT(*) AS count
			        FROM achievement
			        WHERE course_id = %s AND student_id = %s;
			    """
			cursor = db.execute_sql(check_sql, (request.json['id'], studentId))
			if cursor:
				result = cursor.fetchone()
				if result['count'] == 0:
					# 如果不存在相同的记录，则插入新记录
					result1 = db.execute_sql("INSERT INTO achievement(course_id, student_id) VALUES (%s, %s)",(request.json['id'], studentId))
					result2 = db.execute_sql("UPDATE course SET selected_stu_num=selected_stu_num+1 WHERE id=%s",(request.json['id']))
					if result1 and result2:
						insert_audit_log(request.remote_addr, current_user.id, model_name,
						                 '学生:'+str(studentId)+' 选课:' + str(request.json['id']))
						return jsonify({'success': True, 'message': "选课成功!"})
					else:
						return jsonify({'success': False, 'message': "选课失败!"})
				else:
					return jsonify({'success': False, 'message': "该课程已选!"})
				



# 已选课程选择
@course_bp.route('/my_course', methods=['GET'])
@login_required
def my_course():
	course_infos = db.execute_sql(
		'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE user.username=%s',current_user.id).fetchall()
	return render_template('my_course.html', course_infos=course_infos)

# 取消已选课程选择
@course_bp.route('/course_cancel', methods=['POST'])
@login_required
def course_cancel():
	# 如果不存在相同的记录，则插入新记录
	result1 = db.execute_sql("DELETE FROM achievement WHERE id=%s",(request.json['id']))
	result2 = db.execute_sql("UPDATE course SET selected_stu_num=selected_stu_num-1 WHERE id=%s",(request.json['id']))
	if result1 and result2:
		insert_audit_log(request.remote_addr, current_user.id, model_name,'取消选课:' + str(request.json['id']))
		return jsonify({'success': True, 'message': "取消成功!"})
	else:
		return jsonify({'success': False, 'message': "取消选课失败!"})
