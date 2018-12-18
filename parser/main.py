from pandas import concat

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


def set_created_at(df):
  dfl = df.copy()
  indexes = dfl.index.to_series()
  year = dfl['Data']
  res = concat([indexes, year], axis=1, ignore_index=False).rename(index=str, columns={0: "Dia"})
  dfl.loc[:, 'created_at'] = res.apply(lambda row : '{} {}'.format(row['Dia'], row['Data']), axis=1)
  return dfl


def set_index(df):
  dfl = df.copy()
  dfl.loc[:, 'index'] = list(range(len(dfl)))
  dfl.set_index('index')
  return dfl


def rename_columns(df):
  dfl = df.copy()
  dfl.rename(index=int, columns={
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


def process_csv(csv):
  pass
