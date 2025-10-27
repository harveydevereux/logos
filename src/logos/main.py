import typer


app = typer.Typer()

@app.command()                                                                  
def goodbye():                                                                    
    """                                                                         
    Say goodbye                                                                   
    """                                                                         
    typer.echo("Goodbye!")    

@app.command()
def hello():
    """
    Say hello
    """
    typer.echo("Hello!")
