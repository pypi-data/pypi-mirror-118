import configparser
import os

import click

from ..settings import get_project_config, get_user_config


@click.command()
@click.option(
    "-f",
    "--force/--no-force",
    default=False,
    help="Setup even if .lancet already exists.",
)
@click.option(
    "-d",
    "--debug/--no-debug",
    default=False,
    help="Adds additional steps to the wizard for debugging.",
)
@click.pass_context
def setup(ctx, force, debug):
    """Wizard to create a user-level configuration file."""

    user_config = get_user_config()

    if os.path.exists(user_config) and not force:
        click.secho(
            'An existing configuration file was found at "{}".'.format(user_config),
            fg="red",
            bold=True,
        )
        raise click.ClickException(
            "Please remove it before in order to run the setup wizard or use the\n"
            "--force flag to overwrite it."
        )

    # setting up wizard
    config = configparser.ConfigParser()
    config.add_section("lancet")

    current_step = 1
    total_steps = 3
    if debug:
        total_steps += 1

    # configurator
    click.secho("Welcome to the Lancet setup wizard.")
    click.secho("Please choose a tracker:")
    tracker = click.prompt("(1) Gitlab, (2) Jira, (3) Both", type=int)
    click.secho()

    if tracker > 3 or tracker == 0:
        raise click.ClickException("Please provide a valid numerical choice.")

    if tracker == 3:
        total_steps += 1

    # Gitlab
    if tracker == 1 or tracker == 3:
        config.add_section("tracker:gitlab")
        config.add_section("scm-manager:gitlab")
        # configure gitlab
        click.secho("Step {} of {}".format(current_step, total_steps))
        click.secho("Enter your Gitlab username:")
        gitlab_user = click.prompt("Username")
        click.secho()
        current_step += 1
        config.set("tracker:gitlab", "username", gitlab_user)
        config.set("scm-manager:gitlab", "username", gitlab_user)

    # Jira
    if tracker == 2 or tracker == 3:
        config.add_section("tracker:jira")
        # configure gitlab
        click.secho("Step {} of {}".format(current_step, total_steps))
        click.secho("Enter your Jira username:")
        gitlab_user = click.prompt("Username")
        click.secho()
        current_step += 1
        config.set("tracker:jira", "url", "https://divio-ch.atlassian.net")
        config.set("tracker:jira", "username", gitlab_user)

    # Harvest
    config.add_section("timer:harvest")
    click.secho("Step {} of {}".format(current_step, total_steps))
    click.secho(
        "Enter the Harvest account ID:\n"
        "(You can get it from https://id.getharvest.com/developers)"
    )
    timer_id = click.prompt("Accound ID", type=int)
    click.secho()
    current_step += 1

    click.secho("Step {} of {}".format(current_step, total_steps))
    click.secho(
        "Enter the Harvest ID found on your profile's URL:\n"
        "(You can get it from https://divio.harvestapp.com/people/<YOUR_ID>/)"
    )
    timer_user = click.prompt("User ID", type=int)
    click.secho()
    current_step += 1
    config.set("timer:harvest", "username", str(timer_id))
    config.set("timer:harvest", "user_id", str(timer_user))

    if debug:
        click.secho(
            "Running with --debug, additional setup parameters will "
            "be requested.",
            fg="green",
            bold=True,
        )
        click.secho("Step {} of {}".format(current_step, total_steps))
        click.secho("Please provide the SENTRY_DSN link:")
        sentry_dsn = click.prompt("Sentry DSN")
        click.secho()
        current_step += 1
        config.set("lancet", "sentry_dsn", sentry_dsn)

    with open(user_config, "w") as fh:
        config.write(fh)

    click.secho(
        'Configuration correctly written to "{}".'.format(user_config), fg="green"
    )


