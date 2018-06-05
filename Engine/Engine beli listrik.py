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
def insertJson(id_transaksi, id_pelanggan, no_token, id_strom, jumlah_strom, jumlah_pembayaran, waktu_pembelian, nama_file_json, action, run):
	list_data = []
	# read file json
	with open('File JSON/' + nama_file_json, 'r', encoding='utf-8') as file:
		try:
			data = json.load(file)
		except:
			data = []
	# menambahkan record baru ke variabel temporary
	new_entry = {'id_transaksi': str(id_transaksi), 'id_pelanggan': str(id_pelanggan), 'no_token': no_token, 'id_strom': str(id_strom), 
				 'jumlah_strom': str(jumlah_strom), 'jumlah_pembayaran': str(jumlah_pembayaran), 'waktu_pembelian': str(waktu_pembelian), 'action': action, 'run': run}
	# append record baru ke variabel array
	list_data.append(new_entry)
	# menyimpan record baru ke file json
	with open('File JSON/' + nama_file_json, 'w', encoding='utf-8')as file:
		json.dump(data + list_data, file, indent=4)

# function untuk mengunggah file json dari drive local 
# funct87ion ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine
def uploadJson(local_file, dropbox_file):
	dropbox_access_token = dropbox.Dropbox("9Em04orxhVAAAAAAAAAAEkWTQhZXnfIGW44R7Yz9i6QSpfRaKxt4lR2hrq6IUtXr")
	file_path = pathlib.Path('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/' + local_file)
	with file_path.open('rb') as file:
		dropbox_access_token.files_upload(file.read(), '/' + dropbox_file, mode=dropbox.files.WriteMode("overwrite"))
	print(local_file + "berhasil diunggah")


