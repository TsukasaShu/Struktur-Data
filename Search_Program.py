import pandas as pd
import os

# Konfigurasi
google_sheets_csv_url = 'https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv'
excel_header_row = 0 # Karena dimulai dari baris 1 

# Kolom Dataset
COLUMNS_TO_FETCH = [
    'no', 'nim', 'nama_mahasiswa', 'sumber_database',
    'fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal',
    'judul_paper', 'tahun_terbit', 'nama_penulis',
    'abstrak_langusung_copas_dari_paper',
    'kesimpulan_langusung_copas_dari_paper', 'link_paper'
]

COL_JUDUL = 'judul_paper'
COL_TAHUN = 'tahun_terbit'
COL_PENULIS = 'nama_penulis'

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def muat_data_dari_csv(csv_url, header_row):
    print("Mengambil data dari Google Sheets...")
    df = pd.read_csv(csv_url, header=header_row)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^a-z0-9_]', '', regex=True)
    data = df.to_dict(orient='records')
    print(f"Berhasil mengambil {len(data)} data paper")
    return data

def pencarian_linear(data_list, kata_kunci, kolom):
    hasil = []
    kata_kunci_bersih = str(kata_kunci).strip().lower()
    
    for item in data_list:
        if kolom == COL_TAHUN:
            try:
                nilai_tahun = float(str(item.get(kolom, '')).strip())
                if nilai_tahun == float(kata_kunci_bersih):
                    hasil.append(item)
            except (ValueError, TypeError):
                continue
        else:
            nilai = str(item.get(kolom, '')).strip().lower()
            if kata_kunci_bersih in nilai:
                hasil.append(item)
    
    return hasil

def pencarian_biner(data_terurut, kata_kunci, kolom):
    hasil = []
    kata_kunci_bersih = str(kata_kunci).strip().lower()
    
    if kolom == COL_TAHUN:
        try:
            tahun_cari = float(kata_kunci_bersih)
            for item in data_terurut:
                try:
                    nilai_tahun = float(str(item.get(kolom, '')).strip())
                    if nilai_tahun == tahun_cari:
                        hasil.append(item)
                except (ValueError, TypeError):
                    continue
        except (ValueError, TypeError):
            return []
    else:
        for item in data_terurut:
            nilai = str(item.get(kolom, '')).strip().lower()
            if nilai == kata_kunci_bersih:
                hasil.append(item)
    
    return hasil

def tampilkan_hasil(row, nomor):
    garis = "─" * 80
    
    print(f"\nHasil #{nomor}")
    print(garis)
    print(f"No                                      : {row.get('no', 'N/A')}")
    print(f"Nim                                     : {row.get('nim', 'N/A')}")
    print(f"Nama Mahasiswa                          : {row.get('nama_mahasiswa', 'N/A')}")
    print(f"Sumber Database                         : {row.get('sumber_database', 'N/A')}")
    print(f"Fokus Kata Kunci                        : {row.get('fokus_kata_kunci_pilih_no1_atau_2_atau_3_sesuai_yg_ada_di_soal', 'N/A')}")
    print(f"Judul Paper                             : {row.get('judul_paper', 'N/A')}")
    print(f"Tahun Terbit                            : {row.get('tahun_terbit', 'N/A')}")
    print(f"Nama Penulis                            : {row.get('nama_penulis', 'N/A')}") 
       
    garis_panjang = "─" * 120
    
    print("\nAbstrak:")
    print(garis_panjang)
    print(str(row.get('abstrak_langusung_copas_dari_paper', 'N/A')).strip())
    
    print("\nKesimpulan:")
    print(garis_panjang)
    print(str(row.get('kesimpulan_langusung_copas_dari_paper', 'N/A')).strip())
    
    print("\nLink Paper:")
    print(garis_panjang)
    print(str(row.get('link_paper', 'N/A')).strip())
    print(garis_panjang)

if __name__ == "__main__":
    try:
        while True:
            bersihkan_layar()
            print("\n" + "="*80)
            print("SISTEM PENCARIAN DATA PAPER MAHASISWA".center(80))
            print("="*80 + "\n")
            
            try:
                semua_data = muat_data_dari_csv(google_sheets_csv_url, excel_header_row)
            except Exception as e:
                print(f"Error saat membaca data: {e}")
                input("\nTekan Enter untuk keluar...")
                break

            if not semua_data:
                print("\nTidak ada data yang bisa diproses.")
                input("\nTekan Enter untuk keluar...")
                break
            
            print("\nMENU PENCARIAN")
            print("─" * 40)
            print("1. Judul Paper")
            print("2. Tahun Terbit")
            print("3. Nama Penulis")
            
            pilihan = input("\nMasukkan nomor kolom (q untuk keluar): ").lower()
            if pilihan == 'q':
                break

            kolom_pencarian = {
                '1': COL_JUDUL,
                '2': COL_TAHUN,
                '3': COL_PENULIS
            }.get(pilihan)

            if not kolom_pencarian:
                print("\nPilihan tidak valid!")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            kata_kunci = input(f"\nMasukkan kata kunci untuk '{kolom_pencarian}': ").strip()
            if not kata_kunci:
                print("\nKata kunci tidak boleh kosong!")
                input("\nTekan Enter untuk melanjutkan...")
                continue

            print("\nPILIH METODE PENCARIAN")
            print("1. Pencarian Sekuensial (pencarian substring)")
            print("2. Pencarian Biner (pencocokan tepat)")
            
            metode = input("\nPilih metode (1/2): ")
            
            hasil = []
            if metode == '1':
                hasil = pencarian_linear(semua_data, kata_kunci, kolom_pencarian)
            elif metode == '2':
                data_valid = [item for item in semua_data if str(item.get(kolom_pencarian, '')).strip()]
                if data_valid:
                    def kunci_pengurutan(item):
                        nilai = str(item.get(kolom_pencarian, '')).strip()
                        if kolom_pencarian == COL_TAHUN:
                            try:
                                return float(nilai)
                            except (ValueError, TypeError):
                                return float('-inf')
                        return nilai.lower()
                    
                    data_terurut = sorted(data_valid, key=kunci_pengurutan)
                    hasil = pencarian_biner(data_terurut, kata_kunci, kolom_pencarian)
                else:
                    print("\nTidak ada data valid untuk dicari.")

            print(f"\n{'='*80}")
            print(f"Hasil Pencarian '{kata_kunci}' pada kolom '{kolom_pencarian}'")
            print(f"{'='*80}")

            if hasil:
                print(f"\nDitemukan {len(hasil)} hasil:")
                for i, row in enumerate(hasil, 1):
                    tampilkan_hasil(row, i)
            else:
                print("\nTidak ada hasil yang ditemukan.")

            input("\nTekan Enter untuk melanjutkan...")

        print("\nTerima kasih telah menggunakan program ini!")
        input("\nTekan Enter untuk keluar...")
        
    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")
        input("\nTekan Enter untuk keluar...")
