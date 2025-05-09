#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-

from flask_login import login_required, current_user
from exts import db
from flask import request, render_template, Blueprint, jsonify, session

from exts.common import insert_audit_log

major_bp = Blueprint('major_bp', __name__, url_prefix='')
model_name = '专业'


@major_bp.route('/major', methods=['GET'])
@login_required
def major_query():
    major_infos = db.execute_sql('SELECT * from major ORDER BY id').fetchall()
    return render_template('major.html', major_infos=major_infos)


@major_bp.route('/major_list', methods=['GET'])
@login_required
def major_list():
    student_no = request.args.get('student_no')
    if not student_no:
        sql = "SELECT name FROM major ORDER BY id ASC"
        majors = db.execute_sql(sql).fetchall()
        return jsonify(majors)
    user = db.execute_sql(
        "SELECT id FROM user WHERE username = %s", (student_no,)
    ).fetchone()

    if not user:
        return jsonify({'success': False, 'message': '找不到该学生学号'})

    student_id = user['id']

    # 查询 student_major 表，找该学生关联的专业
    sql = """
        SELECT major.name
        FROM student_major
        JOIN major ON student_major.major_id = major.id
        WHERE student_major.student_id = %s
        ORDER BY major.id ASC
    """
    majors = db.execute_sql(sql, (student_id,)).fetchall()

    if not majors:
        return jsonify({'success': False, 'message': '该学生没有绑定专业'})

    major_list = [m['name'] for m in majors]
    return jsonify({'success': True, 'majors': major_list})


@major_bp.route('/major/add', methods=['POST'])
@login_required
def add_major():
    data = request.get_json()
    name = data.get('name')
    level = data.get('level')

    if not name:
        return jsonify({'success': False, 'message': '专业名称不能为空'})

    # 检查是否已存在
    existing = db.execute_sql("SELECT * FROM major WHERE name = %s", (name,)).fetchone()
    if existing:
        return jsonify({'success': False, 'message': '该专业已存在'})

    result = db.execute_sql("INSERT INTO major (name, level) VALUES (%s, %s)", (name, level))
    if result:
        return jsonify({'success': True, 'message': '添加成功'})
    else:
        return jsonify({'success': False, 'message': '添加失败'})


@major_bp.route('/major/update', methods=['POST'])
@login_required
def update_major():
    data = request.get_json()
    name = data.get('name')
    level = data.get('level')
    major_id = data.get('id')

    if not major_id:
        return jsonify({'success': False, 'message': '未指定要更新的专业ID'})

    # 查询原始记录
    existing = db.execute_sql("SELECT * FROM major WHERE id = %s", (major_id,)).fetchone()
    if not existing:
        return jsonify({'success': False, 'message': '该专业不存在'})

    if existing['name'] == name and existing['level'] == level:
        return jsonify({'success': True, 'message': '无变动，无需更新'})

    result = db.execute_sql(
        "UPDATE major SET name = %s, level = %s WHERE id = %s",
        (name, level, major_id)
    )
    if result:
        return jsonify({'success': True, 'message': '更新成功'})
    else:
        return jsonify({'success': False, 'message': '更新失败'})


@major_bp.route('/major/delete', methods=['POST'])
@login_required
def delete_major():
    data = request.get_json()

    ids = []
    if 'id' in data:
        ids = [data['id']]
    elif 'ids' in data:
        ids = data['ids']

    if not ids:
        return jsonify({'success': False, 'message': '未指定要删除的专业'})

    failed = []
    for mid in ids:
        # 判断该专业是否被课程引用
        ref = db.execute_sql("SELECT id FROM course WHERE major_id = %s", (mid,)).fetchone()
        if ref:
            major_name = db.execute_sql("SELECT name FROM major WHERE id = %s", (mid,)).fetchone()
            if major_name:
                failed.append(major_name['name'])

    if failed:
        return jsonify({'success': False, 'message': f'以下专业已关联课程，无法删除：{failed}，请删除专业下所有课程后再删除'})

    placeholders = ','.join(['%s'] * len(ids))
    sql = f"DELETE FROM major WHERE id IN ({placeholders})"
    result = db.execute_sql(sql, ids)

    if result:
        return jsonify({'success': True, 'message': '删除成功'})
    else:
        return jsonify({'success': False, 'message': '删除失败'})


