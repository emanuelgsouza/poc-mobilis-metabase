import pandas as pd
import uuid

transaction_df_props = [
  'uuid',
  'created_at',
  'month',
  'year',
  'description',
  'value',
  'category',
  'account'
]


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

  df.to_csv('data/raw.csv', index=False)
