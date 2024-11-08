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
import pandas as pd

course_bp = Blueprint('course_bp', __name__, url_prefix='')
model_name = '选课管理'
achievement_model_name = '成绩管理'


@course_bp.route('/course', methods=['GET', 'POST'])
@login_required
def course_query():
    if request.method == 'GET':
        if request.args.get('query') is None and request.args.get('course_no') is None:
            # if current_user.id != "admin":
            #     course_infos = db.execute_sql(
            #         'SELECT course.*, teacher.name AS teacher_name FROM course JOIN teacher ON course.teacher_id = teacher.id WHERE teacher.username=%s ',
            #         current_user.id).fetchall()
            # else:
            #     course_infos = db.execute_sql(
            #         'SELECT course.*, teacher.name AS teacher_name, teacher.number AS teacher_number FROM course JOIN teacher ON course.teacher_id = teacher.id').fetchall()
            course_infos = db.execute_sql(
                     'SELECT course.*, teacher.name AS teacher_name, teacher.number AS teacher_number FROM course JOIN teacher ON course.teacher_id = teacher.id').fetchall()
            return render_template('course.html', course_infos=course_infos)
        elif request.args.get('query') is not None:
            course_infos = db.execute_sql(
                'SELECT * from course where number like %s or name like %s',
                ('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%')).fetchall()
            for course_info in course_infos:
                cmd1 = """SELECT * from teacher WHERE id=%s"""
                params1 = (course_info['teacher_id'])
                result = db.execute_sql(cmd1, params1)
                row = result.fetchone()
                teacher_name = row['name']
                course_info.update({'teacher_name': teacher_name})
            return jsonify({"rows": course_infos, "total": len(course_infos)})
        elif request.args.get('course_no') is not None:
            course_info = db.execute_sql(
                'SELECT course.*, teacher.name AS teacher_name from course JOIN teacher ON course.teacher_id = teacher.id where course.number=%s',
                (request.args.get('course_no'))).fetchone()
            if course_info:
                return jsonify({'success': True, 'course_info': course_info})
            else:
                return jsonify({'success': False, 'message': "不存在该课程"})
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


# @course_bp.route('/course/add', methods=['POST'])
# @login_required
# def course_add():
# 	cmd1 = """SELECT * from teacher WHERE username=%s"""
# 	params1 = (current_user.id)
# 	result = db.execute_sql(cmd1, params1)
# 	row = result.fetchone()
# 	if row:
# 		cmd2 = """INSERT INTO course(name, teaching_time, teaching_place,allow_stu_num, teacher_id) VALUES (%s, %s, %s, %s, %s)"""
# 		params2 = (
# 			request.json['name'], request.json['teachingTime'], request.json['teachingPlace'],
# 			request.json['allowNumber'],
# 			row['id'])
# 		result = db.execute_sql(cmd2, params2)
# 		if result:
# 			insert_audit_log(request.remote_addr, current_user.id, model_name, '新增课程:' + request.json['name'])
# 			return jsonify({'success': True, 'message': "添加成功!"})
# 		else:
# 			return jsonify({'success': False, 'message': "添加失败!"})
# 	else:
# 		return jsonify({'success': False, 'message': "您不是老师，无法添加课程!"})


