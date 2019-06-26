from tabula import read_pdf
import pandas as pd
import re, glob

files = glob.glob('pdfs/*.pdf')

def pdf_to_df(pdf):
    df = read_pdf(pdf)
    df.dropna(axis=1, how='all', inplace=True)
    df.columns = ['measure', 'ref', 'pre', 'pre%', 'ci', 'post', 'post%', 'post_chg']
    df.dropna(axis=0, subset=['measure'], inplace=True)
    df['id'] = re.sub(r'(pdfs[/\\]+)(\d+)(_.*)', r'\2', pdf)
    df2 = df.set_index(['id', 'measure']).unstack('measure')
    return df2

dfs = []
for file in files:
    dfs.append(pdf_to_df(file))

dfs = pd.concat(dfs)
print(dfs.head())
