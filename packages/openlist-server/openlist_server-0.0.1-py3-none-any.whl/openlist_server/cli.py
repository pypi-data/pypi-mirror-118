import click


@click.command()
def run():
    """
    Starts OpenList backend server API.
    """
    print("Hello from OpenList!")


if __name__ == "__main__":
    run()