# function untuk mengunduh file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def downloadJson(target_file, local_file):
	# E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine
	try:
		dbx = dropbox.Dropbox('9Em04orxhVAAAAAAAAAAEkWTQhZXnfIGW44R7Yz9i6QSpfRaKxt4lR2hrq6IUtXr')
		target_file_dropbox = "/" + target_file
		link = dbx.sharing_create_shared_link(target_file_dropbox)
		url = link.url
		dl_url = re.sub(r"\?dl\=1", "?dl=1", url)
		print(dl_url)
		dbx.files_download_to_file('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/' + local_file, '/' + target_file)
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
		# Select data dari tabel tb_transaksi Indomaret
		cur_indomaret.execute("SELECT * FROM tb_transaksi")
		data = cur_indomaret.fetchall()
		
		# Select data dari tabel tb_transaksi_temp Indomaret
		cur_indomaret.execute("SELECT * FROM tb_transaksi_temp")
		data_temp = cur_indomaret.fetchall()
		

		# Todo Menghitung banyak data dari tabel transaksi Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('indomaret.json', 'indomaret.json')
		con_indomaret.close()

	elif  transaksi == 'pln':
		# Todo membuat koneksi
		con_pln = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")

		# Todo membuat cursor
		cur_pln = con_pln.cursor()
		
		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_transaksi PLN
		cur_pln.execute("SELECT * FROM tb_transaksi")
		data = cur_pln.fetchall()
		
		# Select data dari tabel tb_transaksi_temp PLN
		cur_pln.execute("SELECT * FROM tb_transaksi_temp")
		data_temp = cur_pln.fetchall()

		# Todo Menghitung banyak data dari tabel transaksi PLN dan Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary PLN dan Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('pln.json', 'pln.json')
		con_pln.close()

	# Todo cek update dari tabel transaksi PLN
	if jumlah_data == jumlah_data_temp:
		print("Cek update pada tabel transaksi " + transaksi + "..")
		for i in range(1, jumlah_data+1):
			# Melakukan select concat pada tabel transaksi PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', id_strom, ' ', jumlah_strom, ' ', jumlah_pembayaran, ' ', waktu_pembelian, ' ') AS data_pln FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s"  % data[i-1][0]
			cur.execute(sql)
			record = cur.fetchone()

			# Melakukan select concat pada tabel transaksi temp PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', id_strom, ' ', jumlah_strom, ' ', jumlah_pembayaran, ' ', waktu_pembelian, ' ') AS data_pln_temp FROM tb_transaksi_temp WHERE tb_transaksi_temp.id_transaksi = %s"  % data[i-1][0]
			cur.execute(sql)
			record_temp = cur.fetchone()

			if record != record_temp:
				# print notifikasi
				print("Terjadi update data pada tb_transaksi " + transaksi + "..")
				t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran','waktu_pembelian'])
				t.add_row([data[i-1][0], data[i-1][1], data[i-1][2], data[i-1][3], data[i-1][4],data[i-1][5],data[i-1][6]])
				print(t)
				
				sql = "UPDATE tb_transaksi_temp SET tb_transaksi_temp.id_pelanggan = %s, tb_transaksi_temp.no_token = '%s', tb_transaksi_temp.id_strom = %s,tb_transaksi_temp.jumlah_strom=%s, tb_transaksi_temp.jumlah_pembayaran=%s, tb_transaksi_temp.waktu_pembelian = '%s' WHERE tb_transaksi_temp.id_transaksi = %s" %(
						  data[i-1][1], data[i-1][2], data[i-1][3], data[i-1][4],data[i-1][5],data[i-1][6], data_temp[i-1][0]
					  )
				cur.execute(sql)
				con.commit()

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data[i-1][0], data[i-1][1], data[i-1][2], data[i-1][3], data[i-1][4],data[i-1][5],data[i-1][6], 'indomaret.json', 'update', '0')
					uploadJson('indomaret.json', 'indomaret.json')
				elif  transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data[i-1][0], data[i-1][1], data[i-1][2], data[i-1][3], data[i-1][4],data[i-1][5],data[i-1][6], 'pln.json', 'update', '0')
					uploadJson('pln.json', 'pln.json')

	# Todo cek insert dari tabel transaksi PLN
	if jumlah_data > jumlah_data_temp:
		print("Cek insert pada tabel transaksi " + transaksi + "..")
		for i in range(jumlah_data_temp, jumlah_data):
			sql = "INSERT INTO tb_transaksi_temp(id_pelanggan, no_token, id_strom, jumlah_strom, jumlah_pembayaran, waktu_pembelian) VALUES(%s, '%s', %s, %s, %s, '%s')" % (
				data[i][1], data[i][2], data[i][3], data[i][4],data[i][5],data[i][6])
			cur.execute(sql)
			con.commit()

			# print notifikasi
			print("Terjadi insert data pada tb_transaksi " + transaksi + "..")
			t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran', 'waktu_pembelian'])
			t.add_row([data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]])
			print(t)

		if transaksi == 'indomaret':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5],data[i][6], 'indomaret.json', 'insert', '0')
			uploadJson('indomaret.json', 'indomaret.json')
		elif  transaksi == 'pln':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4],data[i][5],data[i][6], 'pln.json', 'insert', '0')
			uploadJson('pln.json', 'pln.json')

	# Todo cek delete dari tabel transaksi PLN
	if jumlah_data < jumlah_data_temp:
		print("Cek delete pada tabel transaksi " + transaksi + "..")
		for i in range(0, jumlah_data_temp):
			cur.execute("SELECT * FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s" % data_temp[i][0])
			record = cur.fetchone()
			#  is None == True
			if cur.rowcount == 0:
				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_transaksi_temp WHERE id_transaksi=%s;" % data_temp[i][0]
				cur.execute(sql)
				con.commit()

				# print notifikasi
				print("Terjadi delete data pada tabel transaksi " + transaksi + "..")
				t = PrettyTable(['id_transaksi'])
				t.add_row([data_temp[i][0]])
				print(t)

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], data_temp[i][3], data_temp[i][4], data_temp[i][5], data_temp[i][6], 'indomaret.json', 'delete', '0')
					uploadJson('indomaret.json', 'indomaret.json')
				if transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], data_temp[i][3], data_temp[i][4],data_temp[i][5],data_temp[i][6], 'pln.json', 'delete', '0')
					uploadJson('pln.json', 'pln.json')

	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON PLN atau Indomaret
	# ============================================
	if transaksi == 'indomaret':
		downloadJson('pln.json', 'temp_pln.json')
        # Cek Pembahruan dalam JSON file database bank
		with open('File JSON/temp_pln.json', 'r', encoding='utf-8') as report:
			try:
				data_json = json.load(report)
			except:
				data_json = []
		jumlah_data_json = len(data_json)
		db_perubahan = 'pln'

	elif transaksi == 'pln':
		downloadJson('indomaret.json', 'temp_indomaret.json')
        # Cek Pembahruan dalam JSON file database toko
		with open('File JSON/temp_indomaret.json', 'r', encoding='utf-8') as report:
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
			id_json = int(data_json[i]['id_transaksi'])

			# Todo cek update dari tabel transaksi PLN atau Indomaret
			if action == 'update' and run == '0':
				for a in range(jumlah_data_temp):
					if id_json == data_temp[a][0]:
						isi_data_json = data_json[i]['id_pelanggan'] + ' ' + data_json[i]['no_token'] + ' ' + data_json[i]['id_strom']+ ' ' + data_json[i]['jumlah_strom']+ ' ' + data_json[i]['jumlah_pembayaran'] + ' ' + data_json[i]['waktu_pembelian']
						# len_isi_data_json = len(isi_data_json)
						# print(len_isi_data_json)
						# print(isi_data_json)

						sql = "SELECT CONCAT(id_pelanggan, ' ', no_token, ' ', id_strom, ' ', jumlah_strom, ' ', jumlah_pembayaran, ' ', waktu_pembelian) AS data_pln_temp FROM tb_transaksi_temp WHERE tb_transaksi_temp.id_transaksi = %s"  % data_temp[a][0]
						cur.execute(sql)
						record_temp = cur.fetchone()
						str_record_temp =''.join(record_temp)

						if isi_data_json != str_record_temp:
							# print notifikasi
							# print(
                            #     "Terjadi perubahan pada Json, data sebelumnya %s berubah menjadi %s pada id %s" % (
                            #         str_record_temp, isi_data_json, id_json))
							print("Terjadi update data pada file json pada tb_transaksi " + transaksi + "..")
							t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran','waktu_pembelian'])
							t.add_row([data_json[i]['id_transaksi'],data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian']])
							print(t)

							# update pada tabel transaksi temporary
							sql = "UPDATE tb_transaksi_temp SET tb_transaksi_temp.id_pelanggan = %s, tb_transaksi_temp.no_token = '%s', tb_transaksi_temp.id_strom = %s,tb_transaksi_temp.jumlah_strom=%s, tb_transaksi_temp.jumlah_pembayaran=%s, tb_transaksi_temp.waktu_pembelian = '%s' WHERE tb_transaksi_temp.id_transaksi = %s" % (
								data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian'], data_json[i]['id_transaksi'])
							cur.execute(sql)
							con.commit()

							# update pada tabel transaksi
							sql = "UPDATE tb_transaksi SET tb_transaksi.id_pelanggan = %s, tb_transaksi.no_token = '%s', tb_transaksi.id_strom = %s,tb_transaksi.jumlah_strom=%s, tb_transaksi.jumlah_pembayaran=%s, tb_transaksi.waktu_pembelian = '%s' WHERE tb_transaksi.id_transaksi = %s" % (
								data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian'], data_json[i]['id_transaksi'])
							cur.execute(sql)
							con.commit()

							# memasukkan perubahan pada status run_bank menjadi 1Engine/Engine/
							data_json[i]['run'] = '1'
							if transaksi == 'indomaret':
								with open('File JSON/temp_pln.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_pln.json', 'pln.json')
							elif transaksi == 'pln':
								with open('File JSON/temp_indomaret.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_indomaret.json', 'indomaret.json')

			# Todo cek insert dari tabel transaksi PLN atau Indomaret
			if action == 'insert' and run == '0':
				# print notifikasi
				print("Terjadi insert data pada file json pada tb_transaksi " + db_perubahan + "..")
				t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran', 'waktu_pembelian'])
				t.add_row([data_json[i]['id_transaksi'], data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian']])
				print(t)

				# insert into tb transaksi temporary
				sql = "INSERT INTO tb_transaksi_temp(id_pelanggan, no_token, id_strom, jumlah_strom, jumlah_pembayaran, waktu_pembelian) VALUES(%s, '%s', %s, %s, %s, '%s')" % (
				data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian'])
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "INSERT INTO tb_transaksi(id_pelanggan, no_token, id_strom, jumlah_strom, jumlah_pembayaran, waktu_pembelian) VALUES(%s, '%s', %s, %s, %s, '%s')" % (
				data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian'])
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/temp_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_pln.json', 'pln.json')
				elif transaksi == 'pln':
					with open('File JSON/temp_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_indomaret.json', 'indomaret.json')

			# Todo cek delete dari tabel transaksi PLN atau Indomaret
			if action == 'delete' and run == '0':
				# print notifikasi
				print("Terjadi delete data pada tb_transaksi " + db_perubahan + "..")
				t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran', 'waktu_pembelian'])
				t.add_row([data_json[i]['id_transaksi'],data_json[i]['id_pelanggan'], data_json[i]['no_token'], data_json[i]['id_strom'], data_json[i]['jumlah_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['waktu_pembelian']])
				print(t)

				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_transaksi_temp WHERE id_transaksi=%s;" % id_json
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "DELETE FROM tb_transaksi WHERE id_transaksi=%s;" % id_json
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/temp_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_pln.json', 'pln.json')
				elif transaksi == 'pln':
					with open('File JSON/temp_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_indomaret.json', 'indomaret.json')

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