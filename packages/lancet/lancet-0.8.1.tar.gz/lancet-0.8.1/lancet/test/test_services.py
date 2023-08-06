from ..cli import main
from .helpers import runner, set_lancet


def test_logout_command(runner):
    setup, init = set_lancet(runner)

    result = runner.invoke(main, "logout")
    assert result.exit_code == 0
    assert "*  Logging out from https://gitlab.com/..." in result.output
    assert "✓  Already logged out from https://gitlab.com/" in result.output
    assert "*  Logging out from https://api.harvestapp.com/v2/..." in result.output
    assert "✓  Already logged out from https://api.harvestapp.com/v2/" in result.output

    # logout with argument
    result = runner.invoke(main, "logout tracker")
    assert "*  Logging out from https://gitlab.com/..." in result.output
    assert "✓  Already logged out from https://gitlab.com/" in result.output
