import pandas as pd
import click
from parser.main import process_csv


@click.command()
@click.option('--csv')
def main(csv):
  df = pd.read_csv(csv)
  process_csv(df=df)

if __name__ == '__main__':
  main()
