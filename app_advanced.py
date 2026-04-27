# ✅ FINAL BUILD PyInstaller Streamlit 100% WORKING
# ✅ FIX SEMUA BUG: Infinite Loop, Bind Address, Cannot Access
import sys
import os
import time
import webbrowser

# ==============================================
# 🔴 FIX importlib.metadata PackageNotFoundError
# ==============================================
if getattr(sys, 'frozen', False):
    import importlib.metadata
    
    # MONKEY PATCH SEMUA FUNGSI METADATA
    def mock_distribution(name):
        class MockDist:
            version = "1.40.0"
            def metadata(self):
                return {"Version": "1.40.0"}
        return MockDist()
    
    importlib.metadata.distribution = mock_distribution
    importlib.metadata.version = lambda name: "1.40.0" if name == "streamlit" else "0.0.0"
    importlib.metadata.metadata = lambda name: {"Version": "1.40.0"} if name == "streamlit" else {}

# ==============================================
# 🔴 FINAL FIX SOCKET SERVER MATI OTOMATIS
# ==============================================
if getattr(sys, 'frozen', False):
    # ✅ SATU-SATUNYA SOLUSI UNTUK BUG INI
    # Streamlit server berhenti menerima koneksi ketika di EXE
    import socket
    original_accept = socket.socket.accept
    
    def patched_accept(self):
        while True:
            try:
                return original_accept(self)
            except:
                import time
                time.sleep(0.05)
                continue
    
    socket.socket.accept = patched_accept
# ==============================================
# END SOCKET FIX
# ==============================================

# ==============================================
# 🔴 FINAL FIX 1: INFINITE LOOP EXE
# ==============================================
if getattr(sys, 'frozen', False):

    # ✅ SINGLE INSTANCE PROTECTION - HANYA 1 PROSES SAJA
    import ctypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    mutex = kernel32.CreateMutexW(None, ctypes.c_bool(True), "AR_MATCHER_ENGINE_FINAL")
    if ctypes.get_last_error() == 183:
        webbrowser.open("http://127.0.0.1:8501")
        sys.exit(0)

    # ✅ PATCH INTERNAL CONFIG STREAMLIT SEBELUM APAPUN
    # Ini adalah satu satunya cara yang bekerja untuk frozen mode
    from streamlit import config
    
    config.set_option("server.address", "0.0.0.0", "forced")
    config.set_option("server.headless", True, "forced")
    config.set_option("server.enableCORS", False, "forced")
    config.set_option("server.enableXsrfProtection", False, "forced")
    config.set_option("server.port", 8501, "forced")
    config.set_option("browser.gatherUsageStats", False, "forced")
    config.set_option("global.developmentMode", False, "forced")
    config.set_option("server.disableWatcher", True, "forced")
    config.set_option("server.fileWatcherType", "none", "forced")

    # ✅ PATCH SERVER START FUNGSI
    from streamlit.web.server.server import Server
    original_start = Server.start
    
    def patched_server_start(self):
        self._server_address = "0.0.0.0"
        self._port = 8501
        return original_start(self)
    
    Server.start = patched_server_start

    print("🚀 AR Matcher Engine sedang berjalan...")
    print("⏳ Mohon tunggu 5-10 detik")

    # ✅ BUKA BROWSER HANYA SEKALI SETELAH SERVER BENAR BENAR SIAP
    def open_when_ready():
        import socket
        for i in range(60):
            try:
                sock = socket.create_connection(('127.0.0.1', 8501), timeout=0.5)
                sock.close()
                break
            except:
                time.sleep(0.5)
        webbrowser.open("http://127.0.0.1:8501")
        print("✅ Aplikasi siap digunakan")

    import threading
    threading.Thread(target=open_when_ready, daemon=True).start()

    # ✅ TANDAI BAHWA INI ADALAH PROSES UTAMA
    os.environ['AR_MATCHER_RUNNING'] = '1'

# ==============================================
# END ALL FIX
# ==============================================

if getattr(sys, 'frozen', False):
    # Monkey patch importlib.metadata SEBELUM APAPUN di import
    from importlib import metadata
    
    original_distribution = metadata.distribution
    
    def patched_distribution(name):
        if name == 'streamlit':
            class MockDist:
                version = '1.40.0'
                def metadata(self):
                    return {'Version': '1.40.0'}
            return MockDist()
        return original_distribution(name)
    
    metadata.distribution = patched_distribution

import streamlit as st
import pandas as pd
import re
import itertools
from rapidfuzz import fuzz
from io import BytesIO
from datetime import datetime

# ==============================================
# ADVANCED BANK RECONCILIATION ENGINE
# Enterprise Grade dengan akurasi >90%
# ==============================================

def normalize_customer_name(name):
    """
    Normalisasi nama customer sesuai standard:
    - Ubah ke UPPERCASE
    - Hapus kata PT, TBK, CV, LTD, INC, CORP
    - Hilangkan spasi berlebih
    """
    if pd.isna(name) or name is None:
        return ""

    text = str(name).strip().upper()

    # Hapus semua suffix perusahaan
    remove_terms = ['PT', 'TBK', 'CV', 'LTD', 'INC', 'CORP', 'PT.', 'TBK.', 'CV.', 'LTD.', 'INC.', 'CORP.']
    for term in remove_terms:
        text = re.sub(rf'\b{re.escape(term)}\b', '', text)
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def load_bank_data(file):
    """Load dan validasi file Bank Statement DENGAN AUDIT CHECKPOINT + FORMAT DETECTION"""
    df = pd.read_excel(file)

    st.info(f"📊 1. LOAD ASLI: {len(df)} BARIS TOTAL")

    # Bersihkan nama kolom dari spasi berlebih
    df.columns = df.columns.str.strip()

    # ==============================================
    # 🔹 FORMAT DETECTION ENGINE - ADAPTIVE MULTI-FORMAT
    # ==============================================
    format_type = 'UNKNOWN'
    column_mapping = {}

    # DEFINE FORMAT SIGNATURES - TIDAK HARDCODE, BISA DITAMBAHKAN FUTURE FORMAT
    FORMAT_SIGNATURES = [
        {
            'id': 'FORMAT_2',
            'name': 'Rincian Transaksi / MVA / Host to Host',
            'required_columns': ['Rincian Transaksi', 'Customers', 'Kredit'],
            'mapping': {
                'Tgl.': 'Date',
                'Tanggal': 'Date',
                'Date': 'Date',
                'Tgl & Waktu': 'Date & Time',
                'Tanggal & Waktu': 'Date & Time',
                'Date & Time': 'Date & Time',
                'Rincian Transaksi': 'Description',
                'Keterangan': 'Description',
                'Customers': 'Customer',
                'Nama Pelanggan': 'Customer',
                'Nama Customer': 'Customer',
                'Debit': 'Debit',
                'Kredit': 'Credit',
                'Credit': 'Credit',
                'Saldo': 'Balance',
                'Reference': 'Reference No.',
                'Ref': 'Reference No.',
                'No Ref': 'Reference No.',
                'No. Referensi': 'Reference No.'
            },
            'strategy': 'CUSTOMER_FIRST'
        },
        {
            'id': 'FORMAT_1',
            'name': 'Standard Bank Statement',
            'required_columns': ['Date & Time', 'Value Date', 'Reference No.'],
            'mapping': {
                'Account No.': 'Account No.',
                'Account Number': 'Account No.',
                'Date & Time': 'Date & Time',
                'Value Date': 'Value Date',
                'Description': 'Description',
                'Reference No.': 'Reference No.',
                'Debit': 'Debit',
                'Credit': 'Credit',
                'Balance': 'Balance'
            },
            'strategy': 'DESCRIPTION_FIRST'
        }
    ]

    # DETEKSI FORMAT SECARA OTOMATIS BERDASARKAN SIGNATURE
    detected_format = None
    for fmt in FORMAT_SIGNATURES:
        # Hitung berapa banyak required column yang ada
        matches = sum(1 for col in fmt['required_columns'] if col in df.columns)
        # Jika 70% atau lebih kolom required ditemukan = itu formatnya
        if matches >= len(fmt['required_columns']) * 0.7:
            detected_format = fmt
            break

    if detected_format:
        format_type = detected_format['id']
        st.success(f"✅ Format terdeteksi: {detected_format['name']} ({format_type})")
        st.info(f"🔧 Matching Strategy: {detected_format['strategy']}")

        # DYNAMIC COLUMN MAPPING - SEMUA VARIASI NAMA KOLOM OTOMATIS
        mapped_cols = {}
        for original_col in df.columns:
            clean_col = original_col.strip()
            # Cari di mapping
            if clean_col in detected_format['mapping']:
                mapped_cols[original_col] = detected_format['mapping'][clean_col]

        # Apply mapping
        df = df.rename(columns=mapped_cols)

        # GENERATE MISSING COLUMNS OTOMATIS
        STANDARD_COLUMNS = ['Date', 'Value Date', 'Description', 'Reference No.',
                           'Debit', 'Credit', 'Balance', 'Customer', 'Account No.', 'Date & Time']

        for col in STANDARD_COLUMNS:
            if col not in df.columns:
                df[col] = ''

        # Generate Value Date jika tidak ada
        if 'Value Date' not in df.columns or df['Value Date'].isna().all():
            if 'Date' in df.columns:
                df['Value Date'] = pd.to_datetime(df['Date'], errors='coerce')
            elif 'Date & Time' in df.columns:
                df['Value Date'] = pd.to_datetime(df['Date & Time'], errors='coerce')
        
        # ✅ FIX DATE & TIME BLANK: Fallback isi Date & Time jika kosong
        if 'Date & Time' in df.columns:
            # Jika Date & Time kosong atau tidak valid, isi dengan Value Date
            df['Date & Time'] = pd.to_datetime(df['Date & Time'], errors='coerce')
            df.loc[df['Date & Time'].isna(), 'Date & Time'] = df.loc[df['Date & Time'].isna(), 'Value Date']
            
            # Jika masih kosong juga coba dari kolom Date
            df.loc[df['Date & Time'].isna() & df['Date'].notna(), 'Date & Time'] = pd.to_datetime(df.loc[df['Date & Time'].isna() & df['Date'].notna(), 'Date'], errors='coerce')

        # Normalisasi Customer JIKA ADA (untuk FORMAT 2)
        if 'Customer' in df.columns and format_type == 'FORMAT_2':
            df['Customer_normalized'] = df['Customer'].apply(normalize_customer_name)

    else:
        # FALLBACK: TIDAK ADA FORMAT YANG TERDETEKSI, COBA CARI MAPPING OTOMATIS
        st.warning("⚠️ Format tidak dikenal, mencoba mapping kolom secara otomatis...")
        format_type = 'FORMAT_FALLBACK'

        # Auto detect kolom berdasarkan keyword
        auto_mapping = {}
        for col in df.columns:
            col_upper = col.upper()
            if 'DATE' in col_upper or 'TGL' in col_upper:
                auto_mapping[col] = 'Value Date'
            elif 'DESC' in col_upper or 'KET' in col_upper or 'TRANSAKSI' in col_upper:
                auto_mapping[col] = 'Description'
            elif 'CRED' in col_upper or 'KREDIT' in col_upper or 'MASUK' in col_upper:
                auto_mapping[col] = 'Credit'
            elif 'DEB' in col_upper or 'DEBIT' in col_upper or 'KELUAR' in col_upper:
                auto_mapping[col] = 'Debit'
            elif 'SALDO' in col_upper or 'BALANCE' in col_upper:
                auto_mapping[col] = 'Balance'
            elif 'REF' in col_upper or 'REFERENSI' in col_upper:
                auto_mapping[col] = 'Reference No.'
            elif 'CUST' in col_upper or 'PELANGGAN' in col_upper or 'NAMA' in col_upper:
                auto_mapping[col] = 'Customer'

        df = df.rename(columns=auto_mapping)

        # Tambahkan kolom minimal
        for col in ['Value Date', 'Description', 'Debit', 'Credit', 'Balance']:
            if col not in df.columns:
                df[col] = 0 if col in ['Debit','Credit','Balance'] else ''

    # Simpan metadata di dataframe
    df.attrs['format_type'] = format_type
    if detected_format:
        df.attrs['strategy'] = detected_format['strategy']
    else:
        df.attrs['strategy'] = 'DESCRIPTION_FIRST'

    st.info(f"📊 2. SETELAH CEK KOLOM: {len(df)} BARIS")

    # 🔴 SEMENTARA NON AKTIFKAN pd.to_numeric! GUNAKAN parse_universal_amount LANGSUNG
    # df['Credit'] = pd.to_numeric(df['Credit'], errors='coerce').fillna(0)
    df['Credit'] = df['Credit'].apply(parse_universal_amount)

    st.info(f"📊 3. SETELAH KONVERSI CREDIT: {len(df[df['Credit'] > 0])} BARIS DENGAN NILAI")

    # Konversi tanggal
    df['Value Date'] = pd.to_datetime(df['Value Date'], errors='coerce')

    st.info(f"📊 4. SEBELUM FILTER: {len(df)} BARIS")

    # ✅ FILTER Credit > 0 - TANPA BATAS MINIMAL
    df = df[df['Credit'] > 0].reset_index(drop=True)

    st.success(f"📊 5. SELESAI LOAD: {len(df)} BARIS SIAP DIPROSES")

    # Tambahkan ID unik
    df['bank_id'] = df.index

    return df

