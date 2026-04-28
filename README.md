# Probability visualizer (Ohjelmistotekniikka, harjoitustyö)

The probability visualizer is meant to maintain user's own **probability distribution tests** and visualize them in GUI.

## Setting up

Copy-paste the following commands to your terminal/command prompt...

```bash
git clone https://github.com/ellapaella/ot-harjoitustyo-beta.git
```

...or if you have SSH set up

```bash
git clone git@github.com:ellapaella/ot-harjoitustyo-beta.git
```

After cloning use these commands in the project root (the one that has the `src` directory)

```bash
poetry install
```

You need Postgresql. Create a database for the project in psql.

In psql run the following command replacing the "name_of_database" with a name of your choosing:

`CREATE DATABASE name_of_database;`

This should create a database for the project.

Now return to command line with the `\q` and feed your database with the `schema.sql` file you 
downloaded with the project. Use the following command (again inserting the name of database here, 
otherwise it will create the tables to your default database which most likely will be your username):

`psql name_of_database < schema.sql`

This creates the necessary tables for you to use the program locally.

Now add the following line to .env file in the project root and 
replace the "name_of_database" with the database name you created:

`DATABASE_URL=postgresql:///name_of_database`


## Running the program

Start the program

```bash
poetry run invoke start
```
Run tests

```bash
poetry run invoke test
```
Create a html report of test branch coverage (report can be found at path ./htmlcov/index.html in project root)

```bash
poetry run invoke coverage-report
```
Run pylint check

```bash
poetry run invoke lint
```
Format code as defined by project's [.pylintrc](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/.pylintrc) file. More info at [PEP 8 style guide](https://peps.python.org/pep-0008/)

```bash
poetry run invoke format
```

## Docs

- [Requirement specifications](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/requirement_specifications.md)

- [Changelog](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/changelog.md)

- [Architecture](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/architecture.md)

- [Working hours](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/worktime.md)
