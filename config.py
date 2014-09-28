import os
basedir = os.path.abspath(os.path.dirname(__file__))

CRSF_ENABLED = True
SECRET_KEY = 'ccc_cms'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://root:admin888@localhost/cccms'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repostitory')

UPLOAD_IMAGE = ['gif', 'jpg', 'png', 'jpeg', 'bmp']
UPLOAD_FLASH = ['swf', 'flv']
UPLOAD_MEDIA = UPLOAD_FLASH + ['mp3', 'wav', 'wma', 'wmv', 'mid', 'avi', 'mpg', 'asf', 'rm', 'rmvb']
UPLOAD_OFFICE = ['doc', 'xls', 'ppt', 'docx', 'xlsx', 'pptx']
UPLOAD_COMPRESS = ['rar', 'zip', '7z', 'tar', 'gz']
UPLOAD_FILE = UPLOAD_IMAGE + UPLOAD_MEDIA + UPLOAD_OFFICE + UPLOAD_COMPRESS + ['pdf', 'txt'] 

UPLOAD_FILE_SIZE = 10000

PAGINATION = 10 