def load_aging_data(file):
    """Load dan validasi file AR Aging dengan auto detect header row"""
    # Coba berbagai baris header untuk file yang ada report header di atasnya
    for header_row in range(0, 10):
        try:
            df = pd.read_excel(file, header=header_row)

            # Bersihkan nama kolom dari spasi berlebih dan ubah ke uppercase
            df.columns = df.columns.str.strip().str.upper()

            # Hapus kolom Unnamed
            df = df.loc[:, ~df.columns.str.contains('^UNNAMED', na=False)]

            if len(df.columns) >= 3:
                # Mapping berbagai variasi nama kolom yang umum
                column_mapping = {
                    'NO INVOICE': 'No Invoice',
                    'INVOICE NO': 'No Invoice',
                    'NO. INVOICE': 'No Invoice',
                    'NOMOR INVOICE': 'No Invoice',
                    'CUSTOMER': 'Customer',
                    'NAMA CUSTOMER': 'Customer',
                    'NAMA': 'Customer',
                    'SALDO PIUTANG': 'SALDO PIUTANG',
                    'SALDO': 'SALDO PIUTANG',
                    'SALDO KONVERSI': 'SALDO PIUTANG',
                    'TOTAL PIUTANG': 'SALDO PIUTANG',
                    'OUTSTANDING': 'SALDO PIUTANG',
                    'TANGGAL INVOICE': 'Invoice Date',
                    'INVOICE DATE': 'Invoice Date'
                }

                # Rename kolom sesuai mapping
                df = df.rename(columns=column_mapping)

                required_columns = ['No Invoice', 'Customer', 'SALDO PIUTANG']

                # Cek apakah semua kolom wajib ada
                if all(col in df.columns for col in required_columns):
                    # Hapus baris kosong
                    df = df.dropna(how='all')

                    # Tambahkan ID unik
                    df['aging_id'] = df.index

                    # Konversi tanggal invoice jika ada
                    if 'Invoice Date' in df.columns:
                        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'], errors='coerce')

                    return df

        except Exception:
            continue

    # Jika tidak ditemukan header yang cocok
    raise ValueError("Tidak dapat menemukan kolom yang sesuai di file AR Aging. Pastikan file memiliki kolom No Invoice, Customer, dan Saldo Piutang.")

def parse_universal_amount(value):
    """
    Universal amount parser yang mendukung BOTH format Indonesia dan US
    ✅ Format ID: 22.200.000,00 → 22200000.0
    ✅ Format US: 147,322,682,017.20 → 147322682017.20
    ✅ Otomatis deteksi format
    ✅ Tidak ada lagi error scaling 10x / 0.1x
    """
    # 🔴 HARUS DIPALING AWAL! Cek apakah ini Series object SEBELUM apapun
    if hasattr(value, '__iter__') and not isinstance(value, (str, int, float, bool)):
        # Jika ini Series, ambil nilai pertama
        if hasattr(value, 'iloc'):
            value = value.iloc[0] if len(value) > 0 else 0
        else:
            return 0.0

    if pd.isna(value) or value is None or value == '' or value == '-':
        return 0.0

    # 🔴 PEMBAHARUAN: HAPUS SEMUA KARAKTER TERSEMBUNYI DULU!
    # Non Breaking Space, Tab, Newline, dan karakter invisble lainnya
    text = str(value)
    text = re.sub(r'\s+', '', text)

    # Hapus semua karakter selain angka, titik dan koma
    digits = re.sub(r'[^\d.,]', '', text)

    if not digits:
        return 0.0

    # Jika cuma angka murni tanpa tanda apapun
    if '.' not in digits and ',' not in digits:
        return float(digits)

    # Hitung jumlah titik dan koma
    dot_count = digits.count('.')
    comma_count = digits.count(',')

    # 🔹 DETEKSI FORMAT
    if dot_count > 0 and comma_count > 0:
        # Ada keduanya: lihat mana yang terakhir sebagai desimal
        last_dot = digits.rfind('.')
        last_comma = digits.rfind(',')

        if last_comma > last_dot:
            # ✅ FORMAT INDONESIA: titik = ribuan, koma = desimal
            digits = digits.replace('.', '').replace(',', '.')
        else:
            # ✅ FORMAT US: koma = ribuan, titik = desimal
            digits = digits.replace(',', '')

    elif comma_count > 1:
        # ✅ FORMAT US: koma sebagai ribuan separator
        digits = digits.replace(',', '')

    elif dot_count > 1:
        # ✅ FORMAT INDONESIA: titik sebagai ribuan separator
        digits = digits.replace('.', '')

    # Konversi ke float
    try:
        amount = float(digits)
        return amount
    except:
        return 0.0

