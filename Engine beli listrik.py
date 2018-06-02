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

# Todo membuat function
# pisahkan masing-masing proses dengan membuat function

# function untuk menambahkan log insert ke file json dari tabel transaksi
# function ini dapat digunakan untuk menambahkan log insert, update, delete ke file json dari PLN maupun Indomaret
# Gunakan function ini saja untuk menghemat penulisan code
def insertJson(id_transaksi, id_pelanggan, no_token, jumlah_strom, jumlah_pembayaran, waktu_pembelian, nama_file_json, action, run):
	list_data = []
	# read file json
	with open('File JSON/' + nama_file_json, 'r', encoding='utf-8') as file:
		try:
			data = json.load(file)
		except:
			data = []
	# menambahkan record baru ke variabel temporary
	new_entry = {'id_transaksi': str(id_transaksi), 'id_pelanggan': str(id_pelanggan), 'no_token': no_token, 'jumlah_strom': str(jumlah_strom), 
				 'jumlah_pembayaran': jumlah_pembayaran, 'waktu_pembelian': waktu_pembelian, 'action': action, 'run': run}
	# append record baru ke variabel array
	list_data.append(new_entry)
	# menyimpan record baru ke file json
	with open('File JSON/' + nama_file_json, 'r', encoding='utf-8')as file:
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


# function main
def main():
	# Todo membuat koneksi
	con_pln = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_pln")
	con_indomaret = pymysql.connect(host = "localhost", user = "root", passwd = "", db = "db_indomaret")
	

	# Todo membuat cursor
	cur_pln = con_pln.cursor()
	cur_indomaret = con_indomaret.cursor()


	# Todo select semua data dari tabel transaksi PLN dan Indomaret
	# Select data dari tabel tb_transaksi PLN
	cur_pln.execute("SELECT * FROM tb_transaksi")
	data_pln = cur_pln.fetchall()
	
	# Select data dari tabel tb_transaksi Indomaret
	cur_indomaret.execute("SELECT * FROM tb_transaksi")
	data_indomaret = cur_indomaret.fetchall()

	# Select data dari tabel tb_transaksi_temp PLN
	cur_pln.execute("SELECT * FROM tb_transaksi_temp")
	data_pln_temp = cur_pln.fetchall()
	
	# Select data dari tabel tb_transaksi_temp Indomaret
	cur_indomaret.execute("SELECT * FROM tb_transaksi_temp")
	data_indomaret_temp = cur_indomaret.fetchall()
	

	# Todo Menghitung banyak data dari tabel transaksi PLN dan Indomaret
	jumlah_data_pln = len(data_pln)
	jumlah_data_indomaret = len(data_indomaret)

	# Todo menghitung banyak data dari tabel transaksi temporary PLN dan Indomaret
	jumlah_data_pln_temp = len(data_pln_temp)
	jumlah_data_indomaret_temp = len(data_indomaret_temp)

	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi PLN
	# ============================================

	# Todo cek update dari tabel transaksi PLN
	if jumlah_data_pln == jumlah_data_pln_temp:
		print("Cek update pada tabel transaksi PLN..")
		for i in range(0, jumlah_data_pln):
			# Melakukan select concat pada tabel transaksi PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', jumlah_strom, ' ', jumlah_pembayaran, ' ', waktu_pembelian, ' ') AS data_pln FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s"  % i
			cur_pln.execute(sql)
			record_pln = cur_pln.fetchone()


			# Melakukan select concat pada tabel transaksi temp PLN
			sql = "SELECT CONCAT(id_transaksi, ' ', id_pelanggan, ' ', no_token, ' ', jumlah_strom, ' ', jumlah_pembayaran, ' ', waktu_pembelian, ' ') AS data_pln_temp FROM tb_transaksi_temp WHERE tb_transaksi_temp.id_transaksi = %s"  % i
			cur_pln.execute(sql)
			record_pln_temp = cur_pln.fetchone()

			if record_pln != record_pln_temp:
				# print notifikasi
				print("Terjadi update data pada tb_transaksi PLN..")
				t = PrettyTable(['id_transaksi', 'no_rek old', 'no_rek new'])
				t.add_row([data_pln[i][0], data_pln_temp[i][1], data_pln[i][1]])
				print(t)
				
				sql = "UPDATE tb_transaksi_temp SET tb_transaksi_temp.id_pelanggan = %s, tb_transaksi_temp.no_token = '%s', tb_transaksi_temp.jumlah_strom = %s, tb_transaksi_temp.jumlah_pembayaran = '%s', tb_transaksi_temp.waktu_pembelian = '%s' WHERE tb_transaksi_temp.id_transaksi = %s" %(
						  data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5], data_pln_temp[i][0]
					  )
				cur_pln.execute(sql)
				con_pln.commit()

				# Memasukkan perubahan ke file json
				insertJson(data_pln[i][0], data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5], 'pln.json', 'update', '0')


	# Todo cek insert dari tabel transaksi PLN
	if jumlah_data_pln > jumlah_data_pln_temp:
		print("Cek insert pada tabel transaksi PLN..")
		for i in range(jumlah_data_pln_temp, jumlah_data_pln):
			sql = "INSERT INTO tb_transaksi_temp(id_pelanggan, no_token, jumlah_strom, jumlah_pembayaran, waktu_pembelian) VALUES(%s, '%s', %s, '%s', '%s')" % (
				data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5])
			cur_pln.execute(sql)
			con_pln.commit()

			# print notifikasi
			print("Terjadi insert data pada tb_transaksi PLN..")
			t = PrettyTable(['id_transaksi', 'id_pelanggan', 'no_token', 'jumlah_strom', 'jumlah_pembayaran', 'waktu_pembelian'])
			t.add_row([data_pln[i][0], data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5]])
			print(t)
		
		# Memasukkan perubahan ke file json
		insertJson(data_pln[i][0], data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5], 'pln.json', 'insert', '0')


	# Todo cek delete dari tabel transaksi PLN
	if jumlah_data_pln < jumlah_data_pln_temp:
		print("Cek delete pada tabel transaksi PLN")
		for i in range(0, jumlah_data_pln_temp):
			cur_pln.execute("SELECT * FROM tb_transaksi WHERE tb_transaksi.id_transaksi = %s" % data_pln_temp[i][0])
			record_pln = cur_pln.fetchone()
			if record_pln is None == True:
				# print notifikasi
				print("Cek delete pada tabel transaksi PLN..")
				print("Terjadi delete data pada tabel transaksi PLN..")
				t = PrettyTable(['id_transaksi'])
				t.add_row([data_pln_temp[i][0]])
				print(t)

				# Memasukkan perubahan ke file json
				insertJson(data_pln[i][0], data_pln[i][1], data_pln[i][2], data_pln[i][3], data_pln[i][4], data_pln[i][5], 'pln.json', 'delete', '0')
				
				
	# ============================================
	# Mulai proses 
	# ============================================
	# Cek tabel transaksi Indomaret
	# ============================================

	# Todo cek update dari tabel transaksi PLN


	# Todo cek insert dari tabel transaksi PLN


	# Todo cek delete dari tabel transaksi PLN


	# ============================================
	# Mulai proses 
	# ============================================
	# Cek file JSON PLN
	# ============================================

	# Todo cek update dari tabel transaksi PLN


	# Todo cek insert dari tabel transaksi PLN


	# Todo cek delete dari tabel transaksi PLN


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
	# Todo menentukan delay dari engine dengan meminta input dari user
	delay = int(input("Masukkan waktu delay: "))
	# Todo memanggil fungsi main