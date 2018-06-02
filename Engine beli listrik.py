# Engine beli listrik
# Dibuat tanggal 1 Juni 2018 17:40
# Ingat hari ini hari kesaktian pancasila

# ============================================
# Persiapan
# ============================================

# Todo import library
import pymysql
import time
import json
import dropbox
import pathlib
import re
import requests
from prettytable import PrettyTable

# Todo menentukan delay dari engine dengan meminta input dari user
delay = int(input("Masukkan waktu delay: "))

# Todo membuat function
# pisahkan masing-masing proses dengan membuat function

# function untuk menambahkan log insert ke file json dari tabel transaksi
# function ini dapat digunakan untuk menambahkan log insert, update, delete ke file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def insertJson(id_transaksi, id_pelanggan, no_token, id_strom, waktu_pembelian, nama_file_json, action, run):
	list_data = []
	# read file json
	with open('File JSON/' + nama_file_json, 'r', encoding='utf-8') as file:
		try:
			data = json.load(file)
		except:
			data = []
	# menambahkan record baru ke variabel temporary
	new_entry = {'id_transaksi': str(id_transaksi), 'id_pelanggan': str(id_pelanggan), 'no_token': no_token, 'id_strom': str(id_strom), 
				 'waktu_pembelian': str(waktu_pembelian), 'action': action, 'run': run}
	# append record baru ke variabel array
	list_data.append(new_entry)
	# menyimpan record baru ke file json
	with open('File JSON/' + nama_file_json, 'w', encoding='utf-8')as file:
		json.dump(data + list_data, file, indent=4)


# function untuk mengunggah file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def uploadJson(local_file, dropbox_file):
	dropbox_access_token = dropbox.Dropbox("EXeeHtUQ-7AAAAAAAAAAWoX2lq8qJhENikI27Ut23hnayr_4d72tl5jhly2B5nwy")
	file_path = pathlib.Path('File JSON/' + local_file)
	with file_path.open('rb') as file:
		dropbox_access_token.files_upload(file.read(), '/' + dropbox_file, mode=dropbox.files.WriteMode("overwrite"))
	print(local_file + "berhasil diunggah")


# function untuk mengunduh file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def downloadJson(target_file, local_file):
	target_file_dropbox = '/' + target_file
	dropb = dropbox.Dropbox("EXeeHtUQ-7AAAAAAAAAAWoX2lq8qJhENikI27Ut23hnayr_4d72tl5jhly2B5nwy")
	link = dropb.sharing_create_shared_link(target_file_dropbox)
	url = link.url
	download_url = re.sub(r"\?dl\=0", "?dl=1", url)
	r = requests.get(download_url)
	with open('File JSON/' + local_file, 'wb') as file:
		file.write(r.content)
	print(local_file + "berhasil diunuduh")