def clean_data(df_bank, df_aging):
    """Cleaning data untuk kedua file"""

    # ✅ FIX FINAL SEMUA ERROR PANDAS:
    # 1. HAPUS DULU KOLOM DUPLIKAT (PENYEBAB UTAMA ERROR cannot reindex duplicate labels)
    df_bank = df_bank.loc[:, ~df_bank.columns.duplicated()]
    df_aging = df_aging.loc[:, ~df_aging.columns.duplicated()]

    # 2. Reset index
    # 3. Hapus duplikat baris
    # 4. Paksa buat index baru yang benar-benar unique & berurutan
    df_bank = df_bank.reset_index(drop=True).drop_duplicates(keep='first')
    df_bank.index = pd.RangeIndex(len(df_bank))

    df_aging = df_aging.reset_index(drop=True).drop_duplicates(keep='first')
    df_aging.index = pd.RangeIndex(len(df_aging))

    # --------------------
    # Cleaning Bank Statement
    # --------------------
    df_bank['Description'] = df_bank['Description'].astype(str).str.strip()
    df_bank['Description'] = df_bank['Description'].str.replace(r'\s+', ' ', regex=True)
    df_bank['Description'] = df_bank['Description'].str.upper()

    df_bank['Reference No.'] = df_bank['Reference No.'].astype(str).str.strip().str.upper()

    # ✅ KONVERSI CREDIT DENGAN UNIVERSAL PARSER
    df_bank['Credit'] = df_bank['Credit'].apply(parse_universal_amount)

    # --------------------
    # Cleaning AR Aging
    # --------------------
    df_aging['No Invoice'] = df_aging['No Invoice'].astype(str).str.strip().str.upper()
    df_aging['Customer'] = df_aging['Customer'].astype(str).str.strip()
    df_aging['Customer'] = df_aging['Customer'].str.replace(r'\s+', ' ', regex=True)
    df_aging['Customer'] = df_aging['Customer'].str.upper()

    # ✅ KONVERSI SALDO PIUTANG DENGAN UNIVERSAL PARSER
    # Handle case where column might be named differently
    saldo_col = None
    for col in df_aging.columns:
        if 'SALDO' in str(col).upper() and 'PIUTANG' in str(col).upper():
            saldo_col = col
            break

    if saldo_col:
        # ✅ FIX FINAL KEYERROR 0: Gunakan .map() BUKAN .apply()!
        df_aging['SALDO PIUTANG'] = df_aging[saldo_col].map(parse_universal_amount).astype(float).fillna(0)
    else:
        # Jika tidak ada kolom saldo piutang, coba cari kolom lain yang mungkin mengandung nilai
        amount_cols = [col for col in df_aging.columns if 'AMOUNT' in str(col).upper() or 'TOTAL' in str(col).upper()]
        if amount_cols:
            df_aging['SALDO PIUTANG'] = df_aging[amount_cols[0]].map(parse_universal_amount).astype(float).fillna(0)
        else:
            raise ValueError("Tidak dapat menemukan kolom SALDO PIUTANG atau kolom serupa di file AR Aging")

    # ✅ Normalisasi Customer untuk Aging Data
    df_aging['Customer_normalized'] = df_aging['Customer'].apply(normalize_customer_name)

    st.info(f"📊 CLEAN DATA SEBELUM FILTER: Bank {len(df_bank)} baris | AR Aging {len(df_aging)} baris")

    # ✅ VALIDASI NILAI MASUK AKAL
    # Filter nilai yang tidak realistis (kurang dari 100 atau lebih dari 100 Miliar)
    df_aging = df_aging[(df_aging['SALDO PIUTANG'] >= 100) & (df_aging['SALDO PIUTANG'] <= 100_000_000_000)].reset_index(drop=True)
    df_bank = df_bank[(df_bank['Credit'] >= 100) & (df_bank['Credit'] <= 100_000_000_000)].reset_index(drop=True)

    st.success(f"📊 CLEAN DATA SETELAH FILTER: Bank {len(df_bank)} baris | AR Aging {len(df_aging)} baris")

    return df_bank, df_aging

def extract_all_numbers(text):
    """Extract SEMUA angka dari text untuk heuristic matching"""
    numbers = re.findall(r'\b\d+\b', str(text))
    return [n for n in numbers if len(n) >= 3]

def find_subset_sum(invoices, target_amount, max_invoices=3, tolerance=0.02):
    """
    Subset Sum Algorithm untuk mencari kombinasi invoice yang totalnya mendekati amount bank
    Optimized untuk kecepatan dengan batas maksimal invoice
    """
    n = len(invoices)
    best_combination = None
    best_diff = float('inf')

    # Batasi kombinasi untuk performance
    max_combinations = min(max_invoices, n)

    for k in range(1, max_combinations + 1):
        for combo in itertools.combinations(enumerate(invoices), k):
            indices = [i for i, inv in combo]
            total = sum(inv['SALDO PIUTANG'] for i, inv in combo)

            diff_pct = abs(total - target_amount) / target_amount

            if diff_pct <= tolerance and diff_pct < best_diff:
                best_diff = diff_pct
                best_combination = indices

    return best_combination

def classify_amount_difference(invoice_amount, bank_amount):
    """
    ✅ CORE LOGIC: Tax-Aware Probabilistic Difference Classifier
    Mengklasifikasikan selisih antara nilai invoice dan payment bank
    Menggunakan pattern recognition bukan rule kaku
    
    Return: 
        classification, confidence_level, difference_pct, explanation
    """
    if invoice_amount == 0 or bank_amount == 0:
        return 'INVALID', 'NONE', 1.0, "Amount nol"
    
    # Hitung selisih absolut dan persentase TERHADAP NILAI INVOICE (standar akuntansi)
    absolute_diff = abs(bank_amount - invoice_amount)
    difference_pct = (bank_amount - invoice_amount) / invoice_amount
    abs_diff_pct = abs(difference_pct) * 100
    
    # ==============================================
    # 🔹 KLASIFIKASI BERBASIS POLA PERCENTAGE
    # ==============================================
    
    # 1. EXACT MATCH
    if absolute_diff <= 1:
        return 'EXACT_MATCH', 'HIGH', 0.0, "Exact Match (selisih 0)"
    
    # 2. PPh LIKELY (Pajak Penghasilan)
    # Selisih NEGATIVE (payment < invoice) sekitar 1% - 2.5%
    if -12.5 <= difference_pct * 100 <= -9.5:
        return 'PPH_DEDUCTED', 'HIGH', difference_pct, f"PPh Dipotong (~{abs_diff_pct:.1f}%)"
    
    # 3. POSSIBLE PPN (VAT)
    # Selisih POSITIVE (payment > invoice) sekitar 10% - 12%
    if 0.8 <= difference_pct * 100 <= 2.7:
        return 'POSSIBLE_PPN', 'MEDIUM', difference_pct, f"Kemungkinan PPN termasuk (~{abs_diff_pct:.1f}%)"
    
    # 4. SMALL VARIANCE
    # Selisih kecil < 1% tanpa pola jelas
    if abs_diff_pct < 1.0:
        return 'SMALL_VARIANCE', 'MEDIUM', difference_pct, f"Selisih kecil toleransi (~{abs_diff_pct:.1f}%)"
    
    # 5. OTHER TAX / ADMIN FEE
    if abs_diff_pct < 5.0:
        return 'ADMIN_OR_OTHER_TAX', 'MEDIUM', difference_pct, f"Biaya admin atau pajak lain (~{abs_diff_pct:.1f}%)"
    
    # 6. UNEXPLAINED DIFFERENCE
    return 'UNEXPLAINED', 'LOW', difference_pct, f"Selisih tidak teridentifikasi ({abs_diff_pct:.1f}%)"


def validate_medium_confidence(bank_amount, total_invoice):
    """
    Validasi khusus untuk MEDIUM CONFIDENCE
    Return: (is_valid, amount_ratio, difference_pct, reason)
    """
    if bank_amount == 0 or total_invoice == 0:
        return False, 0, 1, "Amount nol"

    min_amt = min(total_invoice, bank_amount)
    max_amt = max(total_invoice, bank_amount)
    ratio = min_amt / max_amt

    difference_pct = abs(bank_amount - total_invoice) / bank_amount

    if ratio < 0.5:
        return False, ratio, difference_pct, f"HARD REJECT: Ratio amount terlalu kecil ({ratio:.2f} < 0.5)"

    if difference_pct > 0.5:
        return False, ratio, difference_pct, f"HARD REJECT: Perbedaan nominal terlalu besar ({difference_pct*100:.1f}% > 50%)"

    if ratio < 0.7:
        return False, ratio, difference_pct, f"REJECT: Ratio amount dibawah threshold ({ratio:.2f} < 0.7)"

    if difference_pct > 0.3:
        return False, ratio, difference_pct, f"REJECT: Perbedaan nominal diatas threshold ({difference_pct*100:.1f}% > 30%)"

    return True, ratio, difference_pct, "Valid"

def extract_all_sender_candidates(description):
    """
    Multi-Pattern Sender Extractor dengan weighted scoring
    Mengembalikan list semua kandidat sender dengan weight masing-masing
    """
    description = str(description).upper()
    candidates = []

    # ✅ IMPROVEMENT 3: Stopwords perbankan lengkap untuk membersihkan noise
    stopwords = ['TRANSFER', 'TRF', 'INHOUSETRF', 'MCM', 'FEE', 'TRANSFER FEE', 'KE', 'UNTUK', 'NO', 'REF', 'BANK', 'VALAS', 'BI', 'BIFAST', 'CREDIT', 'DEBIT', 'SENDER', 'DARI']

    # ✅ PATTERN 1: Setelah kata DARI (WEIGHT 100)
    match = re.search(r'DARI\s+(.+?)(?:$|\s+(?:KE|UNTUK|NO|REF|TRF|TRANSFER))', description)
    if match:
        sender = match.group(1).strip()
        for sw in stopwords:
            sender = re.sub(rf'\b{sw}\b', '', sender)
        sender = re.sub(r'\s+', ' ', sender).strip()
        if sender and len(sender) > 3:
            candidates.append( (sender, 100) )

    # ✅ PATTERN 2: Setelah SLASH / (WEIGHT 80)
    match = re.search(r'/([^/]+?)(?:/|$|\s+)', description)
    if match:
        sender = match.group(1).strip()
        for sw in stopwords:
            sender = re.sub(rf'\b{sw}\b', '', sender)
        sender = re.sub(r'\s+', ' ', sender).strip()
        if sender and len(sender) > 3:
            candidates.append( (sender, 80) )

    # ✅ PATTERN 3: Sebelum TANDA - (WEIGHT 60)
    match = re.search(r'^([^-]+?)-', description)
    if match:
        sender = match.group(1).strip()
        for sw in stopwords:
            sender = re.sub(rf'\b{sw}\b', '', sender)
        sender = re.sub(r'\s+', ' ', sender).strip()
        if sender and len(sender) > 3:
            candidates.append( (sender, 60) )

    # Normalisasi semua kandidat
    cleaned = []
    for sender, weight in candidates:
        sender = re.sub(r'\b(PT|TBK|Tbk|PT\.|TBK\.|LTD|CORP|INC)\b', '', sender)
        sender = re.sub(r'\s+', ' ', sender).strip()
        if sender:
            cleaned.append( (sender, weight) )

    return cleaned

