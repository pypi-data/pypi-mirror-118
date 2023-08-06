from typing import List
import typer
import pytest
from pytest import ExitCode
import os
from pathlib import Path
import coverage
import pylint.lint

cli = typer.Typer()


# https://docs.pytest.org/en/documentation-restructure/how-to/writing_plugins.html#well-specified-hooks
class eHelplyPytest:
    pass
    # def pytest_sessionfinish(self):
    #     print("", "*** starting coverage report ***")


LINTING_THRESHOLD: float = 7.5
COVERAGE_THRESHOLD: int = 70


@cli.command()
def units(
        ignore_linting: bool = typer.Option(False),
        ignore_unit_tests: bool = typer.Option(False),
        ignore_final_report: bool = typer.Option(False)
):
    """
    INITIAL SETUP AND INITIALIZATION
    """

    omit_patterns_linting: List[str] = [
        "example/**/*",
        "db/alembic/**/*",
        "service_meta.py",
        "service_template/**/*"
    ]

    omit_patterns_unit_testing: List[str] = [
        "src/example/*",
        "src/db/alembic/*",
        "src/db/*schema*.py",
        "src/db/*model*.py",
        "src/*seeders*",
        "src/service_meta.py",
        "src/service_template/*",
        "src/db/__init__.py",
        "src/service.py"
    ]

    omit_files: List[str] = []

    for omit_pattern in omit_patterns_linting:
        for path in Path('src').glob(omit_pattern):
            omit_files.append(str(path))

    """
    LINTING
    """

    linting_score: float = -1

    if not ignore_linting:
        lint_file_version: str = "0.0.1"

        files_to_lint: List[str] = []

        for path in Path('src').rglob("*.py"):
            if str(path) not in omit_files:
                files_to_lint.append(str(path))

        results = pylint.lint.Run(
            [
                "-r",  # generate report
                "y",  # yes
                "-s",  # generate code score
                "y",  # yes
                f"--rcfile=.pylintrc.ehelply.{lint_file_version}",
            ] + files_to_lint,
            exit=False
        )

        linting_score = results.linter.stats["global_note"]

        if linting_score < LINTING_THRESHOLD:
            raise Exception(
                f"Linting score is {round(linting_score, 2)} which is below {LINTING_THRESHOLD}. Thus, build has failed.")

    """
    UNIT TESTING
    """

    coverage_amount: float = -1

    if not ignore_unit_tests:
        # Run DB migrations or unit tests for features relying on DB migrations will fail
        #   Thus, failing prod build/deploys
        typer.echo("Running Migrations..")
        from alembic.config import Config
        import alembic.command

        config = Config('alembic.ini')
        config.attributes['configure_logger'] = False

        alembic.command.upgrade(config, 'head')

        # Run unit tests

        root_path = Path(os.getcwd())

        docs_location = Path(root_path).resolve().joinpath('test-results')
        docs_location.mkdir(exist_ok=True)

        result: ExitCode = pytest.main(
            [
                "-s",
                "-v",
                # "--cov-report", "term-missing",
                "--cov-report", f"html:{str(docs_location)}",
                "--cov=src",
                "tests/"
            ]
        )

        if result != ExitCode.OK:
            raise typer.Exit(code=result)

        cov = coverage.Coverage()
        cov.load()

        # coverage_amount: float = cov.json_report(
        #     omit=omit
        # )

        coverage_amount = cov.report(
            show_missing=True,
            omit=omit_patterns_unit_testing
        )

        if coverage_amount < COVERAGE_THRESHOLD:
            raise Exception(
                f"Test coverage is {int(coverage_amount)}% which is below {COVERAGE_THRESHOLD}%. Thus, build has failed.")

    """
    REPORTING
    """

    if not ignore_final_report:
        print("\n\n")
        print("REPORT")
        print(f"Linting Score: {round(linting_score, 2)}/10, Linting Threshold: {LINTING_THRESHOLD}")
        print(f"Test Coverage: {int(coverage_amount)}%/100%, Test Coverage Threshold: {COVERAGE_THRESHOLD}%")
        print("\n\n")
