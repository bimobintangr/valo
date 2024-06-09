import streamlit as st
import pandas as pd

# Mengatur konfigurasi halaman
st.set_page_config(layout="wide")

# CSS untuk mengatur background dan warna teks
page_bg_img = '''
<style>
.stApp {
    background: #0F1923; /* Background color sesuai tema logo */
    color: #F74D60; /* Font color sesuai tema logo */
}
header {
    background: #0F1923;
}
.css-1aumxhk {
    background: #0F1923;
}
h1 {
    color: #FF4655; /* Warna merah lebih terang untuk judul utama */
}
h2, h3 {
    color: #FF4655; /* Warna merah lebih terang untuk header */
}
table {
    color: #F74D60; /* Warna font tabel */
    background-color: #0F1923; /* Warna background tabel */
}
thead th {
    color: #FF4655; /* Warna font header tabel */
    background-color: #0F1923; /* Warna background header tabel */
}
tbody tr:nth-child(even) {
    background-color: #1c2b36; /* Warna background baris genap */
}
tbody tr:nth-child(odd) {
    background-color: #0F1923; /* Warna background baris ganjil */
}
tbody td {
    color: #F74D60; /* Warna font isi tabel */
}
</style>
'''

# Menambahkan CSS ke Streamlit
st.markdown(page_bg_img, unsafe_allow_html=True)

# Judul aplikasi
st.title("Valorant Agent Information")

# Deskripsi aplikasi
st.write("""
This is a web application to display Valorant agents' information including their roles, ultimate abilities, and best maps.
""")

# Load dataset
df = pd.read_csv('valorant_agents_updated.csv')

# Rename columns to English
df = df.rename(columns={
    'Nama': 'Name',
    'Peran': 'Role',
    'Kemampuan Ultimate': 'Ultimate Ability',
    'Peta Terbaik': 'Best Maps',
    'Kemampuan 1': 'Ability 1',
    'Kemampuan 2': 'Ability 2',
    'Kemampuan 3': 'Ability 3'
})

# Filter berdasarkan peran
st.sidebar.header("Filter")
roles = ["All"] + list(df["Role"].unique())
role_filter = st.sidebar.multiselect("Select Role:", options=roles, default="All")

# Filter dataset
if "All" in role_filter:
    filtered_df = df.sort_values(by=["Role", "Name"]).reset_index(drop=True)
else:
    filtered_df = df[df["Role"].isin(role_filter)].sort_values(by=["Role", "Name"]).reset_index(drop=True)

# Tambahkan kolom indeks yang dimulai dari 1
filtered_df.index = filtered_df.index + 1
filtered_df.reset_index(inplace=True)
filtered_df.rename(columns={'index': 'No'}, inplace=True)

# Drop the 'ID' column
filtered_df = filtered_df.drop(columns=["ID"])

# Opsi untuk menampilkan tabel agen
st.header("Valorant Agents")
st.dataframe(filtered_df.reset_index(drop=True))

# Pilih Agen
st.sidebar.header("Agent Details")
agent_selected = st.sidebar.selectbox("Select Agent:", filtered_df["Name"])

# Layout untuk menampilkan logo di samping kanan detail agen
col1, col2 = st.columns([4, 1])

with col1:
    agent_details = filtered_df[filtered_df["Name"] == agent_selected]

    if not agent_details.empty:
        st.header(f"Agent Details: {agent_selected}")
        st.write(f"**Role:** {agent_details['Role'].values[0]}")
        st.write(f"**Ultimate Ability:** {agent_details['Ultimate Ability'].values[0]}")
        st.write(f"**Best Maps:** {agent_details['Best Maps'].values[0]}")
        st.write(f"**Ability 1:** {agent_details['Ability 1'].values[0]}")
        st.write(f"**Ability 2:** {agent_details['Ability 2'].values[0]}")
        st.write(f"**Ability 3:** {agent_details['Ability 3'].values[0]}")
    else:
        st.write("No agent data found.")

with col2:
    st.image('valoo.jpg', use_column_width=True)

# Menjalankan aplikasi
if __name__ == '__main__':
    pass
