"""
Deploy project related functions
- With virtualenv and virtualenvwrapper added
"""

from fabric.api import run, cd, prefix, env, settings, sudo

env.hosts = ['user@111.111.11.11']
env.user = "{youruser}"
env.password = '{you password}'

CLONE_PATH = "{path/to/your/project}"
PROJECT_PATH = "{Your project path}"
VIRTUAL_ENV_NAME = "{your virtualenv name}"
GIT_REPO = "{your repository here}"
REQUIRE_PATH_LIST = [
    "list",
    "of",
    "path",
    "requirements"
]
MASTER_USER = "Other master user root here"
MASTER_PASSWORD = "Other master password root here"

SUPERVISOR_APPS = ["one app", "another app"]


def install_git_pip():
    """
    Install git and dependencies
    - Debian Like
    """
    run("sudo apt-get install git; git-core; python-pip")


def clone_project():
    """
    Clone project to folder
    """
    with cd(CLONE_PATH):
        with prefix("workon {}".format(VIRTUAL_ENV_NAME)):
            run("git clone {}".format(GIT_REPO))


def pull_project(branch="master"):
    """
    Pull git project
    """
    with cd(PROJECT_PATH):
        run("git pull origin {}".format(branch))


def collect_static():
    """
    Django collectstatic
    """
    with cd(PROJECT_PATH):
        with prefix("workon {}".format(VIRTUAL_ENV_NAME)):
            run("python manage.py collectstatic --noinput")


def full_deploy():
    """
    Make a full Deploy of project
    """
    pull_project("master")
    install_requirements()
    manage('migrate --all')
    collect_static()
    service_restart("{your service here}")
    restart_apps()


def run_sudo_master(command="ll"):
    """
    Example to execute a command with another Root user if needed
    """
    with settings(user=MASTER_USER, password=MASTER_PASSWORD):
        run(command)


def service_restart(app_name="nginx"):
    """
    Restart a service
    - if an app not started yet, restart will
    """
    run("sudo service {} restart".format(app_name))


def restart_apps(app=False):
    """
    If not pass an app, he takes all apps on SUPERVISOR_APPS var
    Like service_restart will started all apps that not started yet
    """
    if app:
        sudo("sudo supervisorctl restart {}".format(app))
    else:
        for app in SUPERVISOR_APPS:
            sudo("sudo supervisorctl restart {}".format(app))


def manage(args):
    """
    Alias for django project manage
    """
    with cd(PROJECT_PATH):
        with prefix("workon {}".format(VIRTUAL_ENV_NAME)):
            run("python manage.py {}".format(args))


def install_requirements():
    """
    Install requirements based on REQUIRE_PATH_LIST
    """
    for path in REQUIRE_PATH_LIST:
        with cd(path):
            with prefix("workon {}".format(VIRTUAL_ENV_NAME)):
                run("pip install -r requirements.txt")
