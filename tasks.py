import os

from invoke import task

@task
def run(ctx):
    print('Migrating db')
    ctx.run('python manage.py migrate')
    print('Collect static')
    ctx.run('python manage.py collectstatic --noinput')

    # comment for hetzner
    # print('Run WSGI server with gunicorn')
    # ctx.run('gunicorn config.wsgi --bind 0.0.0.0:8000')
    # heroku supports gunicorn, hetzner supports uwsgi

    command = ('uwsgi --http 0.0.0.0:8080 --master'
            ' --module "config.wsgi:get_wsgi_application()"'
            ' --processes=5'
            ' --offload-threads 4'
            ' --enable-threads'
            ' --static-map /static=/static'
            ' --static-map /media=/media'
    )

    if os.getenv('PY_AUTORELOAD'):
        command += ' --py-autoreload 1'

    # if os.getenv('BASICAUTH'):
    #     command += ' --route "^/--basicauth:BA,{0}"'.format(os.getenv('BASICAUTH'))

    # if os.getenv('ENV', "dev") == 'dev':
    #     command += ' --honour-stdin'
    # else:
    #     command += ' --harakiri 30'

    ctx.run(command)
