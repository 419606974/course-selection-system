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

import pandas as pd

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
        # elif role == 2:
        #     result = db.execute_sql('SELECT password from teacher WHERE username = %s',
        #                             (request.json['username'])).fetchone()
        elif role == 2:
            result = db.execute_sql('SELECT password,status from admin WHERE username = %s',
                                    (request.json['username'])).fetchone()
        elif role == 3:
            result = db.execute_sql('SELECT password,status from user WHERE username = %s',
                                    (request.json['username'])).fetchone()
        else:
            result = None
        if result:
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
    query = request.args.get('query')
    student_no = request.args.get('student_no')
    major_name = request.args.get('major_name')

    # 1. 如果是根据专业名查学生
    if major_name:
        sql = """
            SELECT
                u.username, u.name, u.enrollment_date, u.student_type, u.fellowship
            FROM
                user u
            JOIN student_major sm ON u.id = sm.student_id
            JOIN major m ON sm.major_id = m.id
            WHERE m.name = %s
        """
        user_infos = db.execute_sql(sql, (major_name,)).fetchall()
        return jsonify({"success": True, "users": user_infos})

    # 2. 无条件，加载所有学生
    if not query and not student_no:
        sql = """
            SELECT
                u.id, u.username, u.name, u.sex, u.hometown, u.enrollment_date,
                u.student_type, u.fellowship, u.phone, u.email, u.description,
                GROUP_CONCAT(m.name SEPARATOR ', ') AS major
            FROM
                user u
            LEFT JOIN student_major sm ON u.id = sm.student_id
            LEFT JOIN major m ON sm.major_id = m.id
            WHERE u.role_id = 3
            GROUP BY u.id
            ORDER BY u.id
        """
        user_infos = db.execute_sql(sql).fetchall()
        # [i.update({'register_time': i['register_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in user_infos]
        # [i.update({'last_login_time': i['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')}) if i[
        #     'last_login_time'] else ''
        #  for i in user_infos]
        return render_template("user.html", user_infos=user_infos)

    # 3. 按关键词模糊搜索
    if query:
        sql = """
            SELECT * FROM user
            WHERE username LIKE %s OR email LIKE %s OR name LIKE %s OR phone LIKE %s
        """
        user_infos = db.execute_sql(
            sql,
            ('%' + query + '%',) * 4
        ).fetchall()
        for i in user_infos:
            if i.get('register_time'):
                i['register_time'] = i['register_time'].strftime('%Y-%m-%d %H:%M:%S')
            if i.get('last_login_time'):
                i['last_login_time'] = i['last_login_time'].strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({"rows": user_infos, "total": len(user_infos)})

    # 4. 根据学号查询
    if student_no:
        student_info = db.execute_sql(
            'SELECT * FROM user WHERE username=%s', (student_no,)
        ).fetchone()
        if student_info:
            return jsonify({'success': True, 'student_info': student_info})
        else:
            return jsonify({'success': False, 'message': "不存在该学生"})


