import os

from invoke import task

@task
def run(ctx):
    ctx.run("pwd", hide=False)
    print()
    print('Migrating db')
    ctx.run('python manage.py migrate', hide=False)
    print('Collecting static')

    ctx.run('python manage.py collectstatic --noinput', hide=False)

    cmd = ('uwsgi --http 0.0.0.0:8080 --master '
           '--module "django.core.wsgi:get_wsgi_application()" '
           '--processes 2 '
           '--offload-threads 4 '
           '--enable-threads '
           '--static-map /static=/static '
           '--static-map /media=/media'
           )


    if os.getenv('PY_AUTORELOAD'):
        cmd += ' --py-autoreload 1'

    # if os.getenv('BASICAUTH'):
    #     command += ' --route "^/--basicauth:BA,{0}"'.format(os.getenv('BASICAUTH'))

    # if os.getenv('ENV', "dev") == 'dev':
    #     command += ' --honour-stdin'
    # else:
    #     command += ' --harakiri 30'

    ctx.run(cmd, hide=False)

