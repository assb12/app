import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import datetime

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="VOID & RUST - Alternative Store", page_icon="🥀", layout="wide")

# --- CUSTOM CSS TEMA INDUSTRIAL GRUNGE ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0d0d0d;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
    }
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        letter-spacing: 3px;
        border-bottom: 1px solid #333;
        padding-bottom: 10px;
    }
    .sub-banner {
        background-color: #1a1a1a;
        color: #ff5555;
        padding: 6px;
        text-align: center;
        font-size: 11px;
        letter-spacing: 2px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE PRODUK ORISINAL (TEMA INDUSTRIAL / DARK STREETWEAR) ---
database_custom_grunge = {
    "V01": {
        "nama": "TOXIC WASTE OVERSIZED TEE", "harga": 850000, "kat": "Tops", "size": ["S", "M", "L", "XL"], 
        "desc": "Kaos boxy fit berat dengan sablon plastisol retak bertema distopia industrial.",
        "img_url": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=400&auto=format&fit=crop&q=80"
    },
    "V02": {
        "nama": "ASPHALT CARGO PANTS", "harga": 1650000, "kat": "Bottoms", "size": ["28", "30", "32", "34"], 
        "desc": "Celana kargo multi-pocket dengan tali serut gantung dan efek acid-wash kotor.",
        "img_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&auto=format&fit=crop&q=80"
    },
    "V03": {
        "nama": "OBSIDIAN LEATHER JACKET", "harga": 3400000, "kat": "Outerwear", "size": ["M", "L", "XL"], 
        "desc": "Jaket kulit imitasi vintage dengan aksen ring besi dan resimen ganda ala cyber-grunge.",
        "img_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&auto=format&fit=crop&q=80"
    },
    "V04": {
        "nama": "BLEEDING HEART KNIT SWEATER", "harga": 1200000, "kat": "Tops", "size": ["S", "M", "L"], 
        "desc": "Sweter rajut longgar dengan benang terurai acak di bagian ujung leher dan lengan.",
        "img_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&auto=format&fit=crop&q=80"
    }
}

# --- INISIALISASI STATE ---
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []
if 'member_poin' not in st.session_state:
    st.session_state.member_poin = 1500
if 'member_nama' not in st.session_state:
    st.session_state.member_nama = "JAJANG"
if 'voucher_aktif' not in st.session_state:
    st.session_state.voucher_aktif = False

# --- HEADER WEB ---
st.markdown('<div class="main-header">VOID & RUST® — ARCHIVE STORE</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-banner">⚠ LIMITED DROP SEASON 01 — USE CODE "VOID30" FOR 30% OFF ⚠</div>', unsafe_allow_html=True)

# --- TATA LETAK UTAMA (2 KOLOM) ---
col_kiri, col_kanan = st.columns([1.3, 1])

with col_kiri:
    st.subheader("💀 PRODUCT ARCHIVE")
    
    # Filter Kategori
    kategori_pilihan = st.selectbox("Filter Kategori:", ["Semua", "Tops", "Bottoms", "Outerwear"])
    
    # Pilihan Produk
    produk_tampil = {k: v for k, v in database_custom_grunge.items() if kategori_pilihan == "Semua" or v['kat'] == kategori_pilihan}
    pilihan_kode = st.selectbox("Pilih Item:", list(produk_tampil.keys()), format_func=lambda x: f"{x} - {produk_tampil[x]['nama']} (Rp {produk_tampil[x]['harga']:,})")
    
    selected_prod = database_custom_grunge[pilihan_kode]
    
    # Layout Detail & Preview (Rasio Gambar 3:4)
    sub_col1, sub_col2 = st.columns([1, 1])
    with sub_col1:
        try:
            response = requests.get(selected_prod['img_url'])
            img = Image.open(BytesIO(response.content))
            st.image(img, caption=selected_prod['nama'], use_column_width=True)
        except:
            st.warning("Gagal memuat gambar")
            
    with sub_col2:
        st.markdown(f"**{selected_prod['nama']}**")
        st.markdown(f"Harga: **Rp {selected_prod['harga']:,}**")
        st.markdown(f"*{selected_prod['desc']}*")
        
        size_pilih = st.selectbox("Ukuran:", selected_prod['size'])
        qty_pilih = st.number_input("Kuantitas:", min_value=1, value=1)
        
        if st.button("TAMBAHKAN KE TAS", use_container_width=True):
            subtotal = selected_prod['harga'] * qty_pilih
            st.session_state.keranjang.append({
                "nama": selected_prod['nama'],
                "size": size_pilih,
                "qty": qty_pilih,
                "subtotal": subtotal
            })
            st.success("Item berhasil dimasukkan ke tas belanja.")

with col_kanan:
    st.subheader("🛒 CART & CHECKOUT")
    
    st.info(f"👤 Member: {st.session_state.member_nama} | Poin: {st.session_state.member_poin} pts")
    
    if len(st.session_state.keranjang) > 0:
        for idx, item in enumerate(st.session_state.keranjang):
            st.markdown(f"- **{item['nama']}** ({item['size']}) x{item['qty']} : Rp {item['subtotal']:,}")
            
        if st.button("Kosongkan Tas"):
            st.session_state.keranjang = []
            st.rerun()
            
        st.divider()
        
        # Pilihan Kurir
        kurir = st.radio("Metode Pengiriman:", [
            "Regular Cargo (Rp 15.000)", 
            "Express Courier (Rp 30.000)", 
            "Instant Same-Day (Rp 50.000)"
        ])
        
        biaya_ongkir = 15000 if "Regular" in kurir else (30000 if "Express" in kurir else 50000)
        
        # Voucher Promo
        promo_input = st.text_input("Kode Promo (Coba 'VOID30'):")
        if promo_input == "VOID30":
            st.session_state.voucher_aktif = True
            st.success("Kode 'VOID30' aktif! Diskon 30% diterapkan.")
        
        # Hitung Total
        subtotal_all = sum([x['subtotal'] for x in st.session_state.keranjang])
        diskon = int(subtotal_all * 0.3) if st.session_state.voucher_aktif else 0
        total_akhir = (subtotal_all - diskon) + biaya_ongkir
        
        st.markdown(f"Subtotal: Rp {subtotal_all:,}")
        st.markdown(f"Ongkir: Rp {biaya_ongkir:,}")
        if st.session_state.voucher_aktif:
            st.markdown(f"Diskon Promo: -Rp {diskon:,}")
        st.markdown(f"### TOTAL: Rp {total_akhir:,}")
        
        # Metode Pembayaran
        metode_bayar = st.selectbox("Metode Pembayaran:", [
            "Virtual Account (BCA / Mandiri)",
            "E-Wallet (GoPay / Dana / OVO)",
            "QRIS Instant",
            "Cash on Delivery (COD)"
        ])
        
        if st.button("SELESAIKAN PEMESANAN", use_container_width=True):
            poin_baru = int(total_akhir / 10000)
            st.session_state.member_poin += poin_baru
            
            st.success("🔥 PESANAN BERHASIL DIPROSES!")
            st.code(f"""
💀 VOID & RUST ORDER RECEIPT 💀
Date      : {datetime.datetime.now().strftime('%d-%b-%Y %H:%M')}
Customer  : {st.session_state.member_nama}
Payment   : {metode_bayar}
----------------------------------------
TOTAL PAID     : Rp {total_akhir:,}
Reward Earned  : +{poin_baru} pts (Total: {st.session_state.member_poin} pts)
----------------------------------------
Package is packing in dark warehouse.
            """)
            st.session_state.keranjang = []
    else:
        st.warning("Tas belanja Anda masih kosong.")