# function untuk insert , update delete pada tabel transaksi 
# function ini dapat digunakan untuk mengubah tabel transaksi dan tabel temporary
#  dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code , cur, db
def cekIUD(transaksi):
	if  transaksi == 'indomaret':
		# Todo membuat koneksi
		con = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_indomaret")
		
		# Todo membuat cursor
		cur = con.cursor()

		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_transaksi Indomaret
		cur.execute("SELECT * FROM tb_transaksi")
		data = cur.fetchall()
		
		# Select data dari tabel tb_transaksi_temp Indomaret
		cur.execute("SELECT * FROM tb_transaksi_temp")
		data_temp = cur.fetchall()
		

		# Todo Menghitung banyak data dari tabel transaksi Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary Indomaret
		jumlah_data_temp = len(data_temp)

	elif  transaksi == 'pln':
		# Todo membuat koneksi
		con = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")

		# Todo membuat cursor
		cur = con.cursor()
		
		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_transaksi PLN
		cur.execute("SELECT * FROM tb_transaksi")
		data = cur.fetchall()
		
		# Select data dari tabel tb_transaksi_temp PLN
		cur.execute("SELECT * FROM tb_transaksi_temp")
		data_temp = cur.fetchall()

		# Todo Menghitung banyak data dari tabel transaksi PLN dan Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary PLN dan Indomaret
		jumlah_data_temp = len(data_temp)

	# Todo cek update dari tabel transaksi PLN
	if jumlah_data == jumlah_data_temp:
		print("Cek update pada tabel transaksi " + transaksi + "..")
		for i in range(0, jumlah_data):
			# Melakukan select concat pada tabel transaksi PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', id_strom, ' ', waktu_pembelian, ' ') AS data_pln FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s"  % i
			cur.execute(sql)
			record = cur.fetchone()

			# Melakukan select concat pada tabel transaksi temp PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', id_strom, ' ', waktu_pembelian, ' ') AS data_pln_temp FROM tb_transaksi_temp WHERE tb_transaksi_temp.id_transaksi = %s"  % i
			cur.execute(sql)
			record_temp = cur.fetchone()

			if record != record_temp:
				# print notifikasi
				print("Terjadi update data pada tb_transaksi " + transaksi + "..")
				t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'waktu_pembelian'])
				t.add_row([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])
				print(t)
				
				sql = "UPDATE tb_transaksi_temp SET tb_transaksi_temp.id_pelanggan = %s, tb_transaksi_temp.no_token = '%s', tb_transaksi_temp.id_strom = %s, tb_transaksi_temp.waktu_pembelian = '%s' WHERE tb_transaksi_temp.id_transaksi = %s" %(
						  data[i][1], data[i][2], data[i][3], data[i][4], data_temp[i][0]
					  )
				cur.execute(sql)
				con.commit()

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'indomaret.json', 'update', '0')
				elif  transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'pln.json', 'update', '0')


	# Todo cek insert dari tabel transaksi PLN
	if jumlah_data > jumlah_data_temp:
		print("Cek insert pada tabel transaksi " + transaksi + "..")
		for i in range(jumlah_data_temp, jumlah_data):
			sql = "INSERT INTO tb_transaksi_temp(id_pelanggan, no_token, id_strom, waktu_pembelian) VALUES(%s, '%s', %s, '%s')" % (
				data[i][1], data[i][2], data[i][3], data[i][4])
			cur.execute(sql)
			con.commit()

			# print notifikasi
			print("Terjadi insert data pada tb_transaksi " + transaksi + "..")
			t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'waktu_pembelian'])
			t.add_row([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4]])
			print(t)

		if transaksi == 'indomaret':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'indomaret.json', 'insert', '0')
		elif  transaksi == 'pln':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'pln.json', 'insert', '0')


	# Todo cek delete dari tabel transaksi PLN
	if jumlah_data < jumlah_data_temp:
		print("Cek delete pada tabel transaksi " + transaksi + "..")
		for i in range(0, jumlah_data_temp):
			cur.execute("SELECT * FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s" % data_temp[i][0])
			record = cur.fetchone()
			if record is None == True:
				# print notifikasi
				print("Terjadi delete data pada tabel transaksi " + transaksi + "..")
				t = PrettyTable(['id_transaksi'])
				t.add_row([data_temp[i][0]])
				print(t)

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'indomaret.json', 'delete', '0')
				if transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], 'pln.json', 'delete', '0')
	
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON PLN atau Indomaret
	# ============================================
	if transaksi == 'indomaret':
        #DownlaodJsonToko()
        # Cek Pembahruan dalam JSON file database bank
        with open('pln.json', 'r', encoding='utf-8') as report:
            try:
                data_json = json.load(report)
            except:
                data_json = []
        jumlah_data_json = len(data_json)
    elif transaksi == 'pln':
        #DownlaodJsonBank()
        # Cek Pembahruan dalam JSON file database toko
        with open('indomaret.json', 'r', encoding='utf-8') as report:
            try:
                data_json = json.load(report)
            except:
                data_json = []
        jumlah_data_json = len(data_json)
	
	if (data_json is None) == False:
        for i in range(jumlah_data_json):
            # memasukkan status action dan status perintah apakah belum atau sudah dijalankan
            action = data_json[i]['action']
            run = data_json[i]['run']

            # memasukkan nilai pada json ke variabel
            id_json = int(data_json[i]['id'])
            no_rek_json = data_json[i]['no_rek']
            atas_nama_json = data_json[i]['atas_nama']
            jumlah_json = int(data_json[i]['jumlah'])
            kode_unik_json = data_json[i]['kode_unik']
            status_json = data_json[i]['status']
            tanggal_json = data_json[i]['tanggal']

            # Todo cek update dari tabel transaksi PLN atau Indomaret
            if action == 'update' and run == '0':
                for a in range(jumlah_data_temp):
                    if id_json == data_temp[a][0]:
						
    
	


	# Todo cek insert dari tabel transaksi PLN atau Indomaret


	# Todo cek delete dari tabel transaksi PLN atau Indomaret


	con.close()
# function main
def main():
	
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi PLN
	# ============================================
	cekIUD('pln')	
	time.sleep(delay)
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi Indomaret
	# ============================================
	cekIUD('indomaret')
	time.sleep(delay)

	
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON Indomaret
	# ============================================

	# Todo cek update dari tabel transaksi PLN


	# Todo cek insert dari tabel transaksi PLN


	# Todo cek delete dari tabel transaksi PLN


# Todo melakukan infinity loop
while True:
	# Todo memanggil fungsi main
	main()