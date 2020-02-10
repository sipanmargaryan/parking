from project.settings import *  # noqa

DEBUG = True
CELERY_TASK_ALWAYS_EAGER = True
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
ENABLE_HTTP_BASIC_AUTH = False
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'test')