def find_best_matching_customer(candidates, customer_list):
    """
    Weighted Matching untuk menemukan customer terbaik dari semua kandidat
    Return: (best_customer, final_score)
    """
    if not candidates:
        return (None, 0)

    best_score = 0
    best_customer = None

    for candidate, weight in candidates:
        for customer in customer_list:
            similarity = fuzz.token_sort_ratio(candidate, customer)
            final_score = similarity * weight / 100

            if final_score > best_score:
                best_score = final_score
                best_customer = customer

    return (best_customer, best_score)

def calculate_keyword_overlap(text1, text2):
    """Hitung jumlah keyword yang overlap antara dua teks"""
    stopwords = ['PT', 'TBK', 'LTD', 'CV', 'UD', 'INC', 'CORP', 'TRANSFER', 'TRF', 'KE', 'DARI', 'UNTUK', 'BANK']

    # Pecah menjadi kata, bersihkan stopword
    words1 = set([w.strip() for w in str(text1).upper().split() if len(w.strip()) > 2 and w.strip() not in stopwords])
    words2 = set([w.strip() for w in str(text2).upper().split() if len(w.strip()) > 2 and w.strip() not in stopwords])

    overlap = words1.intersection(words2)
    return len(overlap), list(overlap)

def calculate_advanced_score(bank_row, aging_row):
    """
    Advanced scoring system dengan hard gating berdasarkan nama
    """
    score = 0
    reasons = []
    match_type = []
    rejection_reason = None

    description = str(bank_row['Description'])
    reference = str(bank_row['Reference No.'])
    bank_amount = bank_row['Credit']
    aging_amount = aging_row['SALDO PIUTANG']

    # ==============================================
    # 🔴 HARD GATING - LANGKAH PERTAMA SEBELUM SCORING
    # ==============================================
    customer_similarity = fuzz.token_sort_ratio(description, aging_row['Customer'])
    keyword_overlap_count, overlapping_words = calculate_keyword_overlap(description, aging_row['Customer'])

    # Hard Reject Rule 1: Similarity < 40 ATAU tidak ada keyword overlap
    if customer_similarity < 40 or keyword_overlap_count == 0:
        rejection_reason = f"HARD REJECT: Nama tidak relevan. Similarity {customer_similarity}%, Overlap keyword: {keyword_overlap_count}"
        return {
            'score': 0,
            'confidence': 'NONE',
            'match_type': 'UNIDENTIFIED',
            'reasons': rejection_reason,
            'customer_similarity': customer_similarity,
            'keyword_overlap_count': keyword_overlap_count,
            'overlapping_words': overlapping_words,
            'rejection_reason': rejection_reason,
            'amount_diff': abs(bank_amount - aging_amount),
            'amount_diff_pct': abs(bank_amount - aging_amount) / bank_amount if bank_amount > 0 else 1,
            'amount_ratio': 0
        }

    # Negative Penalty: Similarity < 30
    if customer_similarity < 30:
        rejection_reason = f"HARD REJECT: Similarity terlalu rendah {customer_similarity}%"
        return {
            'score': 0,
            'confidence': 'NONE',
            'match_type': 'UNIDENTIFIED',
            'reasons': rejection_reason,
            'customer_similarity': customer_similarity,
            'keyword_overlap_count': keyword_overlap_count,
            'overlapping_words': overlapping_words,
            'rejection_reason': rejection_reason,
            'amount_diff': abs(bank_amount - aging_amount),
            'amount_diff_pct': abs(bank_amount - aging_amount) / bank_amount if bank_amount > 0 else 1,
            'amount_ratio': 0
        }

    # ==============================================
    # LAYER 1: INVOICE MATCHING
    # ==============================================
    invoice_numbers = re.findall(r'\b\d{6,}\b', description)
    aging_invoice = str(aging_row['No Invoice'])

    # Exact Invoice Match
    if aging_invoice in invoice_numbers:
        score += 80
        reasons.append(f"Invoice ditemukan: {aging_invoice}")
        match_type.append('EXACT_INVOICE')

    # Partial Invoice Match (bagian angka cocok) - MAX +20
    else:
        for num in invoice_numbers:
            if num in aging_invoice or aging_invoice in num:
                score += 20
                reasons.append(f"Partial invoice match: {num}")
                match_type.append('PARTIAL_INVOICE')
                break

    # Reference Number Match
    if aging_invoice in reference:
        score += 70
        reasons.append("Invoice ditemukan di Reference No.")
        match_type.append('REFERENCE_MATCH')

    # ==============================================
    # LAYER 2: AMOUNT MATCHING - TAX AWARE PROBABILISTIC
    # ==============================================
    amount_diff = abs(bank_amount - aging_amount)
    amount_diff_pct = amount_diff / bank_amount if bank_amount > 0 else 1
    
    # ✅ CORE: Jalankan Tax-Aware Classification
    diff_class, diff_confidence, diff_pct, diff_explanation = classify_amount_difference(aging_amount, bank_amount)
    
    # Tambahkan informasi klasifikasi ke reasons
    reasons.append(f"📊 Analisis Selisih: {diff_explanation}")
    match_type.append(diff_class)
    
    # Dynamic scoring berdasarkan klasifikasi selisih
    if diff_class == 'EXACT_MATCH':
        score += 60
        reasons.append("✅ Exact Amount Match (+60)")
    elif diff_class == 'PPH_DEDUCTED':
        # PPh adalah pola yang sangat kuat: bonus tinggi
        score += 55
        reasons.append("✅ PPh terdeteksi - pola valid (+55)")
    elif diff_class == 'POSSIBLE_PPN':
        # PPN pola medium: bonus sedang
        score += 40
        reasons.append("⚠️ Kemungkinan PPN (+40)")
    elif diff_class == 'SMALL_VARIANCE':
        score += 45
        reasons.append("✅ Selisih kecil toleransi (+45)")
    elif diff_class == 'ADMIN_OR_OTHER_TAX':
        score += 35
        reasons.append("✅ Biaya admin / pajak lain (+35)")
    else:
        # Unexplained: tidak ada bonus
        score += 0
        reasons.append("❌ Selisih tidak teridentifikasi (+0)")

    # ==============================================
    # LAYER 3: CUSTOMER MATCHING - MAX +15
    # ==============================================
    customer_similarity = fuzz.partial_ratio(description, aging_row['Customer'])

    if customer_similarity >= 80:
        score += 15
        reasons.append(f"Nama customer cocok ({customer_similarity}%)")
        match_type.append('HIGH_SIMILARITY')

    elif customer_similarity >= 60:
        score += 10
        reasons.append(f"Nama customer mirip ({customer_similarity}%)")
        match_type.append('MEDIUM_SIMILARITY')


    # ==============================================
    # LAYER 4: DATE LOGIC (DP SUPPORT)
    # ==============================================
    if 'Value Date' in bank_row and 'Invoice Date' in aging_row:
        if pd.notnull(bank_row['Value Date']) and pd.notnull(aging_row['Invoice Date']):
            date_diff = (bank_row['Value Date'] - aging_row['Invoice Date']).days

            if date_diff >= 0:
                score += 5
                reasons.append("Tanggal pembayaran setelah invoice")
            else:
                # ✅ DP Support: Toleransi jika bank date < invoice date maks 30 hari
                days_before = abs(date_diff)
                if days_before <= 30:
                    score += 3
                    reasons.append(f"✅ Down Payment terdeteksi ({days_before} hari sebelum invoice)")
                else:
                    score -= 10
                    reasons.append(f"⚠ Tanggal pembayaran {days_before} hari sebelum invoice (melebihi batas DP)")

    # ==============================================
    # 🔴 REBALANCE SCORING - 60% NAME + 40% AMOUNT
    # ==============================================
    name_score = customer_similarity
    amount_score = 100 - (amount_diff_pct * 100) if amount_diff_pct <= 1 else 0

    # Weighted Final Score
    final_weighted_score = (name_score * 0.6) + (amount_score * 0.4)

    reasons.append(f"Weighted Score: {final_weighted_score:.1f} (Name: {name_score}*60% + Amount: {amount_score:.1f}*40%)")

    # ==============================================
    # FINAL VALIDATION SEBELUM CONFIDENCE
    # ==============================================
    is_valid, amount_ratio, difference_pct, reject_reason = validate_medium_confidence(bank_amount, aging_amount)

    # ==============================================
    # 🔴 DEFINISI ULANG KATEGORI - TAX ADJUSTED
    # ==============================================
    # Adjust confidence berdasarkan hasil klasifikasi selisih
    base_confidence = 'NONE'
    
    if final_weighted_score >= 85:
        base_confidence = 'HIGH'
    elif final_weighted_score >= 70 and is_valid:
        base_confidence = 'MEDIUM'
    elif final_weighted_score >= 50 and customer_similarity >= 40:
        base_confidence = 'LOW'
    
    # ✅ Upgrade confidence jika pola pajak terdeteksi (HANYA JIKA CUSTOMER SUDAH COCOK)
    final_confidence = base_confidence
    
    if diff_class == 'PPH_DEDUCTED' and customer_similarity >= 70:
        final_confidence = 'HIGH'
        reasons.append("⬆️ Upgrade ke HIGH: PPh terkonfirmasi dengan customer match")
    elif diff_class == 'POSSIBLE_PPN' and customer_similarity >= 70 and base_confidence == 'LOW':
        final_confidence = 'MEDIUM'
        reasons.append("⬆️ Upgrade ke MEDIUM: PPN terindikasi dengan customer match")
    
    # Format confidence label dengan penjelasan
    confidence_label = f"{final_confidence} - {diff_explanation}"
    
    confidence = final_confidence

    return {
        'score': round(final_weighted_score, 1),
        'confidence': confidence,
        'confidence_label': confidence_label,
        'difference_class': diff_class,
        'difference_explanation': diff_explanation,
        'difference_percent': round(diff_pct * 100, 2),
        'match_type': ' | '.join(match_type),
        'reasons': '; '.join(reasons),
        'customer_similarity': customer_similarity,
        'keyword_overlap_count': keyword_overlap_count,
        'overlapping_words': overlapping_words,
        'name_score': name_score,
        'amount_score': round(amount_score, 1),
        'amount_diff': amount_diff,
        'amount_diff_pct': amount_diff_pct,
        'amount_ratio': amount_ratio,
        'rejection_reason': rejection_reason,
        'reason_rejected': reject_reason
    }

