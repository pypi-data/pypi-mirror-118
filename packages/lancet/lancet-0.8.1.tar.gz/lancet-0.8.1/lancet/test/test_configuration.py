from textwrap import dedent

from ..settings import load_config

from .helpers import runner, setup_lancet, init_lancet


def test_setup_command(runner):
    setup, user_config = setup_lancet(runner)
    assert setup.exit_code == 0

    text = dedent(
        """
        Welcome to the Lancet setup wizard.
        Please choose a tracker:
        (1) Gitlab, (2) Jira, (3) Both: 3

        Step 1 of 4
        Enter your Gitlab username:
        Username: john-doe

        Step 2 of 4
        Enter your Jira username:
        Username: john-doe

        Step 3 of 4
        Enter the Harvest account ID:
        (You can get it from https://id.getharvest.com/developers)
        Accound ID: 12345

        Step 4 of 4
        Enter the Harvest ID found on your profile's URL:
        (You can get it from https://divio.harvestapp.com/people/<YOUR_ID>/)
        User ID: 67890

        Configuration correctly written to "{}".\n""".format(user_config)
    ).lstrip()
    assert setup.output == text

    # check that the values are written correctly
    config = load_config(user_config)
    assert config.get("tracker:gitlab", "username") == "john-doe"
    assert config.get("scm-manager:gitlab", "username") == "john-doe"
    assert config.get("tracker:jira", "url") == "https://divio-ch.atlassian.net"
    assert config.get("tracker:jira", "username") == "john-doe"
    assert config.get("timer:harvest", "username") == "12345"
    assert config.get("timer:harvest", "user_id") == "67890"


def test_init_command(runner):
    setup, user_config = setup_lancet(runner)
    assert setup.exit_code == 0

    init, project_config = init_lancet(runner, user_config)
    assert init.exit_code == 0

    text = dedent(
        """
        Welcome to the Lancet init wizard.

        What should be the default base branch?
        Integration branch [master]: develop

        [Gitlab] found in your configuration.
        Please provide the Gitlab group and project ID:
        Group ID: 12345
        Project ID: 67890

        [JIRA] found in your configuration.
        Not fully supported yet.
        Please provide the Jira project key:
        Project Key: KEY

        [Harvest] found in your configuration.
        Please provide the Harvest project and task ID:
        Project ID: 09876
        Task ID: 54321

        There are 2 trackers defined, please choose a default one:
        (1) Gitlab, (2) Jira: 1

        Do you use a virtual environment for this project? [y/N]: n

        Configuration correctly written to "{}".\n""".format(project_config)
    ).lstrip()
    assert init.output == text

    # check that the values are written correctly
    config = load_config(project_config)
    assert config.get("lancet", "tracker") == "gitlab"
    assert config.get("lancet", "timer") == "harvest"
    assert config.get("tracker", "active_status") == "doing"
    assert config.get("tracker", "paused_status") == "onhold"
    assert config.get("tracker", "review_status") == "review"
    assert config.get("tracker:gitlab", "project_id") == "67890"
    assert config.get("tracker:gitlab", "group_id") == "12345"
    assert config.get("tracker:jira", "project_id") == "KEY"
    assert config.get("repository", "base_branch") == "develop"
    assert config.get("timer:harvest", "project_id") == "9876"
    assert config.get("timer:harvest", "task_id") == "54321"
