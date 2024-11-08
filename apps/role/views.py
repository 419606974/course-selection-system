#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/15 12:53
** @Author：Anonymous
** @Description：
**************************************************************
'''
from flask_login import current_user
from exts import db
from flask import request, render_template, Blueprint, jsonify
from exts.common import insert_audit_log

role_bp = Blueprint('role_bp', __name__, url_prefix='')
model_name = '角色管理'


@role_bp.route('/role', methods=['GET'])
def role_list():
    role_infos = db.execute_sql('SELECT * from role').fetchall()
    return render_template("role.html", role_infos=role_infos)


@role_bp.route('/roles', methods=['POST'])
def getAllRoles():
    cmd = "SELECT id,name FROM role"
    result = db.execute_sql(cmd).fetchall()
    if result:
        return jsonify(result)


@role_bp.route('/role/add', methods=['POST'])
def role_add():
    cmd = "INSERT INTO role(name,description) VALUES (%s,%s)"
    params = (request.json['name'], request.json['description'])
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '新增角色信息:' + request.json['name'])
        return jsonify({'success': True, 'message': "添加成功!"})
    else:
        return jsonify({'success': False, 'message': "添加失败!"})


@role_bp.route('/role/update', methods=['POST'])
def role_update():
    update_dict = {}
    # 根据request.get_json()中的数据构建一个动态的SQL更新语句
    if request.get_json()["name"] != '':
        update_dict.update({'name': request.get_json()["name"]})
    if request.get_json()["description"] != '':
        update_dict.update({'description': request.get_json()["description"]})
    # 构建SQL更新语句
    set_clause = ', '.join(f"{key} = %s" for key in update_dict.keys())
    cmd = f"UPDATE role SET {set_clause} WHERE name = %s"

    # 准备参数列表
    params = list(update_dict.values()) + [request.get_json()["name"]]
    result = db.execute_sql(cmd, params)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '更新角色信息:' + request.json['name'])
        return jsonify({'success': True, 'message': "更新成功!"})
    else:
        return jsonify({'success': False, 'message': "更新失败!"})


@role_bp.route('/role/delete', methods=['POST'])
def role_delete():
    if 'id' in request.json:
        cmd = "DELETE FROM role WHERE id=%s;"
        result = db.execute_sql(cmd, request.json['id'])
        ids_to_delete = request.json['id']
    elif 'ids' in request.json:
        ids_to_delete = request.json['ids']
        # 构建 SQL 语句
        placeholders = ', '.join(['%s'] * len(ids_to_delete))
        cmd = f"DELETE FROM role WHERE id IN ({placeholders})"
        result = db.execute_sql(cmd, ids_to_delete)
    if result:
        insert_audit_log(request.remote_addr, current_user.id, model_name, '删除角色信息:' + str(ids_to_delete))
        return jsonify({'success': True, 'message': "删除成功!"})
    else:
        return jsonify({'success': False, 'message': "删除失败!"})