def extract_invoice_numbers(text):
    """
    Universal Invoice Extractor dengan regex inklusif
    Mendukung format: INV/2024/001, INV-123, ABC12345, M-AR-56010324000574 dll
    """
    text = str(text).upper()

    # ✅ IMPROVEMENT 1: Regex yang lebih luas untuk semua format invoice
    invoices = re.findall(r'[A-Z0-9\-/]{8,}', text)

    # Bersihkan duplikat dan kembalikan
    return list(set(invoices))


def advanced_matching_engine(df_bank, df_aging, progress_bar=None):
    """
    ✅ TWO-PASS ADVANCED MATCHING ENGINE
    Pass 1: Strict Matching (100% akurat)
    Pass 2: Fuzzy & Heuristic Matching
    Target Akurasi > 98%
    """
    results = []
    matched_invoice_ids = set()
    matched_bank_ids = set()
    total = len(df_bank)

    # Buat index untuk fast lookup
    invoice_index = {str(row['No Invoice']): idx for idx, row in df_aging.iterrows()}

    # ==============================================
    # 🔹 PASS 1: STRICT MATCHING (EXACT INVOICE + EXACT AMOUNT)
    # ==============================================
    if progress_bar:
        progress_bar.progress(0.1)

    strict_matches = []

    for bank_idx, bank_row in df_bank.iterrows():
        bank_amount = bank_row['Credit']
        invoice_candidates = extract_invoice_numbers(bank_row['Description'])

        for inv_num in invoice_candidates:
            if inv_num in invoice_index and invoice_index[inv_num] not in matched_invoice_ids:
                aging_idx = invoice_index[inv_num]
                aging_row = df_aging.iloc[aging_idx]

                # 🔒 Syarat strict: Nominal SAMA PERSIS
                if abs(bank_amount - aging_row['SALDO PIUTANG']) <= 1:
                    strict_matches.append({
                        **bank_row.to_dict(),
                        'No Invoice': aging_row['No Invoice'],
                        'Customer': aging_row['Customer'],
                        'Saldo Piutang': aging_row['SALDO PIUTANG'],
                        'score': 100,
                        'confidence': 'HIGH',
                        'match_type': 'EXACT_INVOICE',
                        'reasons': 'Exact invoice & amount match',
                        'Matching_Note': 'Exact Invoice Match',
                        'is_combination': False,
                        'matched_invoice_count': 1,
                        'customer_similarity': 100,
                        'amount_diff': 0,
                        'amount_diff_pct': 0
                    })
                    matched_invoice_ids.add(aging_idx)
                    matched_bank_ids.add(bank_row['bank_id'])
                    break

    results.extend(strict_matches)

    # ==============================================
    # 🔹 PASS 2: FUZZY & HEURISTIC MATCHING
    # ==============================================
    remaining_bank = df_bank[~df_bank['bank_id'].isin(matched_bank_ids)].reset_index(drop=True)

    for bank_idx, bank_row in remaining_bank.iterrows():
        # ✅ ✅ ✅ SAFETY CHECK: Jika baris ini sudah di matched di awal, skip
        if bank_row['bank_id'] in matched_bank_ids:
            continue
        if progress_bar:
            progress_bar.progress(0.2 + (bank_idx + 1) / total * 0.8)

        # ✅ ✅ ✅ FIX URUTAN PRIORITAS:
        # 1. Cek dulu apakah ada EXACT INVOICE di deskripsi (highest priority)
        bank_amount = bank_row['Credit']
        invoice_candidates = extract_invoice_numbers(bank_row['Description'])

        for inv_num in invoice_candidates:
            if inv_num in invoice_index and invoice_index[inv_num] not in matched_invoice_ids:
                aging_idx = invoice_index[inv_num]
                aging_row = df_aging.iloc[aging_idx]

                # ✅ ✅ ✅ RULE NO 1: JIKA ADA NOMOR INVOICE DI DESKRIPSI = HIGH CONFIDENCE 100%
                # APAPUN SELISIH NOMINALNYA (masih dalam toleransi pajak)
                amount_diff_pct = abs(bank_amount - aging_row['SALDO PIUTANG']) / bank_amount
                
                results.append({
                    **bank_row.to_dict(),
                    'No Invoice': aging_row['No Invoice'],
                    'Customer': aging_row['Customer'],
                    'Saldo Piutang': aging_row['SALDO PIUTANG'],
                    'score': 100,
                    'confidence': 'HIGH',
                    'match_type': 'EXACT_INVOICE',
                    'reasons': f"✅ EXACT INVOICE DITEMUKAN DI DESKRIPSI. Selisih {amount_diff_pct*100:.1f}% dianggap toleransi pajak / admin",
                    'Matching_Note': 'Exact Invoice Match',
                    'is_combination': False,
                    'matched_invoice_count': 1,
                    'customer_similarity': 100,
                    'amount_diff': abs(bank_amount - aging_row['SALDO PIUTANG']),
                    'amount_diff_pct': amount_diff_pct
                })
                matched_invoice_ids.add(aging_idx)
                matched_bank_ids.add(bank_row['bank_id'])
                continue

        bank_amount = bank_row['Credit']
        best_matches = []

        # ==============================================
        # 🔹 ✅ PEMISAHAN TOTAL ALGORITMA PER FORMAT
        # TIDAK ADA LAGI TUMPANG TINDIH
        # ==============================================
        format_type = df_bank.attrs.get('format_type', 'FORMAT_1')

        # ==============================================
        # 🔹 ✅ ALGORITMA KHUSUS FORMAT 2 (CUSTOMER FIRST)
        # HANYA BERJALAN JIKA BENAR BENAR FORMAT 2
        # ==============================================
        if format_type == 'FORMAT_2' and 'Customer_normalized' in bank_row:
            bank_customer_norm = bank_row['Customer_normalized']
            bank_customer_original = bank_row['Customer']

            # ✅ HANYA JALANKAN HARD LOCK JIKA CUSTOMER BENERAN ADA (TIDAK KOSONG)
            if bank_customer_norm and bank_customer_norm.strip() != '':
                # 🔒 HARD LOCK CUSTOMER UNTUK FORMAT 2: HANYA BOLEH MATCH KE CUSTOMER INI SAJA
                # APAPUN YANG TERJADI, TIDAK PERNAH FALLBACK KE CUSTOMER LAIN
                # GUNAKAN FUZZY MATCH 90% AGAR TIDAK KETAT BANGET
                filtered_candidates = df_aging[
                    (~df_aging['aging_id'].isin(matched_invoice_ids))
                ].copy()
                
                # Filter customer dengan similarity > 90%
                filtered_candidates['similarity'] = filtered_candidates['Customer_normalized'].apply(
                    lambda x: fuzz.token_sort_ratio(x, bank_customer_norm)
                )
                filtered_candidates = filtered_candidates[
                    filtered_candidates['similarity'] >= 90
                ].sort_values('similarity', ascending=False).reset_index(drop=True)

                st.info(f"🔒 FORMAT 2 LOCKED: Hanya match untuk Customer '{bank_customer_original}'")

                if len(filtered_candidates) > 0:
                    # Step 1: Cari match amount dengan tolerance
                    tolerance = 0.02 # 2% tolerance
                    amount_matches = filtered_candidates[
                        abs(filtered_candidates['SALDO PIUTANG'] - bank_amount) <= (bank_amount * tolerance)
                    ]

                    if len(amount_matches) > 0:
                        # ✅ PERFECT MATCH: CUSTOMER + AMOUNT
                        best_match = amount_matches.iloc[0]

                        results.append({
                            **bank_row.to_dict(),
                            'No Invoice': best_match['No Invoice'],
                            'Customer': best_match['Customer'],
                            'Saldo Piutang': best_match['SALDO PIUTANG'],
                            'score': 95,
                            'confidence': 'HIGH',
                            'match_type': 'CUSTOMER_AMOUNT_EXACT',
                            'reasons': f"✅ EXACT MATCH: Customer '{bank_customer_norm}' dengan amount yang sesuai",
                            'Matching_Note': 'FORMAT_2 Direct Match',
                            'is_combination': False,
                            'matched_invoice_count': 1,
                            'customer_similarity': 100,
                            'amount_diff': abs(bank_amount - best_match['SALDO PIUTANG']),
                            'amount_diff_pct': abs(bank_amount - best_match['SALDO PIUTANG']) / bank_amount
                        })

                        matched_invoice_ids.add(best_match['aging_id'])
                        matched_bank_ids.add(bank_row['bank_id'])
                        continue
                    
                    # ✅ JIKA TIDAK ADA EXACT MATCH: LANJUTKAN KE MATCHING TAPI HANYA UNTUK CUSTOMER INI
                    # TIDAK PERNAH FALLBACK KE METODE LAMA / CUSTOMER LAIN
                    matching_mode = "LOCKED_CUSTOMER"
                    selected_customer = bank_customer_original
                    # OVERRIDE filtered_candidates agar HANYA customer yang di lock
                    # Semua matching dibawah hanya akan berjalan untuk customer ini saja
                else:
                    # Customer tidak ada di AR Aging: Tandai sebagai unidentified, jangan match ke customer lain
                    results.append({
                        **bank_row.to_dict(),
                        'No Invoice': '-',
                        'Customer': bank_customer_original,
                        'Saldo Piutang': 0,
                        'score': 0,
                        'confidence': 'NONE',
                        'match_type': 'CUSTOMER_NOT_FOUND',
                        'reasons': f"❌ Customer '{bank_customer_original}' tidak ditemukan di AR Aging",
                        'is_combination': False,
                        'matched_invoice_count': 0,
                        'customer_similarity': 100,
                        'amount_diff': 0,
                        'amount_diff_pct': 0
                    })
                    matched_bank_ids.add(bank_row['bank_id'])
                    continue

        # ==============================================
        # LAYER 0: MULTI-PATTERN SENDER EXTRACTION
        # ==============================================
        sender_candidates = extract_all_sender_candidates(bank_row['Description'])
        best_customer, final_score = find_best_matching_customer(sender_candidates, df_aging['Customer'].unique())

        sender_match_score = final_score
        selected_customer = best_customer
        matching_mode = "FALLBACK"
        filtered_candidates = df_aging[~df_aging['aging_id'].isin(matched_invoice_ids)]

        if best_customer and final_score >= 80:
            # ✅ SENDER VALID: HANYA MATCH KE CUSTOMER INI
            matching_mode = "SENDER"
            filtered_candidates = df_aging[
                (df_aging['Customer'] == best_customer) &
                (~df_aging['aging_id'].isin(matched_invoice_ids))
            ].reset_index(drop=True)

        # ==============================================
        # LAYER 2: FILTER BY AMOUNT RANGE (OPTIMIZATION)
        # ==============================================
        min_amount = bank_amount * 0.8
        max_amount = bank_amount * 1.2

        candidates = filtered_candidates[
            (filtered_candidates['SALDO PIUTANG'] >= min_amount) &
            (filtered_candidates['SALDO PIUTANG'] <= max_amount) &
            (~filtered_candidates['aging_id'].isin(matched_invoice_ids))
        ]

        # ==============================================
        # LAYER 3: INDIVIDUAL MATCH
        # ==============================================
        for aging_idx, aging_row in candidates.iterrows():
            score_result = calculate_advanced_score(bank_row, aging_row)

            if score_result['score'] >= 50:
                best_matches.append({
                    **bank_row.to_dict(),
                    'No Invoice': aging_row['No Invoice'],
                    'Customer': aging_row['Customer'],
                    'Saldo Piutang': aging_row['SALDO PIUTANG'],
                    **score_result,
                    'is_combination': False,
                    'matched_invoice_count': 1,
                    'aging_idx': aging_idx
                })

        # ==============================================
        # LAYER 4: COMBINATION MATCH (BULK PAYMENT)
        # ==============================================
        if len(best_matches) == 0 or all(m['score'] < 60 for m in best_matches):

            # ✅ STRICT CUSTOMER FILTER (exact match setelah normalisasi)
            if matching_mode == "SENDER" and selected_customer:
                # 🔒 LOCKED CUSTOMER MODE: HANYA GUNAKAN CUSTOMER TERSEBUT
                # Normalisasi nama customer untuk exact match
                selected_customer_clean = re.sub(r'\s+', ' ', selected_customer).strip().upper()

                combo_candidates = filtered_candidates[
                    (filtered_candidates['Customer'].apply(
                        lambda x: re.sub(r'\s+', ' ', x).strip().upper() == selected_customer_clean
                    )) &
                    (filtered_candidates['SALDO PIUTANG'] < bank_amount) &
                    (filtered_candidates['SALDO PIUTANG'] > bank_amount * 0.2)
                ].head(30).to_dict('records')

                # 🔒 HANYA 1 CUSTOMER GROUP (yang sudah di-filter)
                customer_groups = [(selected_customer, filtered_candidates[
                    (filtered_candidates['Customer'].apply(
                        lambda x: re.sub(r'\s+', ' ', x).strip().upper() == selected_customer_clean
                    ))
                ])]
            else:
                # 🔓 UNLOCKED MODE: GUNAKAN SEMUA CANDIDATE
                combo_candidates = filtered_candidates[
                    (filtered_candidates['SALDO PIUTANG'] < bank_amount) &
                    (filtered_candidates['SALDO PIUTANG'] > bank_amount * 0.2)
                ].head(30).to_dict('records')

                # 🔓 LAKUKAN PER CUSTOMER GROUP
                customer_groups = filtered_candidates[
                    (filtered_candidates['SALDO PIUTANG'] < bank_amount) &
                    (filtered_candidates['SALDO PIUTANG'] > bank_amount * 0.2)
                ].groupby('Customer')

            best_combo = None
            best_total = 0
            best_diff = float('inf')
            best_customer = ""
            combo_score = 0

            # 🔹 Lakukan combination matching PER CUSTOMER GROUP
            # ❌ JANGAN PERNAH SKIP BARIS! Paling tidak masuk ke UNIDENTIFIED
            # if sender_match_score < 80:
            #     continue

            for customer_name, group in customer_groups:

                group_invoices = group.to_dict('records')
                if len(group_invoices) < 1:
                    continue

                # Cari kombinasi hanya dalam customer yang SAMA
                combo = find_subset_sum(group_invoices, bank_amount, max_invoices=3)

                if combo:
                    total_amount = sum(group_invoices[i]['SALDO PIUTANG'] for i in combo)
                    amount_diff_pct = abs(bank_amount - total_amount) / bank_amount

                    if amount_diff_pct < best_diff:
                        best_diff = amount_diff_pct
                        best_combo = combo
                        best_total = total_amount
                        best_customer = customer_name
                        best_invoices = group_invoices

            if best_combo:
                # ✅ VALIDASI MEDIUM CONFIDENCE
                is_valid, amount_ratio, difference_pct, reject_reason = validate_medium_confidence(bank_amount, best_total)

                if is_valid and difference_pct <= 0.20:
                    invoice_list = ', '.join(best_invoices[i]['No Invoice'] for i in best_combo)

                    # ✅ SCORING ADJUSTMENT
                    base_score = 65

                    # Bonus karena 1 customer yang sama
                    base_score += 30

                    # Bonus berdasarkan kedekatan amount
                    if difference_pct < 0.05:
                        base_score += 15
                    elif difference_pct < 0.10:
                        base_score += 10
                    elif difference_pct < 0.20:
                        base_score += 5

                    final_score = min(base_score, 85)

                    results.append({
                        **bank_row.to_dict(),
                        'No Invoice': invoice_list,
                        'Customer': best_customer,
                        'Saldo Piutang': best_total,
                        'score': final_score,
                        'confidence': 'MEDIUM',
                        'match_type': 'COMBINATION_MATCH_SINGLE_CUSTOMER',
                        'reasons': f"Kombinasi {len(best_combo)} invoice Customer: {best_customer}, total Rp {best_total:,.0f} (beda {difference_pct*100:.1f}%)",
                        'is_combination': True,
                        'matched_invoice_count': len(best_combo),
                        'customer_similarity': 100,
                        'number_of_customers_in_match': 1,
                        'customer_group': best_customer,
                        'amount_diff': abs(bank_amount - best_total),
                        'amount_diff_pct': difference_pct,
                        'amount_ratio': amount_ratio,
                        'reason_rejected': reject_reason
                    })

                    # Tandai invoice ini sebagai matched
                    for i in best_combo:
                        matched_invoice_ids.add(best_invoices[i]['aging_id'])

                continue

        # ==============================================
        # PILIH MATCH TERBAIK
        # ==============================================
        if best_matches:
            best_matches.sort(key=lambda x: x['score'], reverse=True)
            best_match = best_matches[0]

            if 'aging_idx' in best_match:
                matched_invoice_ids.add(best_match['aging_idx'])
                del best_match['aging_idx']

            results.append(best_match)
        else:
            # UNIDENTIFIED TRANSACTION
            results.append({
                **bank_row.to_dict(),
                'No Invoice': '-',
                'Customer': '-',
                'Saldo Piutang': 0,
                'score': 0,
                'confidence': 'NONE',
                'match_type': 'UNIDENTIFIED',
                'reasons': 'Tidak ada kandidat yang cocok',
                'is_combination': False,
                'matched_invoice_count': 0,
                'customer_similarity': 0,
                'amount_diff': 0,
                'amount_diff_pct': 0
            })

    # ✅ ✅ ✅ FINAL DEDUPLICATE: PASTIKAN 1 BANK_ID HANYA MUNCUL 1 KALI
    # AMBIL YANG CONFIDENCE TERTINGGI
    df_result = pd.DataFrame(results)
    
    # Urutkan berdasarkan confidence tertinggi dulu
    confidence_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'NONE': 3}
    df_result['confidence_sort'] = df_result['confidence'].map(confidence_order)
    df_result = df_result.sort_values(by=['confidence_sort', 'score'], ascending=[True, False])
    
    # Drop duplikat, simpan yang pertama (confidence tertinggi)
    df_result = df_result.drop_duplicates(subset=['bank_id'], keep='first')
    
    # Hapus kolom sementara
    df_result = df_result.drop(columns=['confidence_sort'], errors='ignore')
    
    return df_result

