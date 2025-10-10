from karnai.cli.karnai import app
from typer.testing import CliRunner

runner = CliRunner()


def test_cli_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0
    assert "KarnAI" in r.stdout


def test_cli_play_smoke():
    r = runner.invoke(app, ["play", "--seed", "123"])
    assert r.exit_code == 0
    assert "Seed:" in r.stdout
