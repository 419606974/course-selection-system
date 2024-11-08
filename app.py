#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/8/12 11:15
** @Author：Anonymous
** @Description：flask框架主程序入口
**************************************************************
'''

import settings
from exts import db
from apps.audit.views import audit_bp
from exts.logHandler import base_logger as logger
from apps.course.views import course_bp
from apps.notice.views import notice_bp
from apps.permission.views import permission_bp
from apps.role.views import role_bp
from apps.teacher.view import teacher_bp
from apps.user.views import user_bp, User
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)
app.config.from_object(settings.DevelopmentConfig)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    result = db.execute_sql(
        'SELECT username FROM admin WHERE username = %s UNION ALL SELECT username FROM user WHERE username = %s UNION ALL SELECT username FROM teacher WHERE username = %s LIMIT 1',
        (username, username, username)).fetchone()
    return User(result['username']) if result else None


# 注册应用蓝图
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(permission_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(course_bp)
app.register_blueprint(audit_bp)


@app.before_request
def print_request_info():
    logger.debug("接口请求地址:" + request.url)
    # 文件上传接口不需要打印请求内容
    if request.endpoint == 'user_bp.file_upload':
        pass
    elif request.files:
        pass
    else:
        logger.debug("接口请求数据:" + request.get_data().decode('utf-8'))


# 处理请求后无异常执行该钩子函数
# @app.after_request
# def print_request_data(response):
#     logger.debug("接口请求返回:" + response.get_data().decode('utf-8'))
#     return response


@app.route('/', methods=['GET'])
@login_required
def index():
    notice_infos = db.execute_sql('SELECT * from notice').fetchall()
    [i.update({'release_time': i['release_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in notice_infos]
    notice_infos = {'total': len(notice_infos), 'infos': notice_infos}
    return render_template("dashboard.html", username=current_user.id, notice_infos=notice_infos)


@app.route('/lyear_main.html', methods=['GET'])
@login_required
def lyear_main():
    courseCountByTeacher = db.execute_sql(
        'SELECT t.name AS teacher_name, COUNT(c.name) AS course_count FROM course c JOIN teacher t ON c.teacher_id = t.id GROUP BY t.name ORDER BY course_count DESC').fetchall()
    courseCountByStudent = db.execute_sql("""
	SELECT c.name AS course_name, COUNT(a.student_id) AS selected_stu_num
	FROM achievement a
	JOIN course c ON a.course_id = c.id
	JOIN user u ON a.student_id = u.id
	GROUP BY c.name
	ORDER BY selected_stu_num DESC;""").fetchall()
    teacherRankCount = db.execute_sql("""SELECT `rank`, COUNT(*) AS count FROM teacher GROUP BY `rank`""").fetchall()
    course_count = db.execute_sql('SELECT COUNT(*) as total from course').fetchone()
    notice_count = db.execute_sql('SELECT COUNT(*) as total from notice').fetchone()
    teacher_count = db.execute_sql('SELECT COUNT(*) as total from teacher').fetchone()
    user_count = db.execute_sql('SELECT COUNT(*) as total from user').fetchone()
    notice_infos = db.execute_sql('SELECT * from notice').fetchall()
    [i.update({'release_time': i['release_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in notice_infos]
    notice_infos = {'total': len(notice_infos), 'infos': notice_infos}
    return render_template("lyear_main.html", teacherRankCount=teacherRankCount,
                           courseCountByTeacher=courseCountByTeacher, courseCountByStudent=courseCountByStudent,
                           course_number=course_count['total'], notice_number=notice_count['total'],
                           username=current_user.id,
                           teacher_number=teacher_count['total'], user_number=user_count['total'],
                           notice_infos=notice_infos)


@app.route('/welcome', methods=['GET'])
@login_required
def welcome():
    return render_template("welcome.html")


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    notice_infos = db.execute_sql('SELECT * from notice').fetchall()
    [i.update({'release_time': i['release_time'].strftime('%Y-%m-%d %H:%M:%S')}) for i in notice_infos]
    notice_infos = {'total': len(notice_infos), 'infos': notice_infos}
    return render_template("dashboard.html", username=current_user.id, notice_infos=notice_infos)


@app.errorhandler(404)
def page_not_found(e):
    # 注意这里的 '404' 是 URL 规则，而不是硬编码的数字
    return redirect(url_for('error_404'))


@app.route('/404')
def error_404():
    return render_template('404.html')


@app.errorhandler(401)
def unauthorized(e):
    # 如果收到401错误，则重定向到登录页面
    flash("Please log in to access this page.", 'warning')
    return redirect(url_for('user_bp.login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8888)