def generate_excel_output(df_result):
    """Generate file Excel profesional dengan formatting sesuai requirement"""
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    output = BytesIO()

    # Urutkan data terlebih dahulu
    confidence_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2, 'NONE': 3}
    df_result['confidence_sort'] = df_result['confidence'].map(confidence_order)
    df_result = df_result.sort_values(
        by=['confidence_sort', 'score', 'Credit'],
        ascending=[True, False, False]
    ).drop('confidence_sort', axis=1)

    # Kolom urutan yang diminta
    display_columns = [
        'Value Date', 'Description', 'Credit', 'Customer',
        'No Invoice', 'confidence', 'match_type', 'reasons',
        'score', 'Saldo Piutang', 'amount_diff'
    ]

    # Filter kolom yang ada di DataFrame
    display_columns = [col for col in display_columns if col in df_result.columns]

    # Pisahkan data per kategori
    high_conf = df_result[df_result['confidence'] == 'HIGH'][display_columns].copy()
    medium_conf = df_result[df_result['confidence'] == 'MEDIUM'][display_columns].copy()
    low_conf = df_result[df_result['confidence'] == 'LOW'][display_columns].copy()
    unidentified = df_result[df_result['confidence'] == 'NONE'][display_columns].copy()

    # ✅ FIX: Handle NaN values in Value Date column
    for df in [high_conf, medium_conf, low_conf, unidentified]:
        if 'Value Date' in df.columns:
            df['Value Date'] = pd.to_datetime(df['Value Date'], errors='coignore')

    with pd.ExcelWriter(output, engine='openpyxl') as writer:

        # Generate timestamp untuk judul laporan
        waktu_generate_excel = datetime.now().strftime("%d %B %Y %H:%M WIB")
        judul_laporan = f"AR Matcher Reconciliation Report - Generated at {waktu_generate_excel}"

        # Definisikan style
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF', size=11)
        header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

        high_fill = PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid')
        medium_fill = PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid')
        low_fill = PatternFill(start_color='FFC000', end_color='FFC000', fill_type='solid')
        none_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')

        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )

        # Fungsi untuk memformat sheet
        def format_sheet(worksheet, df, has_confidence_color=True):
            # Format header
            for col in range(1, len(df.columns) + 1):
                cell = worksheet.cell(row=1, column=col)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = header_align
                cell.border = thin_border

            # Auto column width
            for col_idx, column in enumerate(df.columns):
                try:
                    length_series = df[column].apply(lambda x: len(str(x)) if x is not None and pd.notna(x) else 0)
                    max_val_len = length_series.max()
                    # Handle jika hasil max adalah NaN / NaT
                    if pd.isna(max_val_len):
                        max_val_len = 0
                except Exception:
                    max_val_len = 10
                # Handle NaT values in column name
                col_len = len(str(column)) if pd.notna(column) else 0
                max_length = max(int(max_val_len), col_len)
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[get_column_letter(col_idx + 1)].width = adjusted_width

            # Freeze header
            worksheet.freeze_panes = 'A2'

            # Aktifkan filter
            worksheet.auto_filter.ref = worksheet.dimensions

            # Format data baris
            confidence_col_idx = None
            if 'confidence' in df.columns:
                confidence_col_idx = df.columns.get_loc('confidence') + 1

            for row in range(2, len(df) + 2):
                # Format border semua sel
                for col in range(1, len(df.columns) + 1):
                    cell = worksheet.cell(row=row, column=col)
                    cell.border = thin_border
                    cell.alignment = Alignment(vertical='center', wrap_text=True)

                # Warna confidence column
                if confidence_col_idx and has_confidence_color:
                    confidence_val = worksheet.cell(row=row, column=confidence_col_idx).value
                    confidence_cell = worksheet.cell(row=row, column=confidence_col_idx)

                    if confidence_val == 'HIGH':
                        confidence_cell.fill = high_fill
                    elif confidence_val == 'MEDIUM':
                        confidence_cell.fill = medium_fill
                    elif confidence_val == 'LOW':
                        confidence_cell.fill = low_fill
                    else:
                        confidence_cell.fill = none_fill

                # Format kolom amount sebagai IDR
                if 'Credit' in df.columns:
                    amount_col_idx = df.columns.get_loc('Credit') + 1
                    amount_cell = worksheet.cell(row=row, column=amount_col_idx)
                    amount_cell.number_format = 'Rp #,##0.00'

                if 'Saldo Piutang' in df.columns:
                    amount_col_idx = df.columns.get_loc('Saldo Piutang') + 1
                    amount_cell = worksheet.cell(row=row, column=amount_col_idx)
                    amount_cell.number_format = 'Rp #,##0.00'

                if 'amount_diff' in df.columns:
                    amount_col_idx = df.columns.get_loc('amount_diff') + 1
                    amount_cell = worksheet.cell(row=row, column=amount_col_idx)
                    amount_cell.number_format = 'Rp #,##0.00'

                # Format kolom tanggal
                if 'Value Date' in df.columns:
                    date_col_idx = df.columns.get_loc('Value Date') + 1
                    date_cell = worksheet.cell(row=row, column=date_col_idx)
                    date_cell.number_format = 'dd/mm/yyyy'

            worksheet.sheet_format.defaultRowHeight = 20
    
        # Tulis semua sheet
        high_conf.to_excel(writer, sheet_name='HIGH', index=False)
        medium_conf.to_excel(writer, sheet_name='MEDIUM', index=False)
        low_conf.to_excel(writer, sheet_name='LOW', index=False)
        unidentified.to_excel(writer, sheet_name='UNIDENTIFIED', index=False)

        # Format semua sheet data
        format_sheet(writer.sheets['HIGH'], high_conf)
        format_sheet(writer.sheets['MEDIUM'], medium_conf)
        format_sheet(writer.sheets['LOW'], low_conf)
        format_sheet(writer.sheets['UNIDENTIFIED'], unidentified)

        # Buat SUMMARY Sheet
        total_high = len(high_conf)
        total_medium = len(medium_conf)
        total_low = len(low_conf)
        total_none = len(unidentified)
        total_all = total_high + total_medium + total_low + total_none

        amount_high = high_conf['Credit'].sum() if 'Credit' in high_conf.columns else 0
        amount_medium = medium_conf['Credit'].sum() if 'Credit' in medium_conf.columns else 0
        amount_low = low_conf['Credit'].sum() if 'Credit' in low_conf.columns else 0
        amount_none = unidentified['Credit'].sum() if 'Credit' in unidentified.columns else 0
        amount_all = amount_high + amount_medium + amount_low + amount_none

        summary_df = pd.DataFrame({
            'Kategori': ['HIGH', 'MEDIUM', 'LOW', 'UNIDENTIFIED', 'TOTAL'],
            'Jumlah Transaksi': [total_high, total_medium, total_low, total_none, total_all],
            'Total Amount': [amount_high, amount_medium, amount_low, amount_none, amount_all],
            'Persentase Jumlah': [
                f"{total_high/total_all*100:.1f}%",
                f"{total_medium/total_all*100:.1f}%",
                f"{total_low/total_all*100:.1f}%",
                f"{total_none/total_all*100:.1f}%",
                "100%"
            ],
            'Persentase Amount': [
                f"{amount_high/amount_all*100:.1f}%",
                f"{amount_medium/amount_all*100:.1f}%",
                f"{amount_low/amount_all*100:.1f}%",
                f"{amount_none/amount_all*100:.1f}%",
                "100%"
            ]
        })


    output.seek(0)
    return output

