#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask import Flask
import os
from app import create_app,db
from flask_script import Manager, Shell,Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import User

app = create_app(os.getenv('GUITARPA_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 部署命令
@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade
    from app.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()

if __name__ == '__main__':
    manager.run()
