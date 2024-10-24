# Python+Flask+html学生选课系统

## 项目技术框架说明

主要技术栈：Python3+Flask+js+jquery+charts.js
数据库：mysql 8.x


## 功能

-   [x] 用户登录、注销、密码找回
      - [x] 登录采用session会话管理
      - [x] 支持通过邮件方式找回密码
-   [x] 首页Dashboard大屏数据统计
-   [x] 教师管理
      - [x] 课程开设、编辑、删除
      - [x] 课程成绩登记、修改、删除
-   [x] 选课，包括：
      - [x] 课程查询、选课
      - [x] 已选课程查询、取消选课
-   [x] 角色管理
      - [x] 不同的角色赋予不同的权限
-   [x] 用户管理
      - [x] 不同的用户赋予不同的角色，展示不同的界面和操作权限
-   [x] 审计管理
      - [x] 三权分立，可以看到系统审计日志
-   [x] 公告管理
-   [x] 用户中心、修改个人信息和密码
-   [x] 全局颜色方案修改


## 安装步骤

### 1. 基础环境准备

> python版本: 3.8.1（如果是其他版本python请自行调试代码）
> mysql版本: 8.x

### 2. 配置+启动

#### 数据库

```
1. 提前创建好想要的数据库，例如course_selection_manage
2. 导入数据库文件course_selection_manage.sql
mysql -u root -p course_selection_manage < course_selection_manage.sql
```

#### 配置

```
1. 进入course-selection-system根目录，执行
pip install -r requirements.txt                        // 安装第三方依赖包
2. 修改settings.py中的数据库信息和邮箱信息相关配置
3. 启动项目
python app.py           //运行后端服务
```

# 访问页面

通过http://127.0.0.1:5000即可访问登录页面
管理员账号admin/12345678
教师账号zhangsan/12345678
学生账号student/12345678

# 联系作者

wx: tygkbk