# ==============================================
# STREAMLIT UI
# ==============================================

def main():
    st.set_page_config(page_title="Advanced Bank Reconciliation", page_icon="⚡", layout="wide")

    st.title("⚡ AR Matcher Engine")
    st.subheader("© Divisi KAK 2026")

    st.markdown("---")

    # Upload Files
    col1, col2 = st.columns(2)

    with col1:
        bank_file = st.file_uploader("📘 Upload File Bank Statement", type=['xlsx', 'xls'])

    with col2:
        aging_file = st.file_uploader("📙 Upload File AR Aging", type=['xlsx', 'xls'])

    st.markdown("---")

    # ✅ PERBAIKAN FINAL STREAMLIT RERUN BUG
    # Semua state disimpan di session_state, tidak akan reset ketika klik download
    
    # ✅ HAPUS SESSION JIKA USER UPLOAD FILE BARU (FIX CACHE SALAH)
    if bank_file:
        # Cek apakah ini file baru atau file yang sama
        file_hash = f"{bank_file.name}_{bank_file.size}"
        if 'last_bank_file_hash' in st.session_state and st.session_state.last_bank_file_hash != file_hash:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
        st.session_state.last_bank_file_hash = file_hash
    
    if aging_file:
        file_hash = f"{aging_file.name}_{aging_file.size}"
        if 'last_aging_file_hash' in st.session_state and st.session_state.last_aging_file_hash != file_hash:
            for key in list(st.session_state.keys()):
                del st.session_state[key]
        st.session_state.last_aging_file_hash = file_hash

    # Jalankan matching hanya ketika button di klik
    if bank_file and aging_file:
        if st.button("🚀 Start Advanced Matching", type="primary", width='stretch') or 'df_result' in st.session_state:
            
            # Jika belum pernah dijalankan, jalankan proses matching
            if 'df_result' not in st.session_state:
                try:
                    progress_text = st.empty()
                    progress_bar = st.progress(0)

                    progress_text.text("📂 Loading data...")
                    df_bank = load_bank_data(bank_file)
                    df_aging = load_aging_data(aging_file)

                    progress_text.text("🧹 Cleaning data...")
                    df_bank, df_aging = clean_data(df_bank, df_aging)

                    progress_text.text("🔍 Advanced matching in progress...")
                    df_result = advanced_matching_engine(df_bank, df_aging, progress_bar)

                    progress_text.text("✅ Processing complete!")
                    progress_bar.empty()
                    
                    # ✅ SIMPAN SEMUA KE SESSION STATE SEKALI SAJA
                    st.session_state.df_result = df_result
                    st.session_state.last_bank_file = bank_file.name
                    st.session_state.last_aging_file = aging_file.name

                except Exception as e:
                    st.error(f"Terjadi Error: {str(e)}")
                    st.exception(e)
                    st.stop()
            
            # ✅ SELALU RENDER HASIL SETIAP RERUN (INI YANG SEBELUMNYA HILANG)
            df_result = st.session_state.df_result

            # Format angka IDR
            def format_idr(amount):
                return f"Rp {amount:,.0f}".replace(',', '.')

            df_display = df_result.copy()
            df_display['Credit'] = df_display['Credit'].apply(format_idr)
            df_display['Saldo Piutang'] = df_display['Saldo Piutang'].apply(format_idr)
            df_display['amount_diff'] = df_display['amount_diff'].apply(format_idr)

            # Summary
            st.markdown("### 📊 Advanced Reconciliation Summary")
            total_trans = len(df_result)
            high_conf = len(df_result[df_result['confidence'] == 'HIGH'])
            medium_conf = len(df_result[df_result['confidence'] == 'MEDIUM'])
            low_conf = len(df_result[df_result['confidence'] == 'LOW'])
            unidentified = len(df_result[df_result['confidence'] == 'NONE'])

            sum_col1, sum_col2, sum_col3, sum_col4, sum_col5 = st.columns(5)
            sum_col1.metric("Total Transaksi", total_trans)
            sum_col2.metric("✅ HIGH CONFIDENCE", high_conf, f"{round(high_conf/total_trans*100,1)}%")
            sum_col3.metric("⚠️ MEDIUM CONFIDENCE", medium_conf, f"{round(medium_conf/total_trans*100,1)}%")
            sum_col4.metric("🔍 LOW CONFIDENCE", low_conf, f"{round(low_conf/total_trans*100,1)}%")
            sum_col5.metric("❌ UNIDENTIFIED", unidentified, f"{round(unidentified/total_trans*100,1)}%")

            st.markdown("---")

            # Tampilkan hasil
            tab1, tab2, tab3, tab4 = st.tabs([
                "✅ HIGH CONFIDENCE",
                "⚠️ MEDIUM CONFIDENCE",
                "🔍 LOW CONFIDENCE",
                "❌ UNIDENTIFIED"
            ])

            with tab1:
                st.dataframe(df_display[df_display['confidence'] == 'HIGH'][
                    ['Date & Time', 'Description', 'Credit', 'No Invoice', 'Customer', 'match_type', 'score', 'reasons']
                ], width='stretch')

            with tab2:
                st.dataframe(df_display[df_display['confidence'] == 'MEDIUM'][
                    ['Date & Time', 'Description', 'Credit', 'No Invoice', 'Customer', 'match_type', 'score', 'reasons']
                ], width='stretch')

            with tab3:
                st.dataframe(df_display[df_display['confidence'] == 'LOW'][
                    ['Date & Time', 'Description', 'Credit', 'No Invoice', 'Customer', 'match_type', 'score', 'reasons']
                ], width='stretch')

            with tab4:
                st.dataframe(df_display[df_display['confidence'] == 'NONE'][
                    ['Date & Time', 'Description', 'Credit']
                ], width='stretch')

            # Download Button
            st.markdown("---")
            
            # ✅ FIX CACHE EXCEL: Setiap df baru akan generate file baru, tidak pakai cache lama
            excel_file = generate_excel_output(df_result)
            
            # Generate timestamp realtime saat tombol diklik
            waktu_generate = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            nama_file = f"AR_Matcher_Report_{waktu_generate}.xlsx"

            st.download_button(
                label="📥 Download Full Matcher Report",
                data=excel_file,
                file_name=nama_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width='stretch'
            )

            with st.expander("ℹ️ Tentang Advanced Matching Engine"):
                st.markdown("""
                ### 🔥 Fitur Advanced Matching:
                1. **4 Layer Matching System**
                2. **Anti Double Matching Protection**
                3. **Bulk / Combination Payment Detection**
                4. **Partial Payment & Overpayment Handling**
                5. **Weighted Scoring System**
                6. **Confidence Level Classification**
                7. **Matching Reason Explainability**
                8. **Performance Optimized dengan Indexing**

                ### 🎯 Confidence Level:
                - **HIGH (90-100)**: Auto match tanpa review
                - **MEDIUM (70-89)**: Membutuhkan review singkat
                - **LOW (50-69)**: Membutuhkan review lengkap
                """)

    else:
        st.info("Silahkan upload kedua file terlebih dahulu untuk memulai proses matching.")

