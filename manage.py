from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app
from exts import db
from apps.cms import models as cms_models

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmission
app = create_app()

manager = Manager(app)
Migrate(app,db)

manager.add_command('db',MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user =CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功')

##147讲
@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s'%role)
    else:
        print('%s邮箱没有这个用户!'%email)
#146讲
@manager.command
def create_role():
    # 1. 访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者',desc='只能相关数据，不能修改。')
    visitor.permissions = CMSPermission.VISITOR

    # 2. 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='运营',desc='管理帖子，管理评论,管理前台用户。')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

    # 3. 管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员',desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 4. 开发者
    developer = CMSRole(name='开发者',desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()


#147讲
@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
    # if user.is_developer:

        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者权限！')


"""

(my_env) $python3 manage.py create_role
(my_env) $

------------------=========================

mysql> select * from cms_role
    -> ;
+----+-----------+---------------------------------------------------+---------------------+-------------+
| id | name      | desc                                              | create_time         | permissions |
+----+-----------+---------------------------------------------------+---------------------+-------------+
|  1 | 访问者    | 只能相关数据，不能修改。                          | 2019-12-23 13:03:42 |           1 |
|  2 | 运营      | 管理帖子，管理评论,管理前台用户。                 | 2019-12-23 13:03:42 |          55 |
|  3 | 管理员    | 拥有本系统所有权限。                              | 2019-12-23 13:03:42 |          63 |
|  4 | 开发者    | 开发人员专用角色。                                | 2019-12-23 13:03:42 |         255 |
+----+-----------+---------------------------------------------------+---------------------+-------------+
4 rows in set (0.00 sec)


"""

if __name__ =='__main__':
    manager.run()

