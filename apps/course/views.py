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
        major = request.args.get('major')
        query = request.args.get('query')
        course_name = request.args.get('course_name')

        if major:
            sql = '''
                SELECT course.*, major.name AS major
                FROM course
                JOIN major ON course.major_id = major.id
                WHERE major.name = %s
                ORDER BY course.id
            '''
            course_infos = db.execute_sql(sql, (major,)).fetchall()
            return jsonify(course_infos)

        elif query is not None:
            course_infos = db.execute_sql(
                'SELECT * FROM course WHERE number LIKE %s OR name LIKE %s',
                ('%' + query + '%', '%' + query + '%')
            ).fetchall()
            return jsonify({"rows": course_infos, "total": len(course_infos)})

        elif course_name is not None:
            course_info = db.execute_sql(
                'SELECT * FROM course WHERE name = %s', (course_name,)
            ).fetchone()
            if course_info:
                return jsonify({'success': True, 'course_info': course_info})
            else:
                return jsonify({'success': False, 'message': "不存在该课程"})

        else:
            course_infos = db.execute_sql(
                'SELECT course.*, major.name AS major FROM course JOIN major ON course.major_id = major.id ORDER BY course.id'
            ).fetchall()
            return render_template('course.html', course_infos=course_infos)


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
    # cmd1 = """SELECT * from teacher WHERE number=%s"""
    # params1 = (request.json['teachernum'])
    # result = db.execute_sql(cmd1, params1)
    # row = result.fetchone()
    # if not row:
    #     return jsonify({'success': False, 'message': "不存在该教师编号!"})
    # teacher_name = row['name']
    name = request.json.get('name')
    major_name = request.json.get('major')

    # 检查是否已存在同名课程
    cursor = db.execute_sql("SELECT id FROM course WHERE name = %s", (name,))
    if cursor.fetchone():
        return jsonify({'success': False, 'message': "已存在同名课程，无法重复添加！"})

    # 查找 major_id
    cursor = db.execute_sql("SELECT id FROM major WHERE name = %s", (major_name,))
    major = cursor.fetchone()
    if not major:
        return jsonify({'success': False, 'message': "专业名称不存在！"})
    major_id = major['id']

    # 解析学分为整数
    try:
        credits = int(request.json.get('credits')) if request.json.get('credits') else None
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': "学分格式错误，必须为整数"})

    # 插入新课程记录
    cmd = """
        INSERT INTO course(name, credits, category, startdate, enddate,
                           teaching_time, teaching_place, teacher_name, major_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        name,
        credits,
        request.json.get('category'),
        request.json.get('startdate'),
        request.json.get('enddate'),
        request.json.get('teachingTime'),
        request.json.get('teachingPlace'),
        request.json.get('teacher_name'),
        major_id
    )

    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, "课程管理", '新增课程: ' + name)
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@course_bp.route('/course/update', methods=['POST'])
@login_required
def course_update():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})

    data = request.get_json()
    course_name = data.get("name")
    if not course_name:
        return jsonify({'success': False, 'message': '课程名称不能为空'})

    # 查找课程原始记录
    cursor = db.execute_sql("SELECT * FROM course WHERE name = %s", (course_name,))
    existing = cursor.fetchone()
    if not existing:
        return jsonify({'success': False, 'message': '未找到该课程'})

    # 解析学分为整数
    try:
        credits = int(request.json.get('credits')) if request.json.get('credits') else None
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': "学分格式错误，必须为整数"})

    update_dict = {}
    if data.get("credits") != '' and data.get("credits") != existing.get("credits"):
        update_dict['credits'] = data.get("credits")
    if data.get("category") != '' and data.get("category") != existing.get("category"):
        update_dict['category'] = data.get("category")
    if data.get("startdate") != '' and data.get("startdate") != str(existing.get("startdate")):
        update_dict['startdate'] = data.get("startdate")
    if data.get("enddate") != '' and data.get("enddate") != str(existing.get("enddate")):
        update_dict['enddate'] = data.get("enddate")
    if data.get("updateTime") != '' and data.get("updateTime") != existing.get("teaching_time"):
        update_dict['teaching_time'] = data.get("updateTime")
    if data.get("updatePlace") != '' and data.get("updatePlace") != existing.get("teaching_place"):
        update_dict['teaching_place'] = data.get("updatePlace")
    if data.get("teacher_name") != '' and data.get("teacher_name") != existing.get("teacher_name"):
        update_dict['teacher_name'] = data.get("teacher_name")

    # 专业字段检查
    if data.get("major") != '':
        cursor = db.execute_sql("SELECT id FROM major WHERE name = %s", (data.get("major"),))
        major_row = cursor.fetchone()
        if not major_row:
            return jsonify({'success': False, 'message': '无效的专业名称'})
        if major_row['id'] != existing.get("major_id"):
            update_dict['major_id'] = major_row['id']

    if not update_dict:
        return jsonify({'success': True, 'message': '数据无变动，无需更新。'})

    set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
    cmd = f"UPDATE course SET {set_clause} WHERE name = %s"
    params = list(update_dict.values()) + [course_name]
    result = db.execute_sql(cmd, params)

    if result:
        insert_audit_log(request.remote_addr, current_user.id, "课程管理", '更新课程: ' + course_name)
        return jsonify({'success': True, 'message': "更新成功!"})
    else:
        return jsonify({'success': False, 'message': "更新失败!"})


@course_bp.route('/course/delete', methods=['POST'])
@login_required
def course_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    failed_ids = []
    if 'id' in request.json:
        ids_to_delete = [request.json['id']]
    elif 'ids' in request.json:
        ids_to_delete = request.json['ids']
    else:
        return jsonify({'success': False, 'message': '未提供课程 ID'})
    # 检查是否存在依赖的成绩记录
    for cid in ids_to_delete:
        cursor = db.execute_sql("SELECT id FROM achievement WHERE course_id = %s", (cid,))
        if cursor.fetchone():
            failed_ids.append(cid)
    if failed_ids:
        return jsonify({
            'success': False,
            'message': f"以下课程存在成绩记录，无法删除：{failed_ids}"
        })
    # 删除课程
    placeholders = ', '.join(['%s'] * len(ids_to_delete))
    delete_sql = f"DELETE FROM course WHERE id IN ({placeholders})"
    result = db.execute_sql(delete_sql, ids_to_delete)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, "课程管理", '删除课程条目: ' + str(ids_to_delete))
        return jsonify({'success': True, 'message': "删除成功!"})
    else:
        return jsonify({'success': False, 'message': "删除失败!"})


# 查询成绩
@course_bp.route('/achievement', methods=['GET'])
@login_required
def achievement_query():
    if request.args.get('query') is None:
        # 管理员角色查询
        if session['role'] in (1, 2):
            sql = """
            SELECT
              a.*,
              c.name          AS course_name,
              m.name          AS course_major,
              c.teacher_name  AS teacher_name,
              u.username      AS student_no,
              u.name          AS student_name,
              gl.name         AS gradelevel_name,
              gl.gpa          AS gpa
            FROM achievement a
            JOIN course      c  ON a.course_id = c.id
            JOIN major       m  ON c.major_id = m.id
            JOIN user        u  ON a.student_id = u.id
            /* 根据 score 落在哪个区间，关联出对应的 gradelevel */
            JOIN gradelevel  gl ON a.score BETWEEN gl.min_score AND gl.max_score
            ORDER BY a.id
            """
            achievement_infos = db.execute_sql(sql).fetchall()
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


def _lookup_student_and_course(student_no, course_name):
    """返回 (student_row, course_row, error_message)"""
    student = db.execute_sql("SELECT id, username, name FROM `user` WHERE username=%s", (student_no,)).fetchone()
    if not student:
        return None, None, "学生信息不存在!"

    # 查课程（带上 major_id）
    course = db.execute_sql(
        "SELECT c.id, c.name, c.teacher_name, c.major_id, m.name AS course_major "
        "FROM course c "
        "JOIN major m ON c.major_id=m.id "
        "WHERE c.name=%s",
        (course_name,)
    ).fetchone()
    if not course:
        return None, None, "课程信息不存在!"

    # 检查 student_major 关联
    assoc = db.execute_sql(
        "SELECT 1 FROM student_major WHERE student_id=%s AND major_id=%s",
        (student['id'], course['major_id'])
    ).fetchone()
    if not assoc:
        return None, None, "学生不属于该课程所属专业!"

    return student, course, None


# 添加成绩
@course_bp.route('/achievement/add', methods=['POST'])
@login_required
def achievement_add():
    if session.get('role') != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})

    data = request.json
    student_no = data['studentNo']
    course_name = data['courseName']
    year = data['year']
    semester = data['semester']
    score = data['score']

    student_row, course_row, err = _lookup_student_and_course(student_no, course_name)
    if err:
        return jsonify(success=False, message=err)

    # 去重
    exists = db.execute_sql(
        "SELECT 1 FROM achievement "
        "WHERE course_id=%s AND student_id=%s AND year=%s AND semester=%s",
        (course_row['id'], student_row['id'], year, semester)
    ).fetchone()
    if exists:
        return jsonify({'success': False, 'message': "该条成绩已存在!"})

    sql = """
        INSERT INTO achievement(score, course_id, student_id, year, semester)
        VALUES (%s,%s,%s,%s,%s)
    """
    res = db.execute_sql(
        sql,
        (score, course_row['id'], student_row['id'], year, semester)
    )
    if not res:
        return jsonify({'success': False, 'message': "添加失败!"})

    # 计算分级、绩点
    level_row = db.execute_sql(
        "SELECT name, gpa FROM gradelevel WHERE %s BETWEEN min_score AND max_score",
        (score,)
    ).fetchone()

    info = {
        'course_name': course_row['name'],
        'course_major': course_row['course_major'],
        'teacher_name': course_row['teacher_name'],
        'student_no': student_row['username'],
        'student_name': student_row['name'],
        'gradelevel_name': level_row['name'] if level_row else None,
        'gpa': float(level_row['gpa']) if level_row else None
    }

    insert_audit_log(
        request.remote_addr, current_user.id, achievement_model_name,
        f"添加成绩: {course_row['name']}-{student_row['name']}-{score}"
    )
    return jsonify({'success': True, 'message': "添加成功!", 'achievement_info': info})


@course_bp.route('/achievement/update', methods=['POST'])
@login_required
def achievement_update():
    if session.get('role') != 1:
        return jsonify(success=False, message='没有操作权限！')

    data = request.json
    rec_id = data['id']
    student_no = data['studentNo']
    course_name = data['courseName']
    year = data['year']
    semester = data['semester']
    new_score = data['newScore']

    orig = db.execute_sql("SELECT score, year, semester FROM achievement WHERE id=%s", (rec_id,)).fetchone()
    if not orig:
        return jsonify(success=False, message="要更新的记录不存在!")

    if float(orig['score']) == float(new_score) and orig['year'] == year and orig['semester'] == semester:
        return jsonify(success=False, message="数据未更改!")

    student, course, err = _lookup_student_and_course(student_no, course_name)
    if err:
        return jsonify(success=False, message=err)

    res = db.execute_sql(
        "UPDATE achievement SET score=%s, year=%s, semester=%s WHERE id=%s",
        (new_score, year, semester, rec_id)
    )
    if not res:
        return jsonify(success=False, message="更新失败!")

    level_row = db.execute_sql("SELECT name, gpa FROM gradelevel WHERE %s BETWEEN min_score AND max_score", (new_score,)).fetchone()

    # 6. 组装返回
    info = {
        'course_name': course['name'],
        'course_major': course['course_major'],
        'teacher_name': course['teacher_name'],
        'student_no': student['username'],
        'student_name': student['name'],
        'gradelevel_name': level_row['name'] if level_row else None,
        'gpa': float(level_row['gpa']) if level_row else None
    }
    insert_audit_log(
        request.remote_addr, current_user.id, achievement_model_name,
        f"更新成绩: {course['name']}-{student['name']}-{new_score}"
    )
    return jsonify(success=True, message="更新成功!", achievement_info=info)


@course_bp.route('/achievement/delete', methods=['POST'])
@login_required
def achievement_delete():
    if session.get('role') != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    ids = []
    if 'id' in request.json:
        ids = [request.json['id']]
    elif 'ids' in request.json:
        ids = request.json['ids']
    else:
        return jsonify({'success': False, 'message': "未提供要删除的ID!"})
    # 执行删除
    placeholders = ",".join(["%s"]*len(ids))
    sql = f"DELETE FROM achievement WHERE id IN ({placeholders})"
    res = db.execute_sql(sql, tuple(ids))
    if not res:
        return jsonify({'success': False, 'message': "删除失败!"})
    insert_audit_log(request.remote_addr, current_user.id, achievement_model_name, f"删除成绩条目: {ids}" )
    return jsonify({'success': True, 'message': "删除成功!"})


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
    added = 0
    skipped = []
    for _, row in df.iterrows():
        name = str(row['课程名']).strip() if pd.notna(row['课程名']) else ''
        if not name:
            continue
        # 检查是否已存在该课程
        cursor = db.execute_sql("SELECT id FROM course WHERE name = %s", (name,))
        if cursor.fetchone():
            skipped.append(name)
            continue
        try:
            credits = int(row['学分']) if pd.notna(row['学分']) else None
        except (ValueError, TypeError):
            skipped.append(f"{name}（学分无效）")
            continue
        category = row['课程类别'] if pd.notna(row['课程类别']) else ''
        startdate = row['开课时间'] if pd.notna(row['开课时间']) else None
        enddate = row['结课时间'] if pd.notna(row['结课时间']) else None
        teaching_time = row['授课时间'] if pd.notna(row['授课时间']) else ''
        teaching_place = row['授课地点'] if pd.notna(row['授课地点']) else ''
        teacher_name = row['授课老师姓名'] if pd.notna(row['授课老师姓名']) else ''

        major_name = row['所属专业'] if pd.notna(row['所属专业']) else ''
        cursor = db.execute_sql("SELECT id FROM major WHERE name = %s", (major_name,))
        major = cursor.fetchone()
        if not major:
            skipped.append(f"{name}（专业未找到: {major_name}）")
            continue

        db.execute_sql("""
            INSERT INTO course (name, credits, category, startdate, enddate, teaching_time, teaching_place, teacher_name, major_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name, credits, category, startdate, enddate, teaching_time, teaching_place, teacher_name, major['id']
        ))
        added += 1

    if added > 0:
        insert_audit_log(request.remote_addr, current_user.id, "课程管理", f"批量新增课程 {added} 门")

    if skipped:
        return jsonify({
            'success': True,
            'message': f"成功导入 {added} 门课程，以下课程跳过：{', '.join(skipped)}"
        })
    else:
        return jsonify({'success': True, 'message': f"成功导入 {added} 门课程"})


