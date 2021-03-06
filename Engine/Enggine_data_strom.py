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
def insertJson(id_storm, jumlah_pembayaran, jumlah_strom, nama_file_json, action, run):
	list_data = []
	# read file json
	with open('File JSON/data_strom/' + nama_file_json, 'r', encoding='utf-8') as file:
		try:
			data = json.load(file)
		except:
			data = []
	# menambahkan record baru ke variabel temporary
	new_entry = {'id_strom': str(id_storm), 'jumlah_pembayaran': str(jumlah_pembayaran), 'jumlah_strom': str(jumlah_strom), 'action': action, 'run': run}
	# append record baru ke variabel array
	list_data.append(new_entry)
	# menyimpan record baru ke file json
	with open('File JSON/data_strom/' + nama_file_json, 'w', encoding='utf-8')as file:
		json.dump(data + list_data, file, indent=4)

# function untuk mengunggah file json dari drive local 
# function ini dapat digunakan untuk mengunggah file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def uploadJson(local_file, dropbox_file):
	dropbox_access_token = dropbox.Dropbox("9Em04orxhVAAAAAAAAAAEkWTQhZXnfIGW44R7Yz9i6QSpfRaKxt4lR2hrq6IUtXr")
	file_path = pathlib.Path('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/data_strom/' + local_file)
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
		dbx.files_download_to_file('E:/Dokument Semester 4/Integrasi dan Migrasi Sistem/Project Akhir/IMSUAS/Engine/File JSON/data_strom/' + local_file, '/' + target_file)
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
		# Select data dari tabel tb_strom Indomaret
		cur_indomaret.execute("SELECT * FROM tb_strom")
		data = cur_indomaret.fetchall()
		
		# Select data dari tabel tb_strom_temp Indomaret
		cur_indomaret.execute("SELECT * FROM tb_strom_temp")
		data_temp = cur_indomaret.fetchall()
		

		# Todo Menghitung banyak data dari tabel transaksi Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('data_strom_indomaret.json', 'data_strom_indomaret.json')
		con_indomaret.close()

	elif  transaksi == 'pln':
		# Todo membuat koneksi
		con_pln = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")

		# Todo membuat cursor
		cur_pln = con_pln.cursor()
		
		# Todo select semua data dari tabel transaksi PLN dan Indomaret
		# Select data dari tabel tb_strom PLN
		cur_pln.execute("SELECT * FROM tb_strom")
		data = cur_pln.fetchall()
		
		# Select data dari tabel tb_strom_temp PLN
		cur_pln.execute("SELECT * FROM tb_strom_temp")
		data_temp = cur_pln.fetchall()

		# Todo Menghitung banyak data dari tabel transaksi PLN dan Indomaret
		jumlah_data = len(data)

		# Todo menghitung banyak data dari tabel transaksi temporary PLN dan Indomaret
		jumlah_data_temp = len(data_temp)

		downloadJson('data_strom_pln.json', 'data_strom_pln.json')
		con_pln.close()

	# Todo cek update dari tabel transaksi PLN
	if jumlah_data == jumlah_data_temp:
		print("Cek update pada tabel strom " + transaksi + "..")
		for i in range(0, jumlah_data):
			a = i + 1
			# Melakukan select concat pada tabel transaksi PLN
			sql = "SELECT CONCAT(id_strom,' ', jumlah_pembayaran, ' ', jumlah_strom, ' ') AS data_pln FROM tb_strom WHERE tb_strom.id_strom = %s"  % data[i][0]
			cur.execute(sql)
			record = cur.fetchone()

			# Melakukan select concat pada tabel transaksi temp PLN
			sql = "SELECT CONCAT(id_strom,' ', jumlah_pembayaran, ' ', jumlah_strom, ' ') AS data_pln_temp FROM tb_strom_temp WHERE tb_strom_temp.id_strom = %s"  % data[i][0]
			cur.execute(sql)
			record_temp = cur.fetchone()

			if record != record_temp:
				# print notifikasi
				print("Terjadi update data pada tb_strom " + transaksi + "..")
				t = PrettyTable(['id_strom', 'jumlah_pembayaran', 'jumlah_strom'])
				t.add_row([data[i][0], data[i][1], data[i][2]])
				print(t)
				
				sql = "UPDATE tb_strom_temp SET tb_strom_temp.jumlah_pembayaran = %s, tb_strom_temp.jumlah_strom = %s WHERE tb_strom_temp.id_strom = %s" % (
						  data[i][1], data[i][2], data_temp[i][0]
					  )
				cur.execute(sql)
				con.commit()

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], 'data_strom_indomaret.json', 'update', '0')
					uploadJson('data_strom_indomaret.json', 'data_strom_indomaret.json')
				elif  transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data[i][0], data[i][1], data[i][2], 'data_strom_pln.json', 'update', '0')
					uploadJson('data_strom_pln.json', 'data_strom_pln.json')

	# Todo cek insert dari tabel transaksi PLN
	if jumlah_data > jumlah_data_temp:
		print("Cek insert pada tabel transaksi " + transaksi + "..")
		for i in range(jumlah_data_temp, jumlah_data):
			sql = "INSERT INTO tb_strom_temp(jumlah_pembayaran, jumlah_strom) VALUES(%s, %s)" % (
				data[i][1], data[i][2])
			cur.execute(sql)
			con.commit()

			# print notifikasi
			print("Terjadi insert data pada tb_strom " + transaksi + "..")
			t = PrettyTable(['id_strom', 'jumlah_pembayaran', 'jumlah_strom'])
			t.add_row([data[i][0], data[i][1], data[i][2]])
			print(t)

		if transaksi == 'indomaret':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], 'data_strom_indomaret.json', 'insert', '0')
			uploadJson('data_strom_indomaret.json', 'data_strom_indomaret.json')
		elif  transaksi == 'pln':
			# Memasukkan perubahan ke file json
			insertJson(data[i][0], data[i][1], data[i][2], 'data_strom_pln.json', 'insert', '0')
			uploadJson('data_strom_pln.json', 'data_strom_pln.json')

	# Todo cek delete dari tabel transaksi PLN
	if jumlah_data < jumlah_data_temp:
		print("Cek delete pada tabel transaksi " + transaksi + "..")
		for i in range(0, jumlah_data_temp):
			cur.execute("SELECT * FROM tb_strom WHERE tb_strom.id_strom = %s" % data_temp[i][0])
			record = cur.fetchone()
			#  is None == True
			if cur.rowcount == 0:
				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_strom_temp WHERE id_strom=%s;" % data_temp[i][0]
				cur.execute(sql)
				con.commit()

				# print notifikasi
				print("Terjadi delete data pada tabel strom " + transaksi + "..")
				t = PrettyTable(['id_strom'])
				t.add_row([data_temp[i][0]])
				print(t)

				if transaksi == 'indomaret':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], 'data_strom_indomaret.json', 'delete', '0')
					uploadJson('data_strom_indomaret.json', 'data_strom_indomaret.json')
				if transaksi == 'pln':
					# Memasukkan perubahan ke file json
					insertJson(data_temp[i][0], data_temp[i][1], data_temp[i][2], 'data_strom_pln.json', 'delete', '0')
					uploadJson('data_strom_pln.json', 'data_strom_pln.json')

	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON PLN atau Indomaret
	# ============================================
	if transaksi == 'indomaret':
		downloadJson('data_strom_pln.json', 'temp_data_strom_pln.json')
        # Cek Pembahruan dalam JSON file database bank
		with open('File JSON/data_strom/temp_data_strom_pln.json', 'r', encoding='utf-8') as report:
			try:
				data_json = json.load(report)
			except:
				data_json = []
		jumlah_data_json = len(data_json)
		db_perubahan = 'pln'

	elif transaksi == 'pln':
		downloadJson('data_strom_indomaret.json', 'temp_data_strom_indomaret.json')
        # Cek Pembahruan dalam JSON file database toko
		with open('File JSON/data_strom/temp_data_strom_indomaret.json', 'r', encoding='utf-8') as report:
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
			id_json = int(data_json[i]['id_strom'])

			# Todo cek update dari tabel transaksi PLN atau Indomaret
			if action == 'update' and run == '0':
				for a in range(jumlah_data_temp):
					if id_json == data_temp[a][0]:
						isi_data_json = data_json[i]['id_strom'] + ' ' + data_json[i]['jumlah_pembayaran'] + ' ' + data_json[i]['jumlah_strom']

						sql = "SELECT CONCAT(id_strom,' ', jumlah_pembayaran, ' ', jumlah_strom, ' ') AS data_pln_temp FROM tb_strom_temp WHERE tb_strom_temp.id_strom = %s"  % data_temp[a][0]
						cur.execute(sql)
						record_temp = cur.fetchone()
						str_record_temp =''.join(record_temp)

						if isi_data_json != str_record_temp:
							# print notifikasi
							# print(
                            #     "Terjadi perubahan pada Json, data sebelumnya %s berubah menjadi %s pada id %s" % (
                            #         str_record_temp, isi_data_json, id_json))
							print("Terjadi perubahan pada Json pada tb_strom " + transaksi + "..")
							t = PrettyTable(['id_strom', 'jumlah_pembayaran', 'jumlah_strom'])
							t.add_row([data_json[i]['id_strom'], data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom']])
							print(t)

							# update pada tabel transaksi temporary
							sql = "UPDATE tb_strom_temp SET tb_strom_temp.jumlah_pembayaran = %s, tb_strom_temp.jumlah_strom = %s WHERE tb_strom_temp.id_strom = %s" % (
								data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom'], data_json[i]['id_strom'])
							cur.execute(sql)
							con.commit()

							# update pada tabel transaksi
							sql = "UPDATE tb_strom SET tb_strom.jumlah_pembayaran = %s, tb_strom.jumlah_strom = %s WHERE tb_strom.id_strom = %s" % (
								data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom'],data_json[i]['id_strom'])
							cur.execute(sql)
							con.commit()

							# memasukkan perubahan pada status run_bank menjadi 1
							data_json[i]['run'] = '1'
							if transaksi == 'indomaret':
								with open('File JSON/data_strom/temp_data_strom_pln.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_data_strom_pln.json', 'data_strom_pln.json')
							elif transaksi == 'pln':
								with open('File JSON/data_strom/temp_data_strom_indomaret.json', 'w', encoding='utf-8') as report:
									json.dump(data_json, report, indent=4)
								uploadJson('temp_data_strom_indomaret.json', 'data_strom_indomaret.json')

			# Todo cek insert dari tabel transaksi PLN atau Indomaret
			if action == 'insert' and run == '0':
				# print notifikasi
				print("Terjadi insert data pada file json pada tb_strom " + db_perubahan + "..")
				t = PrettyTable(['id_strom', 'jumlah_pembayaran', 'jumlah_strom'])
				t.add_row([data_json[i]['id_strom'],data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom']])
				print(t)

				# insert into tb transaksi temporary
				sql = "INSERT INTO tb_strom_temp(jumlah_pembayaran, jumlah_strom) VALUES(%s, %s)" % (
				data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom'])
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "INSERT INTO tb_strom(jumlah_pembayaran, jumlah_strom) VALUES(%s, %s)" % (
				data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom'])
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/data_strom/temp_data_strom_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_strom_pln.json', 'data_strom_pln.json')
				elif transaksi == 'pln':
					with open('File JSON/data_strom/temp_data_strom_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_strom_indomaret.json', 'data_strom_indomaret.json')

			# Todo cek delete dari tabel transaksi PLN atau Indomaret
			if action == 'delete' and run == '0':
				# print notifikasi
				print("Terjadi delete data pada tb_strom " + db_perubahan + "..")
				t = PrettyTable(['id_strom', 'jumlah_pembayaran', 'jumlah_strom'])
				t.add_row([data_json[i]['id_strom'],data_json[i]['jumlah_pembayaran'], data_json[i]['jumlah_strom']])
				print(t)

				# delete di tabel transaksi temporary database
				sql = "DELETE FROM tb_strom_temp WHERE id_strom=%s;" % id_json
				cur.execute(sql)
				con.commit()

				# insert into tb transaksi
				sql = "DELETE FROM tb_strom WHERE id_strom=%s;" % id_json
				cur.execute(sql)
				con.commit()					
				
				# memasukkan perubahan pada status run_bank menjadi 1
				data_json[i]['run'] = '1'
				if transaksi == 'indomaret':
					with open('File JSON/data_strom/temp_data_strom_pln.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_strom_pln.json', 'data_strom_pln.json')
				elif transaksi == 'pln':
					with open('File JSON/data_strom/temp_data_strom_indomaret.json', 'w', encoding='utf-8') as report:
						json.dump(data_json, report, indent=4)
					uploadJson('temp_data_strom_indomaret.json', 'data_strom_indomaret.json')

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