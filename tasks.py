from invoke import task

@task
def build(ctx, db_name="probability_app"):
    # Create main database
    ctx.run(f"createdb {db_name}", warn=True)

    # Create test database
    ctx.run(f"createdb {db_name}_test", warn=True)

    # Apply schema to main database
    ctx.run(f"psql -d {db_name} -f schema.sql")

    # Apply schema to test database
    ctx.run(f"psql -d {db_name}_test -f schema.sql")

@task
def start(ctx):
    ctx.run("python3 src/main.py", pty=True)

@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def lint(ctx):
    ctx.run("pylint src", pty=True)

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src", pty=True)