@user_bp.route('/user/add', methods=['POST'])
@login_required
def user_add():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    role = int(request.json['role'])
    if role == 1:
        cmd = "INSERT INTO admin(username,password,email,role_id,status,description) VALUES (%s,%s,%s,%s,%s,%s)"
        params = (request.json['username'], request.json['password'], request.json['email'], request.json['role'],
                  request.json['status'], request.json['description'])
    elif role == 2:
        cmd = "INSERT INTO teacher(username,password,email,description) VALUES (%s,%s,%s,%s,%s)"
        params = (
        request.json['username'], request.json['password'], request.json['email'], request.json['description'])
    elif role == 3:
        cursor = db.execute_sql("SELECT id FROM user WHERE username = %s", (request.json['username'],))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "学号已存在"})
        cmd = """INSERT INTO user(username,password,name,email,role_id,status,description,sex,hometown,
		enrollment_date,student_type,fellowship,phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        params = (request.json['username'], request.json['password'], request.json['name'],
                  request.json['email'], role,
                  request.json['status'], request.json['description'], request.json['sex'],
                  request.json['hometown'],
                  request.json['enrollment_date'],
                  request.json['student_type'],
                  request.json['fellowship'],
                  request.json['phone'])
    result = db.execute_sql(cmd, params)
    if result:
        cursor = db.execute_sql("SELECT id FROM user WHERE username = %s", (request.json['username'],))
        user_id = cursor.fetchone()["id"]
        majors = request.get_json().get("major", [])
        if majors:
            cursor = db.execute_sql("SELECT id FROM major WHERE name IN %s", ((tuple(majors),)))
            for row in cursor.fetchall():
                db.execute_sql("INSERT INTO student_major (student_id, major_id) VALUES (%s, %s)", (user_id, row['id']))
        insert_audit_log(request.remote_addr, current_user.id, "用户管理", '新增账号: ' + request.get_json()['username'])
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@user_bp.route('/user/update', methods=['POST'])
@login_required
def user_update():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})

    update_dict = {}
    data = request.get_json()
    username = data.get("username")
    majors = data.get("major", [])

    cursor = db.execute_sql("SELECT id FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return jsonify({"success": False, "message": "用户不存在"})
    user_id = user["id"]

    # 动态生成待更新字段字典
    if data.get("name") != '': update_dict['name'] = data["name"]
    if data.get("password") != '': update_dict['password'] = data["password"]
    if data.get("email") != '': update_dict['email'] = data["email"]
    if data.get("role") != '': update_dict['role_id'] = data["role"]
    if data.get("status") != '': update_dict['status'] = data["status"]
    if data.get("description") != '': update_dict['description'] = data["description"]
    if data.get("sex") != '': update_dict['sex'] = data["sex"]
    if data.get("hometown") != '': update_dict['hometown'] = data["hometown"]
    if data.get("enrollment_date") != '': update_dict['enrollment_date'] = data["enrollment_date"]
    if data.get("student_type") != '': update_dict['student_type'] = data["student_type"]
    if data.get("fellowship") != '': update_dict['fellowship'] = data["fellowship"]
    if data.get("phone") != '': update_dict['phone'] = data["phone"]

    # 获取当前数据库中该学生已关联的 major_id 集合
    cursor = db.execute_sql("SELECT major_id FROM student_major WHERE student_id = %s", (user_id,))
    existing_major_ids = {row["major_id"] for row in cursor.fetchall()}

    # 获取前端提交的 major_id 集合
    cursor = db.execute_sql("SELECT id FROM major WHERE name IN %s", ((tuple(majors),)))
    new_major_ids = {row["id"] for row in cursor.fetchall()}

    # 计算差集
    to_add = new_major_ids - existing_major_ids
    to_delete = existing_major_ids - new_major_ids

    updated = False

    if update_dict:
        set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
        cmd = f"UPDATE user SET {set_clause} WHERE username = %s"
        params = list(update_dict.values()) + [username]
        result = db.execute_sql(cmd, params)
        updated = True if result else False

    if to_add or to_delete:
        for mid in to_delete:
            db.execute_sql("DELETE FROM student_major WHERE student_id = %s AND major_id = %s", (user_id, mid))
        for mid in to_add:
            db.execute_sql("INSERT INTO student_major (student_id, major_id) VALUES (%s, %s)", (user_id, mid))
        updated = True

    if updated:
        insert_audit_log(request.remote_addr, current_user.id, "用户管理", '更新用户信息: ' + username)
        return jsonify({'success': True, 'message': "更新成功!"})
    else:
        return jsonify({'success': True, 'message': "数据无变动，无需更新。"})


@user_bp.route('/user/delete', methods=['POST'])
@login_required
def user_delete():
    if session['role'] != 1:
        return jsonify({'success': False, 'message': '没有操作权限！'})
    data = request.get_json()
    ids = data.get("ids", []) if isinstance(data.get("ids"), list) else [data.get("id")]
    not_found_ids = []
    for uid in ids:
        cursor = db.execute_sql("SELECT username FROM user WHERE id = %s", (uid,))
        user = cursor.fetchone()
        if not user:
            not_found_ids.append(uid)
            continue
        # 删除成绩记录
        db.execute_sql("DELETE FROM achievement WHERE student_id = %s", (uid,))
        # 删除学生的专业关系
        db.execute_sql("DELETE FROM student_major WHERE student_id = %s", (uid,))
        # 删除学生本身
        db.execute_sql("DELETE FROM user WHERE id = %s", (uid,))
    if not_found_ids:
        insert_audit_log(request.remote_addr, current_user.id, "用户管理", ('删除用户,id: %s' % ids - not_found_ids))
        return jsonify({"success": False, "message": f"以下用户不存在：{not_found_ids}，其他已删除"})
    insert_audit_log(request.remote_addr, current_user.id, "用户管理", ('删除用户,id: %s' % ids))
    return jsonify({'success': True, 'message': "删除成功!"})
    # if 'id' in request.json:
    #     achievement_cmd = """SELECT * from achievement WHERE student_id=%s"""
    #     achievement_params = (request.json['id'])
    #     achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
    #     if achievement_row:
    #         return jsonify({'success': False, 'message': "存在该学生对应的成绩，请更改后再删除"})
    #     cmd = "DELETE FROM user WHERE id=%s;"
    #     result = db.execute_sql(cmd, request.json['id'])
    #     ids_to_delete = request.json['id']
    # elif 'ids' in request.json:
    #     ids_to_delete = request.json['ids']
    #     for id in ids_to_delete:
    #         achievement_cmd = """SELECT * from achievement WHERE student_id=%s"""
    #         achievement_params = (id)
    #         achievement_row = db.execute_sql(achievement_cmd, achievement_params).fetchone()
    #         if achievement_row:
    #             return jsonify({'success': False, 'message': "存在该学生对应的成绩，请更改后再删除"})
    #     # 构建 SQL 语句
    #     placeholders = ', '.join(['%s'] * len(ids_to_delete))
    #     cmd = f"DELETE FROM user WHERE id IN ({placeholders})"
    #     result = db.execute_sql(cmd, ids_to_delete)
    # if result:
    #     insert_audit_log(request.remote_addr, current_user.id, "用户管理", ('删除用户,id: %s' % ids_to_delete))
    #     return jsonify({'success': True, 'message': "删除成功!"})
    # else:
    #     return jsonify({'success': False, 'message': "删除失败!"})


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
        if role == 1 or role == 2:
            user_infos = db.execute_sql('SELECT password from admin WHERE username = %s', current_user.id).fetchone()
            cmd = "UPDATE admin SET password=%s WHERE username = %s"
        # elif role == 2:
        #     user_infos = db.execute_sql('SELECT password from teacher WHERE username = %s', current_user.id).fetchone()
        #     cmd = "UPDATE teacher SET password=%s WHERE username = %s"
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
                return {'success': True, 'message': "密码修改成功！请重新登录"}
            else:
                return {'success': False, 'message': "密码修改失败!"}
        else:
            return {'success': False, 'message': "原始密码错误，密码修改失败!"}


# 用户头像更新
@user_bp.route('/upload/avatar', methods=['POST'])
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
            avatar_image_path = url_for('static', filename='images/users/' + f'{new_file_name}')
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


@user_bp.route('/user/import', methods=['POST'])
@login_required
def import_users():
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
    for _, row in df.iterrows():
        if row['性别'] == '男':
            sex = 1
        elif row['性别'] == '女':
            sex = 0
        else:
            sex = 2
        username = str(row['学号']).strip() if pd.notna(row['学号']) else ''
        if not username:
            continue
        cursor = db.execute_sql("SELECT id FROM user WHERE username = %s", (username,))
        if cursor.fetchone():
            continue
        name = row['姓名'] if pd.notna(row['姓名']) else ''
        email = row['邮箱'] if pd.notna(row['邮箱']) else ''
        hometown = row['籍贯'] if pd.notna(row['籍贯']) else ''
        enrollment_date = row['入学时间'] if pd.notna(row['入学时间']) else None
        student_type = row['学生类别'] if pd.notna(row['学生类别']) else ''
        major_str = row['专业'] if pd.notna(row['专业']) else ''
        fellowship = row['团契'] if pd.notna(row['团契']) else ''
        phone = row['电话'] if pd.notna(row['电话']) else ''
        description = row['备注'] if pd.notna(row['备注']) else ''
        db.execute_sql("""
            INSERT INTO user (username, password, name, email, role_id, status, description,
                              sex, hometown, enrollment_date, student_type, fellowship, phone)
            VALUES (%s, %s, %s, %s, 3, 1, %s, %s, %s, %s, %s, %s, %s)
        """, (
            username, username, name, email, description, sex, hometown,
            enrollment_date, student_type, fellowship, phone
        ))
        cursor = db.execute_sql("SELECT id FROM user WHERE username = %s", (username,))
        user_id = cursor.fetchone()['id']
        # 专业处理
        majors = [m.strip() for m in major_str.split(',') if m.strip()]
        if majors:
            cursor = db.execute_sql("SELECT id FROM major WHERE name IN %s", ((tuple(majors),)))
            for m in cursor.fetchall():
                db.execute_sql("INSERT INTO student_major (student_id, major_id) VALUES (%s, %s)", (user_id, m['id']))
        added += 1

    if added > 0:
        insert_audit_log(request.remote_addr, current_user.id, "用户管理", f"批量新增学生 {added} 名")
        return jsonify({'success': True, 'message': f"成功添加 {added} 名学生！"})
    else:
        return jsonify({'success': False, 'message': "没有新增任何学生（可能已存在或数据不完整）"})
