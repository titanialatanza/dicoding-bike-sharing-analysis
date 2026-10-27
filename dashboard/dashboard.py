from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Bike Sharing | Analisis Permintaan', page_icon='🚲', layout='wide')

WARNA_KERJA = '#185ABD'
WARNA_NONKERJA = '#E07B39'
URUT_HARI = ['Hari kerja', 'Hari non-kerja']
BULAN = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']


def format_id(angka, desimal=0):
    return f'{angka:,.{desimal}f}'.replace(',', '_').replace('.', ',').replace('_', '.')


@st.cache_data
def muat_data():
    path = Path(__file__).resolve().parent / 'main_data.csv'
    df = pd.read_csv(path, parse_dates=['dteday'])
    wajib = {'dteday', 'hr', 'cnt', 'jenis_hari', 'tahun', 'bulan', 'tingkat_permintaan'}
    if not wajib.issubset(df.columns):
        raise ValueError('Kolom utama data dashboard tidak lengkap.')
    if df.duplicated(['dteday', 'hr']).any() or df['cnt'].isna().any() or df['cnt'].lt(0).any():
        raise ValueError('Dataset dashboard mempunyai kunci berulang atau jumlah penyewaan tidak valid.')
    if not df.groupby('dteday').size().eq(24).all():
        raise ValueError('Dataset dashboard harus memiliki 24 slot jam per hari.')
    return df


try:
    df = muat_data()
except (OSError, ValueError) as error:
    st.error(f'Gagal membaca dashboard/main_data.csv: {error}')
    st.stop()

st.title('🚲 Bike Sharing — Pola Permintaan')
st.caption('Analisis deskriptif Capital Bikeshare, Washington, D.C. | Januari 2011–Desember 2012')

with st.sidebar:
    st.header('Filter analisis')
    pilihan = st.selectbox('Periode tahun', ['2011 & 2012', '2011', '2012'], index=0)
    st.markdown('**Definisi jenis hari**')
    st.caption('Hari kerja: bukan akhir pekan dan bukan hari libur. Hari non-kerja: akhir pekan atau hari libur.')
    st.caption('Sumber: Bike Sharing Dataset dari materi proyek Dicoding.')

if pilihan == '2011 & 2012':
    data = df.copy()
else:
    data = df[df['tahun'].eq(int(pilihan))].copy()

# Ringkasan harian dihitung setelah konsolidasi 24 jam, bukan rata-rata baris per jam.
harian = (data.groupby(['dteday', 'jenis_hari', 'bulan'], as_index=False)['cnt'].sum())
per_bulan = harian.groupby(['bulan', 'jenis_hari'], as_index=False)['cnt'].mean()
per_jam = data.groupby(['jenis_hari', 'hr'], as_index=False)['cnt'].mean()
puncak = per_jam.loc[per_jam.groupby('jenis_hari')['cnt'].idxmax()].set_index('jenis_hari')

col1, col2, col3, col4 = st.columns(4)
col1.metric('Total penyewaan', format_id(data['cnt'].sum()))
col2.metric('Rata-rata per hari', format_id(harian['cnt'].mean(), 1))
col3.metric('Puncak hari kerja', f"{int(puncak.loc['Hari kerja', 'hr']):02d}.00",
            help='Jam dengan rata-rata penyewaan per jam tertinggi pada hari kerja')
col4.metric('Puncak non-kerja', f"{int(puncak.loc['Hari non-kerja', 'hr']):02d}.00",
            help='Jam dengan rata-rata penyewaan per jam tertinggi pada hari non-kerja')

st.divider()
st.subheader('1. Perbandingan permintaan harian menurut bulan')
st.write('Bagaimana rata-rata **penyewaan per hari** berbeda antara hari kerja dan non-kerja sepanjang bulan kalender?')

fig1, ax1 = plt.subplots(figsize=(10, 4.3))
for jenis, warna in [('Hari kerja', WARNA_KERJA), ('Hari non-kerja', WARNA_NONKERJA)]:
    baris = per_bulan[per_bulan['jenis_hari'].eq(jenis)].sort_values('bulan')
    ax1.plot(baris['bulan'], baris['cnt'], color=warna, linewidth=2.5, marker='o', markersize=4.5, label=jenis)
ax1.set(xlabel='Bulan kalender', ylabel='Rata-rata penyewaan per hari')
ax1.set_xticks(range(1, 13), BULAN)
ax1.set_ylim(bottom=0)
ax1.grid(axis='y', linestyle='--', alpha=0.25)
ax1.spines[['top', 'right']].set_visible(False)
ax1.legend(frameon=False)
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

