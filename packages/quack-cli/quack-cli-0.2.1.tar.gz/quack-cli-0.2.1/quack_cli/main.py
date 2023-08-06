from typing import Optional

import typer
import requests

API_URL = "https://quackstack.pythondiscord.com"

app = typer.Typer()

@app.command()
def generate(ducktype: str = "duck", seed: Optional[str] = None) -> None:
    """
    Generates a duck from Quackstack and returns the link.
    """
    ducktype = ducktype.lower()
    if ducktype not in ["duck", "manduck"]:
        error = typer.style("Ducktype must be 'duck' or 'manduck'.", fg=typer.colors.RED)
        typer.echo(error)
        raise typer.Exit()
    params = {}
    if seed is not None:
        try:
            seed = int(seed)
        except ValueError:
            newseed = ""
            for e in seed:
                newseed += str(ord(e))
            seed = int(newseed)
        params["seed"] = seed
    r = requests.get(
        f"{API_URL}/{ducktype}",
        params=params
    )
    data = r.json()
    typer.echo("✨Generated Duck!✨")
    typer.echo(f"View at {API_URL}{data['file']}")
