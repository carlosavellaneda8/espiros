from tabula import read_pdf
import pandas as pd
import re, glob

files = glob.glob('pdfs/*.pdf')

def pdf_to_df(pdf):
    df = read_pdf(pdf)
    # Remove NAs columns:
    df.dropna(axis=1, how='all', inplace=True)
    # Rename columns:
    df.columns = ['measure', 'ref', 'pre', 'pre%', 'ci', 'post', 'post%', 'post_chg']
    # Drop wrong rows:
    df.dropna(axis=0, subset=['measure'], inplace=True)
    # Get IDs from filename:
    df['id'] = re.sub(r'(pdfs[/\\]+)(\d+)(_.*)', r'\2', pdf)
    # Reshape data:
    df = df.set_index(['id', 'measure']).unstack('measure')
    return df

dfs = []
for file in files:
    dfs.append(pdf_to_df(file))

dfs = pd.concat(dfs)
print(dfs.head())

dfs.to_excel('data/output.xlsx')