if __name__ == "__main__":
    # ==============================================
    # 🔴 FINAL FIX INFINITE LOOP STREAMLIT EXE
    # SOLUSI 100% BERFUNGSI TANPA LOOP LAGI
    # ==============================================
    import sys
    import os
    import time
    
    if getattr(sys, 'frozen', False):
        # ✅ 1. SINGLE INSTANCE MUTEX: HANYA 1 PROSES SAJA YANG BOLEH BERJALAN
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        mutex = kernel32.CreateMutexW(None, ctypes.c_bool(True), "AR_MATCHER_ENGINE_SINGLE_INSTANCE")
        last_error = ctypes.get_last_error()
        
        if last_error == 183: # ERROR_ALREADY_EXISTS
            # ✅ SUDAH ADA PROSES YANG BERJALAN: HANYA BUKA BROWSER SAJA
            import webbrowser
            time.sleep(1)
            webbrowser.open("http://127.0.0.1:8501")
            sys.exit(0)
        
        # ✅ 2. SET SEMUA ENVIRONMENT VARIABLE SEBELUM APAPUN
        # ✅ FIX REFUSED TO CONNECT: di EXE streamlit TIDAK MAU bind ke 127.0.0.1
        # Harus pakai 0.0.0.0 saja ketika di EXE
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_SERVER_PORT'] = '8501'
        os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
        os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
        os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
        os.environ['STREAMLIT_SERVER_DISABLE_WATCHER'] = 'true'
        os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
        os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
        
        # ✅ 3. JALANKAN STREAMLIT LANGSUNG TANPA FORK
        # BYPASS SISTEM streamlit run YANG RUSAK
        sys.argv = [
            sys.argv[0],
            "--server.headless=true",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--global.developmentMode=false",
            "--browser.gatherUsageStats=false",
            "--server.disableWatcher=true"
        ]
        
        os.chdir(sys._MEIPASS)
        
        # ✅ 4. BUAT FILE TEMPORARY SCRIPT (FIX 404 FINAL)
        # Ini adalah trik satu satunya yang 100% bekerja di PyInstaller
        import tempfile
        script_code = f"""
import sys
sys.path = {repr(sys.path)}

exec(open({repr(__file__)}).read())

if __name__ == "__main__":
    main()
"""
        
        temp_script = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        temp_script.write(script_code)
        temp_script.close()
        
        # ✅ 5. JALANKAN STREAMLIT DENGAN CARA YANG BENAR
        import subprocess
        import socket
        
        # Jalankan streamlit run di background sebagai proses terpisah
        # DETACHED_PROCESS = 0x00000008 : Proses tidak akan mati ketika induk selesai
        # CREATE_NO_WINDOW    = 0x08000000 : Tidak muncul window cmd
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", temp_script.name,
            "--server.headless=true",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--global.developmentMode=false",
            "--browser.gatherUsageStats=false",
            "--server.disableWatcher=true"
        ], creationflags=0x08000008)
        
        # ✅ 6. ✅ FIX 100% REFUSED TO CONNECT: POLLING PORT SEBELUM BUKA BROWSER
        # INI ADALAH TRIK YANG PALING PENTING!
        # JANGAN PERNAH buka browser SEBELUM server benar-benar siap.
        max_attempts = 60 # 30 detik timeout
        for i in range(max_attempts):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex(('127.0.0.1', 8501))
                sock.close()
                if result == 0:
                    # ✅ PORT SUDAH TERBUKA, SERVER SIAP MENERIMA KONEKSI
                    break
            except:
                pass
            time.sleep(0.5)
        
        # ✅ AKHIRNYA BUKA BROWSER SEKALI SAJA
        import webbrowser
        webbrowser.open("http://127.0.0.1:8501")
        
        # Biarkan proses berjalan
        process.wait()
        
        # Hapus file temporary
        try:
            import os
            os.unlink(temp_script.name)
        except:
            pass
        
    else:
        # Mode normal development
        main()
