#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/21 17:48
** @Author：Anonymous
** @Description：
**************************************************************
'''

from exts import db
from flask import request, render_template, jsonify, Blueprint

audit_bp = Blueprint('audit_bp', __name__, url_prefix='')
model_name = '审计日志'


@audit_bp.route('/audit', methods=['GET'])
def audit_query():
    if "startTime" not in request.args and "endTime" not in request.args:
        result = db.execute_sql("select * from audit ORDER BY op_time desc")
        if result:
            audit_infos = result.fetchall()
            [i.update({'op_time': i['op_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in audit_infos]
        else:
            audit_infos = []
        return render_template("audit.html", audit_infos=audit_infos)
    else:
        startTime = request.args.get('startTime')
        endTime = request.args.get('endTime')
        cmd = """
		SELECT * FROM audit
    WHERE op_time BETWEEN FROM_UNIXTIME(%s) AND FROM_UNIXTIME(%s) ORDER BY op_time desc"""
        result = db.execute_sql(cmd, (startTime, endTime)).fetchall()
        if result:
            audit_infos = result
            [i.update({'op_time': i['op_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in audit_infos]
        else:
            audit_infos = []
        return jsonify({"rows": audit_infos, "total": len(audit_infos)})
