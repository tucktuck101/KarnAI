import typer
from rich.console import Console
from rich.table import Table
from karnai.eval import run_head_to_head, EvalConfig
from karnai.env import KarnAIGymEnv

console = Console()
app = typer.Typer(help="KarnAI CLI")


@app.command()
def version():
    """Print version banner."""
    console.print("KarnAI CLI v0.1")


@app.command()
def play(seed: int = typer.Option(0, help="RNG seed")):
    """Smoke-run the env once."""
    env = KarnAIGymEnv(seed=seed)
    obs, _ = env.reset()
    console.print(f"Seed: {seed}")
    console.print(f"Obs: {obs}")
    env.close()


@app.command()
def setup():
    """Placeholder setup."""
    console.print("[bold green]Environment setup complete.[/bold green]")


@app.command()
def train(episodes: int = 4, seed: int = 0):
    """Run sample evaluation between two dummy policies."""
    from dataclasses import dataclass

    @dataclass
    class AlwaysPass:
        def capabilities(self):
            return {"stochastic": False}

        def act(self, observation):
            return {"type": "pass_priority"}

        def reset(self, seed=None): ...

    cfg = EvalConfig(episodes=episodes, seed=seed)
    pol_a = AlwaysPass()
    pol_b = AlwaysPass()
    res, ratings = run_head_to_head(pol_a, pol_b, cfg)

    t = Table(title="Evaluation Results")
    t.add_column("Metric")
    t.add_column("Value")
    t.add_row("Wins A", str(res.wins_a))
    t.add_row("Wins B", str(res.wins_b))
    t.add_row("Draws", str(res.draws))
    t.add_row("Rating A", f"{ratings['A']:.2f}")
    t.add_row("Rating B", f"{ratings['B']:.2f}")
    console.print(t)


if __name__ == "__main__":
    app()
