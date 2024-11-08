#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/16 15:57
** @Author：Anonymous
** @Description：
**************************************************************
'''
from flask_login import login_required, current_user

from exts import db
from flask import request, jsonify, Blueprint, render_template

from exts.common import insert_audit_log

permission_bp = Blueprint('permission_bp', __name__, url_prefix='')
model_name = '权限管理'


@permission_bp.route('/permissions/query', methods=['POST'])
def permission_query():
    if 'role' in request.json:
        result = db.execute_sql('SELECT permission_ids from role WHERE id = %s', request.json['role']).fetchone()
        if result:
            return jsonify({'success': True, 'message': '权限查询成功', 'permission_ids': result['permission_ids']})
        else:
            return jsonify({'success': False, 'message': '权限查询失败'})
    else:
        result = db.execute_sql('SELECT * from role').fetchall()
        if result:
            return jsonify(
                {'success': True, 'result': [{'role': i['id'], 'permission_ids': i['permission_ids']} for i in result]})
        else:
            return jsonify({'success': False, 'message': '权限查询失败'})


@permission_bp.route('/permissions', methods=['GET'])
@login_required
def permissions():
    return render_template("permission.html")


@permission_bp.route('/permissions/update', methods=['POST'])
@login_required
def permissions_update():
    # 将 permission_ids 中的每个元素转换为整数
    try:
        int_permission_ids = [int(id) for id in request.json['permission_ids'] if id.isdigit()]
    except ValueError:
        pass
    # 使用逗号将整数列表拼接成一个字符串
    permissions_str = ','.join(str(id) for id in int_permission_ids)
    result = db.execute_sql('UPDATE role SET permission_ids = %s WHERE id = %s',
                            (permissions_str, request.json["role"]))
    if result:
        if result:
            insert_audit_log(request.remote_addr, current_user.id, model_name, '更新权限条目:' + str(request.json['role']))
            return jsonify({'success': True, 'message': "权限修改成功!"})
        else:
            return jsonify({'success': False, 'message': "权限修改失败!"})
