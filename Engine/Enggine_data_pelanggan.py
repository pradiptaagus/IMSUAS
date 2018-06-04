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

# function untuk menambahkan log insert ke file json dari tabel transaksi
# function ini dapat digunakan untuk menambahkan log insert, update, delete ke file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def insertJson(id_pelanggan, nama_pelanggan, alamat,id_meter, no_meter, waktu_pendaftaran, nama_file_json, action, run):
	list_data = []
	# read file json
	with open('File JSON/data_pelanggan/' + nama_file_json, 'r', encoding='utf-8') as file:
		try:
			data = json.load(file)
		except:
			data = []
	# menambahkan record baru ke variabel temporary
	new_entry = {'id_pelanggan': str(id_pelanggan), 'nama_pelanggan': nama_pelanggan, 'alamat': alamat, 
				 'id_meter': str(id_meter), 'no_meter': str(no_meter), 'waktu_pendaftaran': str(waktu_pendaftaran), 'action': action, 'run': run}
	# append record baru ke variabel array
	list_data.append(new_entry)
	# menyimpan record baru ke file json
	with open('File JSON/data_pelanggan/' + nama_file_json, 'w', encoding='utf-8')as file:
		json.dump(data + list_data, file, indent=4)

# function untuk mengunggah file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def uploadJson(local_file, dropbox_file):
	dropbox_access_token = dropbox.Dropbox("9Em04orxhVAAAAAAAAAAEkWTQhZXnfIGW44R7Yz9i6QSpfRaKxt4lR2hrq6IUtXr")
	file_path = pathlib.Path('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/data_pelanggan/' + local_file)
	with file_path.open('rb') as file:
		dropbox_access_token.files_upload(file.read(), '/' + dropbox_file, mode=dropbox.files.WriteMode("overwrite"))
	print(local_file + "berhasil diunggah")


# function untuk mengunduh file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def downloadJson(target_file, local_file):
	try:
		dbx = dropbox.Dropbox('9Em04orxhVAAAAAAAAAAEkWTQhZXnfIGW44R7Yz9i6QSpfRaKxt4lR2hrq6IUtXr')
		target_file_dropbox = "/" + target_file
		link = dbx.sharing_create_shared_link(target_file_dropbox)
		url = link.url
		dl_url = re.sub(r"\?dl\=1", "?dl=1", url)
		print(dl_url)
		dbx.files_download_to_file('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/data_pelanggan/' + local_file, '/' + target_file)
		print(local_file + " berhasil diunuduh")
	except:
		print(local_file + " tidak berhasil diunuduh")