@click.command()
@click.option(
    "-f",
    "--force/--no-force",
    default=False,
    help="Init even if .lancet already exists.",
)
@click.pass_context
def init(ctx, force):
    """Wizard to create a project-level configuration file."""

    project_config = get_project_config()

    if os.path.exists(project_config) and not force:
        click.secho(
            'An existing configuration file was found at "{}".'.format(project_config),
            fg="red",
            bold=True,
        )
        raise click.ClickException(
            "Please remove it before in order to run the setup wizard or use the\n"
            "--force flag to overwrite it."
        )

    # setting up wizard
    config = configparser.ConfigParser()
    config.add_section("lancet")
    trackers = []

    # configurator
    click.secho("Welcome to the Lancet init wizard.")

    def get_config(key, value):
        return ctx.obj.config.get(key, value)

    # TODO for now we generate this without the configurator.
    # Needs testing, deploy and done status as well, maybe
    # we can pass an array and then process through it sequentially
    # to be reviewed when tackling the issue implementation
    config.add_section("tracker")
    config.set("tracker", "active_status", "doing")
    config.set("tracker", "paused_status", "onhold")
    config.set("tracker", "review_status", "review")

    click.secho()
    click.secho("What should be the default base branch?")
    base_branch = click.prompt("Integration branch", default="master")

    config.add_section("repository")
    config.set("repository", "base_branch", base_branch)

    # Gitlab configurator
    gitlab = get_config("tracker:gitlab", "username")
    if gitlab:
        config.add_section("tracker:gitlab")
        trackers.append("gitlab")

        click.secho()
        click.secho("[Gitlab] found in your configuration.", fg="green")
        click.secho("Please provide the Gitlab group and project ID:")
        gitlab_group = click.prompt("Group ID", type=int)
        gitlab_id = click.prompt("Project ID", type=int)

        # write config
        config.set("tracker:gitlab", "project_id", str(gitlab_id))
        config.set("tracker:gitlab", "group_id", str(gitlab_group))

    # Jira configurator
    jira = get_config("tracker:jira", "username")
    if jira:
        config.add_section("tracker:jira")
        trackers.append("jira")

        click.secho()
        click.secho("[JIRA] found in your configuration.", fg="green")
        click.secho("Not fully supported yet.", fg="yellow")
        click.secho("Please provide the Jira project key:")
        jira_key = click.prompt("Project Key")

        config.set("tracker:jira", "project_id", str(jira_key))

    # Harvest configurator
    timer = get_config("timer:harvest", "username")
    if timer:
        click.secho()
        click.secho("[Harvest] found in your configuration.", fg="green")
        click.secho("Please provide the Harvest project and task ID:")
        harvest_project = click.prompt("Project ID", type=int)
        harvest_task = click.prompt("Task ID", type=int)
        click.secho()

        # write config
        config.set("lancet", "tracker", "harvest")
        config.add_section("timer:harvest")
        config.set("timer:harvest", "project_id", str(harvest_project))
        config.set("timer:harvest", "task_id", str(harvest_task))

    # multiple trackers available, choose which one to use
    if len(trackers) > 1:
        click.secho(
            "There are {} trackers defined, please choose a default one:"
            .format(len(trackers))
        )
        text = ["({}) {}".format(i+1, t.capitalize()) for i, t in enumerate(trackers)]
        default = click.prompt(", ".join(text), type=int)
        if default > len(trackers) or default == 0:
            raise click.ClickException("Please provide a valid numerical choice.")
        config.set("lancet", "tracker", trackers[default-1])
        click.secho()
    else:
        config.set("lancet", "tracker", trackers[0])

    # configure virtuel environment
    if click.confirm(
            "Do you use a virtual environment for this project?",
        ):
        virtualenvs = (".venv", ".env", "venv", "env")
        for p in virtualenvs:
            if os.path.exists(os.path.join(p, "bin", "activate")):
                venv = p
                break
        else:
            venv = ""
        venv_path = click.prompt("Path to virtual environment", default=venv)
        # write config
        config.set("lancet", "virtualenv", venv_path)

    with open(project_config, "w") as fh:
        config.write(fh)

    click.secho()
    click.secho(
        'Configuration correctly written to "{}".'.format(project_config), fg="green"
    )
