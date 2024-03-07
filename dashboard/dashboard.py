import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul aplikasi
st.title('Aplikasi Dashboard Interaktif Peminjaman Sepeda')

# Muat data
@st.cache_data
def load_data():
    df_day = pd.read_csv('D:\submission\dashboard\day.csv')
    return df_day

df_day = load_data()

# Cleaning data
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

# Terjemahan kategori cuaca dan tahun
weathersit_translation = {1: 'Cerah', 2: 'Kabut', 3: 'Salju dan Hujan ringan', 4: 'Hujan lebat dan Salju berkabut'}
yr_translation = {0: '2011', 1: '2012'}

# Menerjemahkan fitur 'weathersit' dan 'yr' di DataFrame
df_day['weathersit'] = df_day['weathersit'].map(weathersit_translation)
df_day['yr'] = df_day['yr'].map(yr_translation)

# Pilih tahun
year = st.selectbox('Pilih Tahun', options=['2011', '2012', 'Keduanya'])
if year != 'Keduanya':
    df_day = df_day[df_day['yr'] == year]

# Visualisasi line chart
st.subheader('Tren Rata-rata Peminjaman Sepeda')
df_grouped = df_day.groupby('dteday')['cnt'].mean()
st.line_chart(df_grouped)

# Visualisasi bar plot
st.subheader('Jumlah Peminjaman Sepeda Tiap Cuaca dan Musim')

# Buat subplot
fig, axes = plt.subplots(2, 1, figsize=(10, 12))

# Plot cuaca
sns.barplot(x='weathersit', y='cnt', hue='yr', data=df_day, ax=axes[0], order=weathersit_translation.values(), errorbar=None)
axes[0].set_title('Jumlah Peminjaman Sepeda Tiap Cuaca')
axes[0].legend(title='Tahun')
axes[0].set_xlabel('')
axes[0].set_ylabel('')

# Plot musim
season_translation = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
df_day['season'] = df_day['season'].map(season_translation)
sns.barplot(x='season', y='cnt', hue='yr', data=df_day, ax=axes[1], order=season_translation.values(), errorbar=None)
axes[1].set_title('Jumlah Peminjaman Sepeda Tiap Musim')
axes[1].legend(title='Tahun')
axes[1].set_xlabel('')
axes[1].set_ylabel('')


# Tampilkan plot
st.pyplot(fig)

# Stackbarchart
st.subheader('Jumlah Hari dalam Setiap Bulan untuk Setiap Kategori Peminjaman Sepeda')

# Buat salinan DataFrame
df_copy = df_day.copy()

# Ekstrak bulan dari 'dteday'
df_copy['month'] = df_copy['dteday'].dt.month

# Hitung Q1 dan Q3
Q1 = df_copy['cnt'].quantile(0.25)
Q3 = df_copy['cnt'].quantile(0.75)

# Fungsi untuk mengkategorikan jumlah peminjaman
def categorize(cnt):
    if cnt < Q1:
        return 'Sedikit'
    elif cnt < Q3:
        return 'Sedang'
    else:
        return 'Banyak'

# Terapkan fungsi ke 'cnt'
df_copy['cnt_category'] = df_copy['cnt'].apply(categorize)

# Buat tabel pivot
pivot_table = pd.pivot_table(df_copy, index='month', columns='cnt_category', aggfunc='size', fill_value=0)

# Buat plot
fig, ax = plt.subplots(figsize=(15, 9))
pivot_table.plot(kind='bar', stacked=True, ax=ax)

# Atur judul dan label sumbu
ax.set_xlabel('Bulan')
ax.set_ylabel('')

# Tampilkan plot
st.pyplot(fig)

# Heatmap
st.subheader('Heatmap Korelasi Fitur-Fitur Numerik')

# Memilih fitur numerik
features = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']
df_selected = df_day[features]

# Menghitung korelasi antara fitur
corr = df_selected.corr()

# Membuat mask untuk segitiga bawah
mask = np.triu(np.ones_like(corr, dtype=bool))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

fig, ax = plt.subplots(figsize=(6, 8))
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, ax=ax)

plt.xticks(rotation=45)
plt.tight_layout()

# Tampilkan plot
st.pyplot(fig)