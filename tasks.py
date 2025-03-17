import os

from invoke import task

@task
def run(ctx):
    command = ('uwsgi --http 0.0.0.0:8080 --master'
            ' --module "config.wsgi:get_wsgi_application()"'
            ' --processes=5'
            ' --offload-threads 4'
            ' --enable-threads'
    )

    if os.getenv('PY_AUTORELOAD'):
        command += ' --py-autoreload 1'

    # if os.getenv('BASICAUTH'):
    #     command += ' --route "^/--basicauth:BA,{0}"'.format(os.getenv('BASICAUTH'))

    if os.getenv('ENV', "dev") == 'dev':
        command += ' --honour-stdin'
    else:
        command += ' --harakiri 30'

    ctx.run(command)
