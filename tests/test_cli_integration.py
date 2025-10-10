import subprocess
import sys


def test_cli_help_runs():
    result = subprocess.run(
        [sys.executable, "-m", "karnai.cli.karnai", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "setup" in result.stdout


def test_cli_train_runs():
    result = subprocess.run(
        [sys.executable, "-m", "karnai.cli.karnai", "train", "--episodes", "2"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Evaluation Results" in result.stdout
