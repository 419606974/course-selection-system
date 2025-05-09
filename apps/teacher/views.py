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
from flask import request, render_template, Blueprint, jsonify, session

from exts.common import insert_audit_log
import pandas as pd

teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='')
model_name = '教师管理'


@teacher_bp.route('/teacher', methods=['GET'])
@login_required
def teacher_query():
    if request.args.get('query') is None and request.args.get('teacher_no') is None:
        teacher_infos = db.execute_sql('SELECT * from teacher').fetchall()
        return render_template('teacher.html', teacher_infos=teacher_infos)
    elif request.args.get('query') is not None:
        teacher_infos = db.execute_sql(
            'SELECT * from teacher where number like %s or username like %s or name like %s or phone like %s or email like %s',
            ('%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%',
             '%' + request.args.get('query') + '%',
             '%' + request.args.get('query') + '%', '%' + request.args.get('query') + '%')).fetchall()
        return jsonify({"rows": teacher_infos, "total": len(teacher_infos)})
    elif request.args.get('teacher_no') is not None:
        teacher_info = db.execute_sql(
            'SELECT * from teacher where number=%s', (request.args.get('teacher_no'))).fetchone()
        if teacher_info:
            return jsonify({'success': True, 'teacher_info': teacher_info})
        else:
            return jsonify({'success': False, 'message': "不存在该教师"})


@teacher_bp.route('/teacher/add', methods=['POST'])
@login_required
def teacher_add():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    cmd = """INSERT INTO teacher(number, username, name, education, password, sex, phone, email, `rank`, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    params = (request.json['number'], request.json['username'], request.json['name'], request.json['education'],
			  request.json['password'], request.json['sex'], request.json['phone'], request.json['email'],
			  request.json['rank'], request.json['description'])
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '新增教师信息: ' + request.json['username'])
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@teacher_bp.route('/teacher/update', methods=['POST'])
@login_required
def teacher_update():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    update_dict = {}
    # 根据request.get_json()中的数据构建一个动态的SQL更新语句
    if request.get_json()["number"] != '':
        update_dict.update({'number': request.get_json()["number"]})
    if request.get_json()["name"] != '':
        update_dict.update({'name': request.get_json()["name"]})
    if request.get_json()["education"] != '':
        update_dict.update({'education': request.get_json()["education"]})
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
        insert_audit_log(request.remote_addr, current_user.id, model_name, '更新教师信息: ' + request.json['username'])
        return jsonify({'success': True, 'message': "更新成功!"})
    else:
        return jsonify({'success': False, 'message': "更新失败!"})


@teacher_bp.route('/teacher/delete', methods=['POST'])
@login_required
def teacher_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    if 'id' in request.json:
        course_cmd = """SELECT * from course WHERE teacher_id=%s"""
        course_params = (request.json['id'])
        course_row = db.execute_sql(course_cmd, course_params).fetchone()
        if course_row:
            return jsonify({'success': False, 'message': "存在该老师对应的课程，请更改后再删除"})
        cmd = "DELETE FROM teacher WHERE id=%s;"
        result = db.execute_sql(cmd, request.json['id'])
        ids_to_delete = request.json['id']
    elif 'ids' in request.json:
        ids_to_delete = request.json['ids']
        for id in ids_to_delete:
            course_cmd = """SELECT * from course WHERE teacher_id=%s"""
            course_params = (id)
            course_row = db.execute_sql(course_cmd, course_params).fetchone()
            if course_row:
                return jsonify({'success': False, 'message': "存在该老师对应的课程，请更改后再删除"})
        # 构建 SQL 语句
        placeholders = ', '.join(['%s'] * len(ids_to_delete))
        cmd = f"DELETE FROM teacher WHERE id IN ({placeholders})"
        result = db.execute_sql(cmd, ids_to_delete)

    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '删除教师信息: ' + str(ids_to_delete))
        return jsonify({'success': True, 'message': "删除成功!"})
    else:
        return jsonify({'success': False, 'message': "删除失败!"})


@teacher_bp.route('/teacher/import', methods=['POST'])
@login_required
def import_teachers():
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
        if row['性别'] == '男':
            sex = 1
        elif row['性别'] == '女':
            sex = 0
        else:
            sex = 2
        number = row['编号'] if pd.notna(row['编号']) else ''
        name = row['姓名'] if pd.notna(row['姓名']) else ''
        username = row['编号'] if pd.notna(row['编号']) else ''
        password = row['编号'] if pd.notna(row['编号']) else ''
        rank = row['类型'] if pd.notna(row['类型']) else ''
        education = row['学历'] if pd.notna(row['学历']) else ''
        email = row['邮箱'] if pd.notna(row['邮箱']) else ''
        phone = row['电话'] if pd.notna(row['电话']) else ''
        description = row['备注'] if pd.notna(row['备注']) else ''
        values.append("('{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}')".format(
            number, username, password, name, email, description, sex, rank, education, phone))
    # 拼接成 SQL 语句
    cmd = """INSERT INTO teacher (number,username,password,name,email,description,sex,`rank`,education,phone) 
    VALUES {};""".format(', '.join(values))
    result = db.execute_sql(cmd)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '批量新增教师')
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})
