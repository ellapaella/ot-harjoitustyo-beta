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

After cloning use these commands in the repository root (the one that has the `src` directory)

```bash
poetry install
```

## Running the program

Start the program

```bash
poetry run invoke start
```
Run tests

```bash
poetry run invoke test
```
Create a html report of test branch coverage

```bash
poetry run invoke coverage-report
```
Run pylint check

```bash
poetry run invoke lint
```
Format code as defined by project's .pylintrc file. More info at [PEP 8 style guide](https://peps.python.org/pep-0008/)

```bash
poetry run invoke format
```

## Docs

- [Requirement specifications](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/requirement_specifications.md)

- [Changelog](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/changelog.md)

- [Architecture](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/architecture.md)

- [Working hours](https://github.com/ellapaella/ot-harjoitustyo-beta/blob/main/documentation/worktime.md)

