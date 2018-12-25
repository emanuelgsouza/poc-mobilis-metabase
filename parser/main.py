import pandas as pd
import uuid
from datetime import datetime
import psycopg2

CSV_FILE_PATH = 'data/raw.csv'


def set_uuid_column(df):
  dfl = df.copy()

  rows = dfl.to_dict(orient='index').values()
  data = []
  for row in rows:
    row['uuid'] = uuid.uuid1()
    data.append(row)
  
  return pd.DataFrame(data)


def set_created_at(df):
  dfl = df.copy()
  indexes = dfl.index.to_series()
  year = dfl['Data']
  res = pd.concat([indexes, year], axis=1, ignore_index=False).rename(index=str, columns={0: "Dia"})
  dfl.loc[:, 'created_at'] = res.apply(lambda row : '{} {}'.format(row['Dia'], row['Data']), axis=1)
  return dfl


def set_index(df):
  dfl = df.copy()
  dfl.loc[:, 'index'] = list(range(len(dfl)))
  dfl = dfl.set_index('index')
  return dfl


def rename_columns(df):
  dfl = df.copy()
  dfl = dfl.rename(index=str, columns={
    'Data': 'date',
    'Descrição': 'description',
    'Valor': 'value',
    'Categoria': 'category',
    'Conta': 'account'
  })

  return dfl


def drop_columns(df, columns=['date']):
  dfl = df.copy()
  dfl = dfl.drop(columns, axis=1)

  return dfl


def clean_data(df):
  dfl = df.copy()
  dfl.loc[:, 'value'] = dfl['value'].apply(lambda x : float(x.replace('R$', '')))
  dfl.loc[:, 'created_at'] = dfl['created_at'].apply(lambda x : datetime.strptime(x, '%d %b %Y'))

  return dfl


def set_transaction_type_column(df):
  dfl = df.copy()
  dfl.loc[:, 'transaction_type'] = dfl['value'].map(lambda x : 'S' if x < 0 else 'E')
  return dfl


def process_value_column(df):
  dfl = df.copy()
  df.loc[:, 'value'] = dfl['value'].map(lambda x : x * -1 if x < 0 else x)
  return df


def process_database(csv_path):
  # set here, the same variables at docker-compose database service
  conn = psycopg2.connect("host=localhost dbname= user=")
  cur = conn.cursor()
  cur.execute("""
      drop table if exists transactions;

      create table if not exists transactions (
          uuid uuid,
          description varchar,
          created_at date,
          value numeric(15, 2),
          category varchar,
          account varchar,
          trasaction_type varchar
      );
  """)
  conn.commit()

  with open(csv_path, 'r') as f:
      next(f)  # Skip the header row.
      print('Save data to database')
      cur.copy_from(f, 'transactions', sep=',')
      
  conn.commit()

def process_csv(df):
  print('Init process csv file')

  print('Compute created_at column')
  df = set_created_at(df=df)

  print('Rename columns')
  df = rename_columns(df=df)

  print('Drop unnecessary columns')
  df = drop_columns(df=df)

  print('Update index')
  df = set_index(df=df)

  print('Set uuid column')
  df = set_uuid_column(df=df)

  print('Clean data')
  df = clean_data(df=df)

  print('Set transaction type column')
  df = set_transaction_type_column(df=df)

  print('Process value column')
  df = process_value_column(df=df)

  print('Ordering columns')
  df = df[['uuid', 'description', 'created_at', 'value', 'category', 'account', 'transaction_type']]

  print('Save data to raw.csv')
  df.to_csv(CSV_FILE_PATH, index=False)

  print('Execute statements at database')
  process_database(csv_path=CSV_FILE_PATH)
