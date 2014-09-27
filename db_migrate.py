#!flask/bin/python
import imp
from migrate.versioning import api
from app import db
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

migration = SQLALCHEMY_MIGRATE_REPO + '/version/%03_migrate.py' % (api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) + 1)
tmp_mdel = imp.new_module('old_model')
old_mdel = api.create_module(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO) 
exec old_model in tmp_module.__dict__
script = api.make_update_script_for_model(SQLALCHEMY_MIGRATE_REPO)
open(migration, "wt").write(script)
a = api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print "New migration saved as " + migration
print "Current database version: " + str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))
