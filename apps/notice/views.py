#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/19 8:49
** @Author：Anonymous
** @Description：
**************************************************************
'''
from flask_login import login_required, current_user
from exts import db
from flask import request, render_template, Blueprint, jsonify

from exts.common import insert_audit_log

notice_bp = Blueprint('notice_bp', __name__, url_prefix='')
model_name = '公告管理'
@notice_bp.route('/notice',methods=['GET'])
@login_required
def notice():
	notice_infos=db.execute_sql('SELECT * from notice').fetchall()
	[i.update({'release_time': i['release_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in notice_infos]
	return render_template('notice.html', notice_infos=notice_infos)


@notice_bp.route('/notice/add',methods=['POST'])
@login_required
def notice_add():
	cmd = "INSERT INTO notice(title,content) VALUES (%s,%s)"
	params = (request.json['title'], request.json['content'])
	result = db.execute_sql(cmd, params)
	if result:
		insert_audit_log(request.remote_addr, current_user.id, model_name, '新增公告:' + request.json['title'])
		return jsonify({'success': True, 'message': "添加成功!"})
	else:
		return jsonify({'success': False, 'message': "添加失败!"})
