from pathlib import Path
import ast
import json
import sys
import pandas as pd

BASE = Path(__file__).resolve().parent
files = ['data/day.csv', 'data/hour.csv', 'dashboard/main_data.csv',
         'dashboard/dashboard.py', 'notebook.ipynb', 'README.md', 'requirements.txt']
for file in files:
    assert (BASE / file).is_file(), f'Berkas wajib tidak ada: {file}'
assert (BASE / 'requirements.txt').read_text(encoding='utf-8').strip()
assert 'streamlit' in (BASE / 'requirements.txt').read_text(encoding='utf-8').lower()

nb = json.loads((BASE / 'notebook.ipynb').read_text(encoding='utf-8'))
assert nb['nbformat'] == 4
header = ''.join(nb['cells'][0]['source'])
assert '[ISI ' not in header, 'Identitas notebook belum lengkap.'
assert header.count('@') == 1, 'Periksa kembali ejaan email di notebook.'
assert sum(c['cell_type']=='code' for c in nb['cells']) >= 7
assert all(c.get('execution_count') is not None for c in nb['cells'] if c['cell_type']=='code'), 'Ada kode notebook belum dijalankan.'
assert not any(out.get('output_type')=='error' for c in nb['cells'] if c['cell_type']=='code' for out in c['outputs']), 'Ada error di output notebook.'
ast.parse((BASE / 'dashboard/dashboard.py').read_text(encoding='utf-8'))

day = pd.read_csv(BASE / 'data/day.csv', parse_dates=['dteday'])
hour = pd.read_csv(BASE / 'data/hour.csv', parse_dates=['dteday'])
main = pd.read_csv(BASE / 'dashboard/main_data.csv', parse_dates=['dteday'])
assert len(day)==731 and len(hour)==17379 and len(main)==17544
assert len(main)==24*len(day)
assert not main.duplicated(['dteday','hr']).any()
assert main.groupby('dteday').size().eq(24).all()
assert main['cnt'].ge(0).all()
assert main['tingkat_permintaan'].isin(['Rendah','Sedang','Tinggi']).all()
assert main['cnt'].sum() == day['cnt'].sum() == hour['cnt'].sum()
assert main.groupby('dteday')['cnt'].sum().sort_index().equals(day.set_index('dteday')['cnt'].sort_index())
assert main.groupby('dteday')['jenis_hari'].nunique().eq(1).all()
assert (main['casual']+main['registered']==main['cnt']).all()
print('LULUS: Berkas utama lengkap, notebook sudah dieksekusi tanpa error, sintaks dashboard valid,')
print('      24 slot per hari lengkap, jumlah penyewaan konsisten, kategori binning valid.')
print('CATATAN: Script ini tidak menguji tampilan Streamlit; jalankan aplikasi secara lokal sebelum submit.')