@major_bp.route('/student_course', methods=['GET'])
@login_required
def student_course_list():
    student_no = request.args.get('student_no')
    major_name = request.args.get('major_name')  # 选的专业名字，可以为空
    status = request.args.get('status')      # repaired / unrepaired / 空

    if not student_no and not major_name and not status:
        return render_template("student_course.html", student_course_infos=[])

    if not student_no:
        return jsonify({'success': False, 'message': '学生学号不能为空', 'rows': []})

    # 查 student_id
    student = db.execute_sql("SELECT * FROM user WHERE username = %s", (student_no,)).fetchone()
    if not student:
        return jsonify({'success': False, 'message': '学生不存在', 'rows': []})
    student_id = student['id']

    # 查专业 id，如果传了 major_name
    if major_name:
        major = db.execute_sql("SELECT id FROM major WHERE name = %s", (major_name,)).fetchone()
        if not major:
            return jsonify({'success': False, 'message': '专业不存在', 'rows': []})
        major_id = major['id']

        check_link = db.execute_sql(
            "SELECT id FROM student_major WHERE student_id = %s AND major_id = %s",
            (student_id, major_id)
        ).fetchone()
        if not check_link:
            return jsonify({'success': False, 'message': '该学生未选修该专业', 'rows': []})

        course_sql = "SELECT * FROM course WHERE major_id = %s"
        course_params = (major_id,)
    else:
        # 不选专业时，查这个学生所有 student_major 对应的专业下的课程
        major_ids = db.execute_sql(
            "SELECT major_id FROM student_major WHERE student_id = %s", (student_id,)
        ).fetchall()
        major_id_list = [str(m['major_id']) for m in major_ids]
        if not major_id_list:
            return jsonify({'success': False, 'message': '该学生未关联任何专业', 'rows': []})
        course_sql = f"SELECT * FROM course WHERE major_id IN ({','.join(major_id_list)})"
        course_params = ()

    courses = db.execute_sql(course_sql, course_params).fetchall()

    # 准备数据
    result_rows = []

    for course in courses:
        # 查 achievement
        achievement = db.execute_sql(
            "SELECT a.score, a.year, a.semester, gl.name AS gradelevel_name "
            "FROM achievement a "
            "LEFT JOIN gradelevel gl ON a.score BETWEEN gl.min_score AND gl.max_score "
            "WHERE a.course_id = %s AND a.student_id = %s",
            (course['id'], student_id)
        ).fetchone()

        repaired_status = 'repaired' if achievement else 'unrepaired'

        # 只保留符合 status 筛选条件的
        if status and status != repaired_status:
            continue

        result_rows.append({
            'student_no': student['username'],
            'student_name': student['name'],
            'course_name': course['name'],
            'major': db.execute_sql("SELECT name FROM major WHERE id = %s", (course['major_id'],)).fetchone()['name'],
            'enrollment_date': student['enrollment_date'],
            'teacher_name': course['teacher_name'],
            'year': achievement['year'] if achievement else '',
            'semester': achievement['semester'] if achievement else '',
            'score': achievement['score'] if achievement else '',
            'gradelevel_name': achievement['gradelevel_name'] if achievement else '',
            'status': repaired_status
        })

    return jsonify({'success': True, 'rows': result_rows})


@major_bp.route('/major_progress', methods=['GET'])
@login_required
def student_major_progress():
    YEAR_LIMIT = 7
    progress_type = request.args.get('type')

    if not progress_type:
        return render_template("major_progress.html", student_course_infos=[])
    # 七年内未完成所有专业课程
    if progress_type == '1':
        sql = """
            SELECT
                u.username AS student_no,
                u.name AS student_name,
                u.enrollment_date,
                m.name AS major,
                COUNT(c.id) AS total_courses,
                COUNT(DISTINCT a.course_id) AS finished_courses,
                (COUNT(c.id) - COUNT(DISTINCT a.course_id)) AS unfinished_courses
            FROM user u
            JOIN student_major sm ON u.id = sm.student_id
            JOIN major m ON sm.major_id = m.id
            JOIN course c ON c.major_id = m.id
            LEFT JOIN achievement a ON a.student_id = u.id AND a.course_id = c.id
            WHERE u.role_id = 3
              AND TIMESTAMPDIFF(YEAR, u.enrollment_date, CURDATE()) >= %s
            GROUP BY u.id, m.name
            HAVING finished_courses < total_courses
        """
        rows = db.execute_sql(sql, (YEAR_LIMIT,)).fetchall()
        return jsonify({"success": True, "rows": rows})

    return jsonify({"success": False, "message": "不支持的进度类型"})
