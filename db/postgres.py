"""
PostgreSQL related functions
"""

from fabric.api import run, cd, get, warn_only, local


def pull_down_remote_db():
    """
    Updates local database with its remote counterpart.

    Use it with only one server.
    """
    with cd('{tmp_dir}'):
        run('pg_dump -U {pg_user} {db_name} > {db_name}.sql')
        print("Dumping database on remote...")
        get('{db_name}.sql', '{tmp_dir}')
        print("Dropping & Creating local DB")
        with warn_only():
            local("dropdb {db_name} -U {pg_user}")
            local("createdb {db_name} -U {pg_user}")
        local('psql {db_name} -U {pg_user} < %s' % '{tmp_dir}/{db_name}.sql')
