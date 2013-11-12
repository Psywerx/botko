from fabric.api import run, sudo, env, cd

env.use_ssh_config = True

env.hosts = ['server']


def host():
    run('uname -a')


def update():
    with cd('botko'):
        out = run('git pull')
        if 'Already up-to-date.' not in out:
            sudo('botko restart')
