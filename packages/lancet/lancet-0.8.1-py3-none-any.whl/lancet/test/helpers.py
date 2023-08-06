import os
import pytest

from click.testing import CliRunner

from ..cli import main
from ..settings import LOCAL_CONFIG


@pytest.fixture
def runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


def setup_lancet(runner, user_config=None, debug=True):
    user_input = ["3", "john-doe", "john-doe", "12345", "67890"]
    if not user_config:
        user_config = "{}/{}".format(os.getcwd(), LOCAL_CONFIG)

    result = runner.invoke(
        main, "setup",
        env={
            "LANCET_TEST_USER_CONFIG": user_config,
        },
        input="\n".join(user_input),
    )
    # keep, this can be rendered by using ``pytest -s``
    if debug:
        print("\n>>>>> EXCEP\n", result.exception)
        print("\n>>>>> STOUT\n", result.stdout)
    return result, user_config


def init_lancet(runner, user_config=None, project_config=None, debug=True):
    user_input = ["develop", "12345", "67890", "KEY", "09876", "54321", "1", "n"]
    if not user_config:
        user_config = "{}/{}".format(os.getcwd(), LOCAL_CONFIG)
    if not project_config:
        project_config = "{}/project/{}".format(os.getcwd(), LOCAL_CONFIG)
        os.makedirs(os.path.dirname(project_config))

    result = runner.invoke(
        main, "init",
        env={
            "LANCET_TEST_USER_CONFIG": user_config,
            "LANCET_TEST_PROJECT_CONFIG": project_config,
        },
        input="\n".join(user_input),
    )
    # keep, this can be rendered by using ``pytest -s``
    if debug:
        print("\n>>>>> EXCEP\n", result.exception)
        print("\n>>>>> STOUT\n", result.stdout)
    return result, project_config


def set_lancet(runner, user_config=None, project_config=None):
    setup, user_config = setup_lancet(runner, debug=False)
    init, project_config = init_lancet(runner, user_config, debug=False)

    assert setup.exit_code == 0
    assert init.exit_code == 0

    return setup, init