@course_bp.route('/course/add', methods=['POST'])
@login_required
def course_add():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    cmd1 = """SELECT * from teacher WHERE number=%s"""
    params1 = (request.json['teachernum'])
    result = db.execute_sql(cmd1, params1)
    row = result.fetchone()
    if not row:
        return jsonify({'success': False, 'message': "不存在该教师编号!"})
    teacher_name = row['name']
    cmd2 = """INSERT INTO course(number, name, credits, year, semester, startdate, enddate, teaching_time, 
	teaching_place, teacher_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    params2 = (request.json['number'], request.json['name'], request.json['credits'], request.json['year'],
               request.json['semester'], request.json['startdate'], request.json['enddate'],
               request.json['teachingTime'], request.json['teachingPlace'], row['id'])
    result = db.execute_sql(cmd2, params2)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '新增课程: ' + request.json['name'])
        return jsonify({'success': True, 'message': "添加成功!", 'teacher_name': teacher_name})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@course_bp.route('/course/update', methods=['POST'])
@login_required
def course_update():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    update_dict = {}
    # 根据request.get_json()中的数据构建一个动态的SQL更新语句
    if request.get_json()["number"] != '':
        update_dict.update({'number': request.get_json()["number"]})
    if request.get_json()["name"] != '':
        update_dict.update({'name': request.get_json()["name"]})
    if request.get_json()["credits"] != '':
        update_dict.update({'credits': request.get_json()["credits"]})
    if request.get_json()["year"] != '':
        update_dict.update({'year': request.get_json()["year"]})
    if request.get_json()["semester"] != '':
        update_dict.update({'semester': request.get_json()["semester"]})
    if request.get_json()["startdate"] != '':
        update_dict.update({'startdate': request.get_json()["startdate"]})
    if request.get_json()["enddate"] != '':
        update_dict.update({'enddate': request.get_json()["enddate"]})
    if request.get_json()["updateTime"] != '':
        update_dict.update({'teaching_time': request.get_json()["updateTime"]})
    if request.get_json()["updatePlace"] != '':
        update_dict.update({'teaching_place': request.get_json()["updatePlace"]})
    teacher_name = ''
    if request.get_json()["teachernum"] != '':
        cmd1 = """SELECT * from teacher WHERE number=%s"""
        params1 = (request.get_json()["teachernum"])
        result = db.execute_sql(cmd1, params1)
        row = result.fetchone()
        if not row:
            return jsonify({'success': False, 'message': "不存在该教师编号!"})
        update_dict.update({'teacher_id': row['id']})
        teacher_name = row['name']
    # 构建SQL更新语句
    set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
    cmd = f"UPDATE course SET {set_clause} WHERE name = %s"
    # 准备参数列表
    params = list(update_dict.values()) + [request.get_json()["name"]]
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '更新课程: ' + request.json['name'])
        data = jsonify({'success': True, 'message': "更新成功!"})
        if teacher_name:
            data = jsonify({'success': True, 'message': "更新成功!", 'teacher_name': teacher_name})
        return data
    else:
        return jsonify({'success': False, 'message': "更新失败!"})


@course_bp.route('/course/delete', methods=['POST'])
@login_required
def course_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    if 'id' in request.json:
        achievement_cmd = """SELECT * from achievement WHERE course_id=%s"""
        achievement_params = (request.json['id'])
        achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
        if achievement_row:
            return jsonify({'success': False, 'message': "存在该课程对应的成绩，请更改后再删除"})
        cmd = "DELETE FROM course WHERE id=%s;"
        result = db.execute_sql(cmd, request.json['id'])
        ids_to_delete = request.json['id']
    elif 'ids' in request.json:
        ids_to_delete = request.json['ids']
        for id in ids_to_delete:
            achievement_cmd = """SELECT * from achievement WHERE course_id=%s"""
            achievement_params = (id)
            achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
            if achievement_row:
                return jsonify({'success': False, 'message': "存在该课程对应的成绩，请更改后再删除"})
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
                'SELECT achievement.*, course.name AS course_name, course.number AS course_no, course.year AS course_year, course.semester AS course_semester, user.name AS student_name, user.username AS student_no, gradelevel.name AS gradelevel_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id JOIN gradelevel ON achievement.gradelevel_id = gradelevel.id ORDER BY achievement.id').fetchall()
        return render_template('achievement.html', achievement_infos=achievement_infos)
    else:
        if 'all' not in request.args.get('query'):
            achievement_infos = db.execute_sql(
                'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s',
                (request.args.get('query'))).fetchall()
        else:
            achievement_infos = db.execute_sql(
                'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
        return jsonify({"rows": achievement_infos, "total": len(achievement_infos)})


# 添加成绩
@course_bp.route('/achievement/add', methods=['POST'])
@login_required
def achievement_add():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    student_cmd = """SELECT * from user WHERE username=%s"""
    student_params = (request.json['studentNo'])
    student_row = db.execute_sql(student_cmd, student_params).fetchone()
    if student_row:
        course_cmd = """SELECT * from course WHERE number=%s"""
        course_params = (request.json['courseNo'])
        course_row = db.execute_sql(course_cmd, course_params).fetchone()
        if course_row:
            isExistFlag = db.execute_sql(
                "SELECT COUNT(*) AS count FROM achievement WHERE course_id = %s AND student_id = %s",
                (course_row['id'], student_row['id'])).fetchone()
            if isExistFlag and isExistFlag['count'] == 0:
                level_cmd = """SELECT * from gradelevel WHERE %s BETWEEN min_score AND max_score;"""
                level_params = (request.json['score'])
                level_row = db.execute_sql(level_cmd, level_params).fetchone()
                achievement_info = {'course': course_row, 'student': student_row, 'score': request.json['score']}
                if level_row:
                    cmd = """INSERT INTO achievement(score, course_id, student_id, gradelevel_id) VALUES (%s, %s, %s, %s)"""
                    params = (request.json['score'], course_row['id'], student_row['id'], level_row['id'])
                    achievement_info.update({'gradelevel_name': level_row['name']})
                else:
                    cmd = """INSERT INTO achievement(score, course_id, student_id) VALUES (%s, %s, %s)"""
                    params = (request.json['score'], course_row['id'], student_row['id'])
                result = db.execute_sql(cmd, params)
                if result:
                    insert_audit_log(request.remote_addr, current_user.id, achievement_model_name,
                                     '添加成绩: {}-{}-{}'.format(course_row['name'], student_row['name'],
                                                             request.json['score']))
                    return jsonify({'success': True, 'message': "添加成功!", 'achievement_info': achievement_info})
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
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    student_cmd = """SELECT * from user WHERE username=%s"""
    student_params = (request.json['studentNo'])
    student_row = db.execute_sql(student_cmd, student_params).fetchone()
    if student_row:
        course_cmd = """SELECT * from course WHERE number=%s"""
        course_params = (request.json['courseNo'])
        course_row = db.execute_sql(course_cmd, course_params).fetchone()
        if course_row:
            level_cmd = """SELECT * from gradelevel WHERE %s BETWEEN min_score AND max_score;"""
            level_params = (request.json['newScore'])
            level_row = db.execute_sql(level_cmd, level_params).fetchone()
            achievement_info = {'course': course_row, 'student': student_row, 'score': request.json['newScore']}
            if level_row:
                cmd = """UPDATE achievement SET score=%s, gradelevel_id=%s WHERE id=%s"""
                params = (request.json['newScore'], level_row['id'], request.json['id'])
                achievement_info.update({'gradelevel_name': level_row['name']})
            else:
                cmd = """UPDATE achievement SET score=%s WHERE id=%s"""
                params = (request.json['newScore'], request.json['id'])
            result = db.execute_sql(cmd, params)
            if result:
                insert_audit_log(request.remote_addr, current_user.id, achievement_model_name,
                                 '更新成绩: {}-{}-{}'.format(course_row['name'], student_row['name'],
                                                         request.json['newScore']))
                return jsonify({'success': True, 'message': "更新成功!", 'achievement_info': achievement_info})
            else:
                return jsonify({'success': False, 'message': "更新失败!"})

        else:
            return jsonify({'success': False, 'message': "课程信息不存在!"})
    else:
        return jsonify({'success': False, 'message': "用户信息不存在!"})


@course_bp.route('/achievement/delete', methods=['POST'])
@login_required
def achievement_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
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
        insert_audit_log(request.remote_addr, current_user.id, achievement_model_name, '删除成绩条目:' + str(ids_to_delete))
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
                score_infos = db.execute_sql(
                    'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s',
                    request.args.get('query')).fetchall()
            else:
                score_infos = db.execute_sql(
                    'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id').fetchall()
            return jsonify({"rows": score_infos, "total": len(score_infos)})
    else:
        if request.args.get('query') is None:
            score_infos = db.execute_sql(
                'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id  WHERE user.username=%s',
                current_user.id).fetchall()
            return render_template('score.html', score_infos=score_infos)
        if 'all' not in request.args.get('query'):
            score_infos = db.execute_sql(
                'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE course_id=%s AND username=%s',
                (request.args.get('query'), current_user.id)).fetchall()
        else:
            score_infos = db.execute_sql(
                'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE user.username=%s',
                current_user.id).fetchall()
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
        row1 = db.execute_sql("SELECT * from user WHERE username=%s", current_user.id).fetchone()
        if row1:
            studentId = row1['id']
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
                    result1 = db.execute_sql("INSERT INTO achievement(course_id, student_id) VALUES (%s, %s)",
                                             (request.json['id'], studentId))
                    result2 = db.execute_sql("UPDATE course SET selected_stu_num=selected_stu_num+1 WHERE id=%s",
                                             (request.json['id']))
                    if result1 and result2:
                        insert_audit_log(request.remote_addr, current_user.id, model_name,
                                         '学生:' + str(studentId) + ' 选课:' + str(request.json['id']))
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
        'SELECT achievement.*, course.name AS course_name, user.name AS student_name FROM achievement JOIN course ON achievement.course_id = course.id JOIN user ON achievement.student_id = user.id WHERE user.username=%s',
        current_user.id).fetchall()
    return render_template('my_course.html', course_infos=course_infos)


# 取消已选课程选择
@course_bp.route('/course_cancel', methods=['POST'])
@login_required
def course_cancel():
    # 如果不存在相同的记录，则插入新记录
    result1 = db.execute_sql("DELETE FROM achievement WHERE id=%s", (request.json['id']))
    result2 = db.execute_sql("UPDATE course SET selected_stu_num=selected_stu_num-1 WHERE id=%s", (request.json['id']))
    if result1 and result2:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '取消选课:' + str(request.json['id']))
        return jsonify({'success': True, 'message': "取消成功!"})
    else:
        return jsonify({'success': False, 'message': "取消选课失败!"})


@course_bp.route('/course/import', methods=['POST'])
@login_required
def import_courses():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件上传'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'})

    # 使用 pandas 读取上传的 Excel 文件流
    df = pd.read_excel(file)
    # 构建批量插入的 SQL 语句
    values = []
    for _, row in df.iterrows():
        number = row['编号'] if pd.notna(row['编号']) else ''
        name = row['课程名'] if pd.notna(row['课程名']) else ''
        credits = row['学分'] if pd.notna(row['学分']) else ''
        year = row['年度'] if pd.notna(row['年度']) else ''
        semester = row['学期'] if pd.notna(row['学期']) else ''
        startdate = row['开课时间'] if pd.notna(row['开课时间']) else 'NULL'
        enddate = row['结课时间'] if pd.notna(row['结课时间']) else 'NULL'
        teaching_time = row['授课时间'] if pd.notna(row['授课时间']) else ''
        teaching_place = row['授课地点'] if pd.notna(row['授课地点']) else ''

        teacher_number = row['授课老师编号'] if pd.notna(row['授课老师编号']) else ''
        teacher_cmd = """SELECT * from teacher WHERE number=%s"""
        teacher_params = (teacher_number)
        teacher_row = db.execute_sql(teacher_cmd, teacher_params).fetchone()
        teacher_id = teacher_row.get('id')
        if not teacher_id:
            return jsonify({'success': False, 'message': "添加失败，不存在该教师：%s" % teacher_number})

        values.append("('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', {})".format(
            number, name, credits, year, semester, startdate,
            enddate, teaching_time, teaching_place, teacher_id))
    # 拼接成 SQL 语句
    cmd = """INSERT INTO course (number, name, credits, year, semester, startdate,
			enddate, teaching_time, teaching_place, teacher_id) VALUES {};""".format(', '.join(values))
    result = db.execute_sql(cmd)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, "课程管理", '批量新增课程')
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@course_bp.route('/achievement/import', methods=['POST'])
@login_required
def import_achievements():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件上传'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'})

    # 使用 pandas 读取上传的 Excel 文件流
    df = pd.read_excel(file)
    # 构建批量插入的 SQL 语句
    values = []
    for _, row in df.iterrows():
        course_no = row['课程编号'] if pd.notna(row['课程编号']) else ''
        course_cmd = """SELECT * from course WHERE number=%s"""
        course_params = (course_no)
        course_row = db.execute_sql(course_cmd, course_params).fetchone()
        if not course_row:
            return jsonify({'success': False, 'message': "添加失败，不存在该课程：%s" % course_no})

        student_no = row['学生学号'] if pd.notna(row['学生学号']) else ''
        student_cmd = """SELECT * from user WHERE username=%s"""
        student_params = (student_no)
        student_row = db.execute_sql(student_cmd, student_params).fetchone()
        if not student_row:
            return jsonify({'success': False, 'message': "添加失败，不存在该学生：%s" % student_no})
        isExistFlag = db.execute_sql(
            "SELECT COUNT(*) AS count FROM achievement WHERE course_id = %s AND student_id = %s",
            (course_row['id'], student_row['id'])).fetchone()
        if isExistFlag and isExistFlag['count'] == 0:
            score = row['成绩'] if pd.notna(row['成绩']) else ''
            level_cmd = """SELECT * from gradelevel WHERE %s BETWEEN min_score AND max_score;"""
            level_params = (score)
            level_row = db.execute_sql(level_cmd, level_params).fetchone()
            if level_row:
                values.append("({}, {}, {}, {})".format(
                    int(score), course_row['id'], student_row['id'], level_row['id']))
            else:
                values.append("({}, {}, {})".format(
                    int(score), course_row['id'], student_row['id']))
        else:
            return jsonify({'success': False, 'message': "{}学生已登记成绩，科目：{}!".format(student_no, course_no)})
    # 拼接成 SQL 语句
    cmd = """INSERT INTO achievement (score, course_id, student_id, gradelevel_id) VALUES {};""".format(
        ', '.join(values))
    result = db.execute_sql(cmd)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, "成绩管理", '批量新增成绩')
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@course_bp.route('/gradelevel', methods=['GET'])
@login_required
def gradelevel_query():
    gradelevel_infos = db.execute_sql('SELECT * from gradelevel').fetchall()
    return render_template('gradelevel.html', gradelevel_infos=gradelevel_infos)


@course_bp.route('/gradelevel/add', methods=['POST'])
@login_required
def gradelevel_add():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    cmd = """INSERT INTO gradelevel (number, name, min_score, max_score) VALUES (%s, %s, %s, %s)"""
    params = (request.json['number'], request.json['name'], request.json['min_score'], request.json['max_score'])
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, achievement_model_name,
                         '新增成绩分级信息: ' + request.json['name'])
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@course_bp.route('/gradelevel/update', methods=['POST'])
@login_required
def gradelevel_update():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    cmd = """UPDATE gradelevel SET number=%s, name=%s, min_score=%s, max_score=%s WHERE id=%s"""
    params = (request.json['number'], request.json['name'], request.json['min_score'], request.json['max_score'],
              request.json['id'])
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, achievement_model_name,
                         '更新成绩分级信息: ' + request.json['name'])
        return jsonify({'success': True, 'message': "更新成功!"})
    else:
        return jsonify({'success': False, 'message': "更新失败!"})


@course_bp.route('/gradelevel/delete', methods=['POST'])
@login_required
def gradelevel_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    if 'id' in request.json:
        achievement_cmd = """SELECT * from achievement WHERE gradelevel_id=%s"""
        achievement_params = (request.json['id'])
        achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
        if achievement_row:
            return jsonify({'success': False, 'message': "存在该分级对应的成绩，请更改后再删除"})
        cmd = "DELETE FROM gradelevel WHERE id=%s;"
        result = db.execute_sql(cmd, request.json['id'])
        ids_to_delete = request.json['id']
    elif 'ids' in request.json:
        ids_to_delete = request.json['ids']
        for id in ids_to_delete:
            achievement_cmd = """SELECT * from achievement WHERE gradelevel_id=%s"""
            achievement_params = (id)
            achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
            if achievement_row:
                return jsonify({'success': False, 'message': "存在该分级对应的成绩，请更改后再删除"})
        # 构建 SQL 语句
        placeholders = ', '.join(['%s'] * len(ids_to_delete))
        cmd = f"DELETE FROM gradelevel WHERE id IN ({placeholders})"
        result = db.execute_sql(cmd, ids_to_delete)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, achievement_model_name, '删除成绩分级: ' + str(ids_to_delete))
        return jsonify({'success': True, 'message': "删除成功!"})
    else:
        return jsonify({'success': False, 'message': "删除失败!"})


@course_bp.route('/average', methods=['GET'])
@login_required
def average_query():
    if "year" not in request.args and "semester" not in request.args:
        return render_template("average.html", average_infos=[])
    else:
        year = request.args.get('year')
        semester = request.args.get('semester')
        if semester:
            where_sql = """c.year='{}' AND c.semester='{}'""".format(year, semester)
        else:
            where_sql = """c.year='{}'""".format(year)
        average_sql = """SELECT
                            u.username,
                            u.name,
                            ROUND(AVG(a.score), 2) AS average_score
                        FROM
                            course c
                                JOIN
                            achievement a ON c.id = a.course_id
                                JOIN
                            user u ON a.student_id = u.id
                        WHERE
                            {} 
                        GROUP BY
                            u.username, u.name
                        ORDER BY
                            average_score DESC;""".format(where_sql)
        average_infos = db.execute_sql(average_sql).fetchall()
        return jsonify({"rows": average_infos, "total": len(average_infos)})


@course_bp.route('/achievement_search', methods=['GET'])
@login_required
def student_score_query():
    year = request.args.get('year')
    semester = request.args.get('semester')
    student_no = request.args.get('student_no')
    if semester:
        where_sql = """c.year='{}' AND c.semester='{}' AND u.username='{}'""".format(year, semester, student_no)
    else:
        where_sql = """c.year='{}' AND u.username='{}'""".format(year, student_no)
    score_sql = """SELECT 
                        c.year AS course_year,
                        c.semester AS course_semester,
                        c.number AS course_number,
                        c.name AS course_name,
                        u.username AS user_username,
                        u.name AS user_name,
                        a.score AS achievement_score
                    FROM 
                        course c
                    JOIN 
                        achievement a ON c.id = a.course_id
                    JOIN 
                        user u ON a.student_id = u.id
                    WHERE {}""".format(where_sql)
    score_infos = db.execute_sql(score_sql).fetchall()
    return jsonify({"rows": score_infos, "total": len(score_infos)})


@course_bp.route('/progress', methods=['GET'])
@login_required
def progress_query():
    if "year" not in request.args:
        return render_template("progress.html", progress_infos=[])
    else:
        year = request.args.get('year')
        progress_sql = """WITH semester_scores AS (
                            SELECT 
                                u.username,
                                u.name,
                                c.semester,
                                ROUND(AVG(a.score), 2) AS average_score
                            FROM 
                                course c
                            JOIN 
                                achievement a ON c.id = a.course_id
                            JOIN 
                                user u ON a.student_id = u.id
                            WHERE 
                                c.year = '{}'  -- 将 '2024' 替换为实际的年份
                            GROUP BY 
                                u.username, u.name, c.semester
                        ),
                        semester_diff AS (
                            SELECT 
                                username,
                                name,
                                MAX(CASE WHEN semester = '3' THEN average_score ELSE NULL END) AS semester_3_score,
                                MAX(CASE WHEN semester = '2' THEN average_score ELSE NULL END) AS semester_2_score,
                                MAX(CASE WHEN semester = '1' THEN average_score ELSE NULL END) AS semester_1_score,
                                MAX(CASE WHEN semester = '3' THEN average_score ELSE NULL END) -
                                MAX(CASE WHEN semester = '1' THEN average_score ELSE NULL END) AS score_diff
                            FROM 
                                semester_scores
                            GROUP BY 
                                username, name
                        )
                        SELECT 
                            username,
                            name,
                            semester_3_score,
                            semester_2_score,
                            semester_1_score,
                            score_diff
                        FROM 
                            semester_diff
                        ORDER BY 
                            score_diff DESC;""".format(year)
        progress_infos = db.execute_sql(progress_sql).fetchall()
        return jsonify({"rows": progress_infos, "total": len(progress_infos)})