@course_bp.route('/achievement/import', methods=['POST'])
@login_required
def import_achievements():
    if session.get('role') != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})

    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '没有文件上传'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '文件名为空'})

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return jsonify({'success': False, 'message': f'文件读取失败: {str(e)}'})

    success_count = 0
    error_list = []

    for idx, row in df.iterrows():
        try:
            # 读取每行数据
            student_no = str(row['学生学号']).strip() if pd.notna(row['学生学号']) else ''
            course_name = str(row['课程名称']).strip() if pd.notna(row['课程名称']) else ''
            year = str(row['学年']).strip() if pd.notna(row['学年']) else ''
            semester = str(row['学期']).strip() if pd.notna(row['学期']) else ''
            score = float(row['成绩']) if pd.notna(row['成绩']) else None

            if not student_no or not course_name or not year or not semester or score is None:
                error_list.append(f"第{idx+2}行: 缺少必要字段")
                continue

            student_row, course_row, err = _lookup_student_and_course(student_no, course_name)
            if err:
                error_list.append(f"第{idx+2}行: {err}")
                continue

            # 检查成绩是否已存在
            exists = db.execute_sql(
                "SELECT 1 FROM achievement WHERE course_id=%s AND student_id=%s AND year=%s AND semester=%s",
                (course_row['id'], student_row['id'], year, semester)
            ).fetchone()
            if exists:
                error_list.append(f"第{idx+2}行: 成绩已存在")
                continue

            # 插入成绩
            insert_sql = """
                INSERT INTO achievement (score, course_id, student_id, year, semester)
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_sql(insert_sql, (score, course_row['id'], student_row['id'], year, semester))
            success_count += 1

        except Exception as e:
            error_list.append(f"第{idx+2}行: 异常 - {str(e)}")

    if success_count > 0:
        insert_audit_log(request.remote_addr, current_user.id, "成绩管理", f"批量新增成绩 {success_count} 条")

    return jsonify({
        'success': True if success_count else False,
        'message': f"成功导入 {success_count} 条成绩，失败 {len(error_list)} 条。",
        'error_details': error_list
    })



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
    year = request.args.get('year')
    semester = request.args.get('semester')
    student_no = request.args.get('student_no')

    if semester and not year:
        return jsonify({"rows": [], "total": 0, "message": "学期不能单独查询，必须选择学年"})

    where_clauses = []
    params = []

    if year:
        where_clauses.append("a.year = %s")
        params.append(year)
    if semester:
        where_clauses.append("a.semester = %s")
        params.append(semester)
    if student_no:
        where_clauses.append("u.username = %s")
        params.append(student_no)

    if not where_clauses:
        return render_template("average.html", average_infos=[])

    where_sql = " AND ".join(where_clauses)

    average_sql = f"""
        SELECT
            u.username,
            u.name,
            ROUND(AVG(a.score), 2) AS average_score,
            SUM(c.credits) AS total_credits,
            ROUND(AVG(gl.gpa), 2) AS average_gpa
        FROM
            achievement a
        JOIN
            course c ON a.course_id = c.id
        JOIN
            user u ON a.student_id = u.id
        JOIN
            gradelevel gl ON a.score BETWEEN gl.min_score AND gl.max_score
        WHERE
            {where_sql}
        GROUP BY
            u.username, u.name
        ORDER BY
            average_score DESC
    """

    average_infos = db.execute_sql(average_sql, tuple(params)).fetchall()
    return jsonify({"rows": average_infos, "total": len(average_infos)})



@course_bp.route('/achievement_search', methods=['GET'])
@login_required
def student_score_query():
    year = request.args.get('year')
    semester = request.args.get('semester')
    student_no = request.args.get('student_no')

    if semester and not year:
        return jsonify({"rows": [], "total": 0, "message": "学期不能单独查询，必须选择学年"})

    if not year and not student_no:
        return jsonify({"rows": [], "total": 0, "message": "请至少提供 年度 或 学生学号"})

    where_clauses = []
    params = []

    if year:
        where_clauses.append("a.year = %s")
        params.append(year)
    if semester:
        where_clauses.append("a.semester = %s")
        params.append(semester)
    if student_no:
        where_clauses.append("u.username = %s")
        params.append(student_no)

    where_sql = " AND ".join(where_clauses)

    sql = f"""
            SELECT 
                a.year AS course_year,
                a.semester AS course_semester,
                c.name AS course_name,
                c.category AS course_cate,
                c.credits AS course_credits,
                u.username AS user_username,
                u.name AS user_name,
                a.score AS achievement_score,
                gl.gpa AS gradelevel_gpa
            FROM 
                achievement a
            JOIN 
                course c ON a.course_id = c.id
            JOIN 
                user u ON a.student_id = u.id
            JOIN 
                gradelevel gl ON a.score BETWEEN gl.min_score AND gl.max_score
            WHERE 
                {where_sql}
            ORDER BY 
                a.year DESC, a.semester DESC, c.name ASC
    """

    score_infos = db.execute_sql(sql, tuple(params)).fetchall()
    return jsonify({"rows": score_infos, "total": len(score_infos)})


@course_bp.route('/progress', methods=['GET'])
@login_required
def progress_query():
    if 'year' not in request.args:
        return render_template("progress.html", progress_infos=[])

    year = request.args.get('year')

    sql = """
        WITH semester_scores AS (
            SELECT 
                u.username,
                u.name,
                a.semester,
                ROUND(AVG(a.score), 2) AS average_score
            FROM 
                achievement a
            JOIN 
                user u ON a.student_id = u.id
            WHERE 
                a.year = %s
            GROUP BY 
                u.username, u.name, a.semester
        ),
        semester_diff AS (
            SELECT 
                username,
                name,
                MAX(CASE WHEN semester = '3' THEN average_score ELSE NULL END) AS semester_3_score,
                MAX(CASE WHEN semester = '2' THEN average_score ELSE NULL END) AS semester_2_score,
                MAX(CASE WHEN semester = '1' THEN average_score ELSE NULL END) AS semester_1_score,
                (MAX(CASE WHEN semester = '3' THEN average_score ELSE 0 END) -
                 MAX(CASE WHEN semester = '1' THEN average_score ELSE 0 END)) AS score_diff
            FROM 
                semester_scores
            GROUP BY 
                username, name
        )
        SELECT 
            username,
            name,
            semester_1_score,
            semester_2_score,
            semester_3_score,
            score_diff
        FROM 
            semester_diff
        ORDER BY 
            score_diff DESC;
    """

    progress_infos = db.execute_sql(sql, (year,)).fetchall()
    return jsonify({"rows": progress_infos, "total": len(progress_infos)})