# function untuk insert , update delete pada tabel transaksi 
# function ini dapat digunakan untuk mengubah tabel transaksi dan tabel temporary
#  dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code , cur, db
def cekIUD(transaksi,con,cur):
	if  transaksi == 'indomaret':
		# Todo membuat koneksi
		con_indomaret = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_indomaret")
		
		# Todo membuat cursor
		cur_indomaret = con.cursor()

		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_pelanggan Indomaret
		cur_indomaret.execute("SELECT * FROM tb_pelanggan")
		data = cur_indomaret.fetchall()
		
		# Select data dari tabel tb_pelanggan_temp Indomaret
		cur_indomaret.execute("SELECT * FROM tb_pelanggan_temp")
		data_temp = cur_indomaret.fetchall()
		

		# Todo Menghitung banyak data dari tabel transaksi Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')
		con_indomaret.close()

	elif  transaksi == 'pln':
		# Todo membuat koneksi
		con_pln = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")

		# Todo membuat cursor
		cur_pln = con_pln.cursor()
		
		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_pelanggan PLN
		cur_pln.execute("SELECT * FROM tb_pelanggan")
		data = cur_pln.fetchall()
		
		# Select data dari tabel tb_pelanggan_temp PLN
		cur_pln.execute("SELECT * FROM tb_pelanggan_temp")
		data_temp = cur_pln.fetchall()

		# Todo Menghitung banyak data dari tabel pelanggan PLN dan Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel pelanggan temporary PLN dan Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('data_pelanggan_pln.json', 'data_pelanggan_pln.json')
		con_pln.close()

	# Todo cek update dari tabel transaksi PLN
	if jumlah_data == jumlah_data_temp:
		print("Cek update pada tabel pelanggan " + transaksi + "..")
		for i in range(0, jumlah_data):
			a = i + 1
			# Melakukan select concat pada tabel pelanggan PLN
			sql = "SELECT CONCAT(id_pelanggan, ' ', nama_pelanggan, ' ', alamat, ' ', id_meter, ' ', no_meter, ' ', waktu_pendaftaran, ' ') AS data_pln FROM tb_pelanggan WHERE tb_pelanggan.id_pelanggan = %s"  % a
			cur.execute(sql)
			record = cur.fetchone()

			# Melakukan select concat pada tabel pelanggan temp PLN
			sql = "SELECT CONCAT(id_pelanggan, ' ', nama_pelanggan, ' ', alamat, ' ', id_meter, ' ', no_meter, ' ', waktu_pendaftaran, ' ') AS data_pln_temp FROM tb_pelanggan_temp WHERE tb_pelanggan_temp.id_pelanggan = %s"  % a
			cur.execute(sql)
			record_temp = cur.fetchone()

			if record != record_temp:
				# print notifikasi
				print("Terjadi update data pada tb_pelanggan " + transaksi + "..")
				t = PrettyTable(['id_pelanggan', 'nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran'])
				t.add_row([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5]])
				print(t)
				
				sql = "UPDATE tb_pelanggan_temp SET tb_pelanggan_temp.nama_pelanggan = '%s', tb_pelanggan_temp.alamat = '%s', tb_pelanggan_temp.id_meter = %s,tb_pelanggan_temp.no_meter='%s', tb_pelanggan_temp.waktu_pendaftaran='%s' WHERE tb_pelanggan_temp.id_pelanggan = %s" %(
						  data[i][1], data[i][2], data[i][3], data[i][4],data[i][5], data_temp[i][0]
					  )
				cur.execute(sql)
				con.commit()

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5], 'data_pelanggan_indomaret.json', 'update', '0')
					uploadJson('data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')
				elif  transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5], 'data_pelanggan_pln.json', 'update', '0')
					uploadJson('data_pelanggan_pln.json', 'data_pelanggan_pln.json')

	# Todo cek insert dari tabel transaksi PLN
	if jumlah_data > jumlah_data_temp:
		print("Cek insert pada tabel pelanggan" + transaksi + "..")
		for i in range(jumlah_data_temp, jumlah_data):
			sql = "INSERT INTO tb_pelanggan_temp( nama_pelanggan, alamat, id_meter, no_meter, waktu_pendaftaran) VALUES('%s', '%s', %s, '%s', '%s')" % (
				data[i][1], data[i][2], data[i][3], data[i][4],data[i][5])
			cur.execute(sql)
			con.commit()

			# print notifikasi
			print("Terjadi insert data pada tb_pelanggan " + transaksi + "..")
			t = PrettyTable(['id_pelanggan', 'nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran'])
			t.add_row([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5]])
			print(t)

		if transaksi == 'indomaret':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5], 'data_pelanggan_indomaret.json', 'insert', '0')
			uploadJson('data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')
		elif  transaksi == 'pln':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5], 'data_pelanggan_pln.json', 'insert', '0')
			uploadJson('data_pelanggan_pln.json', 'data_pelanggan_pln.json')

	# Todo cek delete dari tabel transaksi PLN
	if jumlah_data < jumlah_data_temp:
		print("Cek delete pada tabel pelanggan " + transaksi + "..")
		for i in range(0, jumlah_data_temp):
			cur.execute("SELECT * FROM tb_pelanggan WHERE tb_pelanggan.id_pelanggan = %s" % data_temp[i][0])
			record = cur.fetchone()
			#  is None == True
			if cur.rowcount == 0:
				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_pelanggan_temp WHERE id_pelanggan=%s;" % data_temp[i][0]
				cur.execute(sql)
				con.commit()

				# print notifikasi
				print("Terjadi delete data pada tabel pelanggan " + transaksi + "..")
				t = PrettyTable(['id_pelanggan'])
				t.add_row([data_temp[i][0]])
				print(t)

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], data_temp[i][3], data_temp[i][4], data_temp[i][5], 'data_pelanggan_indomaret.json', 'delete', '0')
					uploadJson('data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')
				if transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], data_temp[i][3], data_temp[i][4],data_temp[i][5], 'data_pelanggan_pln.json', 'delete', '0')
					uploadJson('data_pelanggan_pln.json', 'data_pelanggan_pln.json')

	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON PLN atau Indomaret
	# ============================================
	if transaksi == 'indomaret':
		downloadJson('data_pelanggan_pln.json', 'temp_data_pelanggan_pln.json')
        # Cek Pembahruan dalam JSON file database bank
		with open('File JSON/data_pelanggan/temp_data_pelanggan_pln.json', 'r', encoding='utf-8') as report:
			try:
				data_json = json.load(report)
			except:
				data_json = []
		jumlah_data_json = len(data_json)
		db_perubahan = 'pln'

	elif transaksi == 'pln':
		downloadJson('data_pelanggan_indomaret.json', 'temp_data_pelanggan_indomaret.json')
        # Cek Pembahruan dalam JSON file database toko
		with open('File JSON/data_pelanggan/temp_data_pelanggan_indomaret.json', 'r', encoding='utf-8') as report:
			try:
				data_json = json.load(report)
			except:
				data_json = []
		jumlah_data_json = len(data_json)
		db_perubahan = 'indomaret'
	
	if (data_json is None) == False:
		for i in range(jumlah_data_json):
            # memasukkan status action dan status perintah apakah belum atau sudah dijalankan
			action = data_json[i]['action']
			run = data_json[i]['run']
			id_json = int(data_json[i]['id_pelanggan'])

			# Todo cek update dari tabel transaksi PLN atau Indomaret
			if action == 'update' and run == '0':
				for a in range(jumlah_data_temp):
					if id_json == data_temp[a][0]:
						isi_data_json = data_json[i]['id_pelanggan'] + ' ' + data_json[i]['nama_pelanggan'] + ' ' + data_json[i]['alamat']+ ' ' + data_json[i]['id_meter']+ ' ' + data_json[i]['no_meter'] + ' ' + data_json[i]['waktu_pendaftaran']
						
						sql = "SELECT CONCAT(id_pelanggan, ' ', nama_pelanggan, ' ', alamat, ' ', id_meter, ' ', no_meter, ' ', waktu_pendaftaran, ' ') AS data_pln_temp FROM tb_pelanggan_temp WHERE tb_pelanggan_temp.id_pelanggan = %s"  % data_temp[a][0]
						cur.execute(sql)
						record_temp = cur.fetchone()
						str_record_temp =''.join(record_temp)

						if isi_data_json != str_record_temp:
							# print notifikasi
							t = PrettyTable(['id_pelanggan', 'nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran'])
							t.add_row([data_json[i]['id_pelanggan'],data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran']])
							print(t)

							# update pada tabel transaksi temporary
							sql = "UPDATE tb_pelanggan_temp SET tb_pelanggan_temp.nama_pelanggan = '%s', tb_pelanggan_temp.alamat = '%s', tb_pelanggan_temp.id_meter = %s,tb_pelanggan_temp.no_meter='%s', tb_pelanggan_temp.waktu_pendaftaran='%s' WHERE tb_pelanggan_temp.id_pelanggan = %s" % (
								 data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran'],data_json[i]['id_pelanggan'])
							cur.execute(sql)
							con.commit()

							# update pada tabel transaksi
							sql = "UPDATE tb_pelanggan SET tb_pelanggan.nama_pelanggan = '%s', tb_pelanggan.alamat = '%s', tb_pelanggan.id_meter = %s,tb_pelanggan.no_meter='%s', tb_pelanggan.waktu_pendaftaran='%s' WHERE tb_pelanggan.id_pelanggan = %s" % (
								 data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran'],data_json[i]['id_pelanggan'])
							cur.execute(sql)
							con.commit()

							# memasukkan perubahan pada status run_bank menjadi 1
							data_json[i]['run'] = '1'
							if transaksi == 'indomaret':
								with open('File JSON/data_pelanggan/temp_data_pelanggan_pln.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_data_pelanggan_pln.json', 'data_pelanggan_pln.json')
							elif transaksi == 'pln':
								with open('File JSON/data_pelanggan/temp_data_pelanggan_indomaret.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')

			# Todo cek insert dari tabel transaksi PLN atau Indomaret
			if action == 'insert' and run == '0':
				# print notifikasi
				print("Terjadi insert data pada file json pada tb_pelanggan " + db_perubahan + "..")
				t = PrettyTable(['id_pelanggan', 'nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran'])
				t.add_row([data_json[i]['id_pelanggan'], data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran']])
				print(t)

				# insert into tb transaksi temporary
				sql = "INSERT INTO tb_pelanggan_temp( nama_pelanggan, alamat, id_meter, no_meter, waktu_pendaftaran) VALUES('%s', '%s', %s, '%s', '%s')" % (
				data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran'])
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "INSERT INTO tb_pelanggan(nama_pelanggan, alamat, id_meter, no_meter, waktu_pendaftaran) VALUES('%s', '%s', %s, '%s', '%s')" % (
				data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran'])
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/data_pelanggan/temp_data_pelanggan_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_pelanggan_pln.json', 'data_pelanggan_pln.json')
				elif transaksi == 'pln':
					with open('File JSON/data_pelanggan/temp_data_pelanggan_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')

			# Todo cek delete dari tabel transaksi PLN atau Indomaret
			if action == 'delete' and run == '0':
				# print notifikasi
				print("Terjadi delete data pada tb_pelanggan " + db_perubahan + "..")
				t = PrettyTable(['id_pelanggan', 'nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran'])
				t.add_row([data_json[i]['id_pelanggan'], data_json[i]['nama_pelanggan'], data_json[i]['alamat'], data_json[i]['id_meter'], data_json[i]['no_meter'], data_json[i]['waktu_pendaftaran']])
				print(t)

				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_pelanggan_temp WHERE id_pelanggan=%s;" % id_json
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "DELETE FROM tb_pelanggan WHERE id_pelanggan=%s;" % id_json
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/data_pelanggan/temp_data_pelanggan_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_pelanggan_pln.json', 'data_pelanggan_pln.json')
				elif transaksi == 'pln':
					with open('File JSON/data_pelanggan/temp_data_pelanggan_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_pelanggan_indomaret.json', 'data_pelanggan_indomaret.json')

# function main
def main():
	#  Todo membuat koneksi
	con = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")

	# Todo membuat cursor
	cur = con.cursor()
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi PLN
	# ============================================
	cekIUD('pln',con,cur)	
	time.sleep(delay)

	# Todo membuat koneksi
	con = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_indomaret")
		
	# Todo membuat cursor
	cur = con.cursor()
	
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi Indomaret
	# ============================================
	cekIUD('indomaret',con,cur)
	time.sleep(delay)
	
	con.close()

# Todo melakukan infinity loop
while True:
	# Todo memanggil fungsi main
	main()