beda = per_bulan.pivot(index='bulan', columns='jenis_hari', values='cnt')
beda['selisih'] = beda['Hari kerja'] - beda['Hari non-kerja']
bulan_maks = int(beda['selisih'].abs().idxmax())
jenis_unggul = 'hari kerja' if beda.loc[bulan_maks, 'selisih'] > 0 else 'hari non-kerja'
st.info(
    f"Selisih absolut rata-rata harian terbesar terjadi pada **{BULAN[bulan_maks - 1]}**: "
    f"**{format_id(abs(beda.loc[bulan_maks, 'selisih']), 1)}** penyewaan per hari, "
    f"dengan rata-rata **{jenis_unggul}** lebih tinggi."
)

st.divider()
st.subheader('2. Jam puncak pada hari kerja dan non-kerja')
st.write('Rata-rata **penyewaan per jam** dihitung dari seluruh 24 slot jam setiap hari, termasuk slot tanpa penyewaan.')
fig2, ax2 = plt.subplots(figsize=(10, 4.3))
for jenis, warna in [('Hari kerja', WARNA_KERJA), ('Hari non-kerja', WARNA_NONKERJA)]:
    baris = per_jam[per_jam['jenis_hari'].eq(jenis)].sort_values('hr')
    ax2.plot(baris['hr'], baris['cnt'], color=warna, linewidth=2.5, marker='o', markersize=4, label=jenis)
ax2.set(xlabel='Jam (00–23)', ylabel='Rata-rata penyewaan per jam')
ax2.set_xticks(range(24))
ax2.set_ylim(bottom=0)
ax2.grid(axis='y', linestyle='--', alpha=0.25)
ax2.spines[['top', 'right']].set_visible(False)
ax2.legend(frameon=False)
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

r1, r2 = st.columns(2)
with r1:
    baris = puncak.loc['Hari kerja']
    st.write(f"**Hari kerja:** puncak {int(baris['hr']):02d}.00–{int(baris['hr']):02d}.59, "
             f"rata-rata **{format_id(baris['cnt'], 1)}** penyewaan per jam.")
with r2:
    baris = puncak.loc['Hari non-kerja']
    st.write(f"**Hari non-kerja:** puncak {int(baris['hr']):02d}.00–{int(baris['hr']):02d}.59, "
             f"rata-rata **{format_id(baris['cnt'], 1)}** penyewaan per jam.")

st.divider()
st.subheader('3. Segmentasi permintaan per jam (binning)')
st.write('Proporsi slot jam yang masuk kategori **Tinggi**. Ambang tiga kelompok ditetapkan '
         'berdasarkan persentil data lengkap 2011–2012, bukan dipelajari ulang saat filter tahun berubah.')
ringkasan = (data.assign(tinggi=data['tingkat_permintaan'].eq('Tinggi'))
             .groupby(['jenis_hari', 'hr'])['tinggi'].mean().mul(100).unstack('hr').reindex(URUT_HARI))
fig3, ax3 = plt.subplots(figsize=(10, 2.9))
im = ax3.imshow(ringkasan.to_numpy(), cmap='Blues', vmin=0, vmax=100, aspect='auto')
ax3.set(xticks=range(24), xticklabels=range(24), yticks=[0, 1], yticklabels=URUT_HARI,
        xlabel='Jam (00–23)')
fig3.colorbar(im, ax=ax3, shrink=0.9, pad=0.02, label='Proporsi kategori Tinggi (%)')
fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

with st.expander('Metodologi, keterbatasan, dan sumber'):
    st.markdown("""
    - **Data:** `day.csv` (731 hari) dan `hour.csv` (17.379 slot teramati); periode 2011–2012.
    - **Pembersihan:** 165 slot jam tanpa catatan dilengkapi menjadi 0 penyewaan setelah setiap total harian dicocokkan dengan file harian. Data dashboard berisi 17.544 slot.
    - **Definisi:** Jumlah penyewaan bukan jumlah pelanggan unik. Pengelompokan bulan bersifat **bulan kalender**.
    - **Binning:** Label Rendah/Sedang/Tinggi berasal dari dua batas persentil dataset 2011–2012. Proporsi kategori Tinggi bukan prediksi.
    - **Batasan:** Tidak tersedia lokasi stasiun, kapasitas sepeda, dan biaya operasional; analisis deskriptif tidak menyimpulkan sebab-akibat.
    - **Sumber:** Fanaee-T, H. & Gama, J. (2013), *Event labeling combining ensemble detectors and background knowledge*, Progress in Artificial Intelligence. [Dokumentasi UCI](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset).
    """)
st.caption('Rekomendasi: tinjau armada sebelum 08.00 dan 17.00 pada hari kerja, dan sebelum 12.00–14.00 pada hari non-kerja. Validasi dengan data stasiun dan stok aktual.')
