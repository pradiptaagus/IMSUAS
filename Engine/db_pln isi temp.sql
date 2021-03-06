/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.5-10.1.19-MariaDB : Database - db_pln
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_pln` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `db_pln`;

/*Table structure for table `tb_meter` */

DROP TABLE IF EXISTS `tb_meter`;

CREATE TABLE `tb_meter` (
  `id_meter` int(11) NOT NULL AUTO_INCREMENT,
  `tegangan_meter` int(11) NOT NULL,
  PRIMARY KEY (`id_meter`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tb_meter` */

insert  into `tb_meter`(`id_meter`,`tegangan_meter`) values (1,500);

/*Table structure for table `tb_meter_temp` */

DROP TABLE IF EXISTS `tb_meter_temp`;

CREATE TABLE `tb_meter_temp` (
  `id_meter` int(11) NOT NULL AUTO_INCREMENT,
  `tegangan_meter` int(11) NOT NULL,
  PRIMARY KEY (`id_meter`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tb_meter_temp` */

insert  into `tb_meter_temp`(`id_meter`,`tegangan_meter`) values (1,500);

/*Table structure for table `tb_pelanggan` */

DROP TABLE IF EXISTS `tb_pelanggan`;

CREATE TABLE `tb_pelanggan` (
  `id_pelanggan` int(11) NOT NULL AUTO_INCREMENT,
  `nama_pelanggan` varchar(50) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `id_meter` int(11) NOT NULL,
  `no_meter` varchar(25) NOT NULL,
  `waktu_pendaftaran` datetime NOT NULL,
  PRIMARY KEY (`id_pelanggan`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tb_pelanggan` */

insert  into `tb_pelanggan`(`id_pelanggan`,`nama_pelanggan`,`alamat`,`id_meter`,`no_meter`,`waktu_pendaftaran`) values (1,'Pradipta','Klungkung',1,'123efe9','2018-06-03 01:06:52'),(2,'pande nata','Bangli',2,'637gdgs','2018-06-03 15:32:16'),(3,'locong','klungkung',3,'36543gt','2018-06-04 16:49:12');

/*Table structure for table `tb_pelanggan_temp` */

DROP TABLE IF EXISTS `tb_pelanggan_temp`;

CREATE TABLE `tb_pelanggan_temp` (
  `id_pelanggan` int(11) NOT NULL AUTO_INCREMENT,
  `nama_pelanggan` varchar(50) NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `id_meter` int(11) NOT NULL,
  `no_meter` varchar(25) NOT NULL,
  `waktu_pendaftaran` datetime NOT NULL,
  PRIMARY KEY (`id_pelanggan`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `tb_pelanggan_temp` */

insert  into `tb_pelanggan_temp`(`id_pelanggan`,`nama_pelanggan`,`alamat`,`id_meter`,`no_meter`,`waktu_pendaftaran`) values (1,'Pradipta','Klungkung',1,'123efe9','2018-06-03 01:06:52'),(2,'pande nata','Bangli',2,'637gdgs','2018-06-03 15:32:16'),(3,'locong','klungkung',3,'36543gt','2018-06-04 16:49:12');

/*Table structure for table `tb_strom` */

DROP TABLE IF EXISTS `tb_strom`;

CREATE TABLE `tb_strom` (
  `id_strom` int(11) NOT NULL AUTO_INCREMENT,
  `jumlah_pembayaran` int(11) NOT NULL,
  `jumlah_strom` int(11) NOT NULL,
  PRIMARY KEY (`id_strom`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tb_strom` */

insert  into `tb_strom`(`id_strom`,`jumlah_pembayaran`,`jumlah_strom`) values (1,50000,15),(2,50000,15),(3,50000,15),(4,50000,15),(5,50000,15);

/*Table structure for table `tb_strom_temp` */

DROP TABLE IF EXISTS `tb_strom_temp`;

CREATE TABLE `tb_strom_temp` (
  `id_strom` int(11) NOT NULL AUTO_INCREMENT,
  `jumlah_pembayaran` int(11) NOT NULL,
  `jumlah_strom` int(11) NOT NULL,
  PRIMARY KEY (`id_strom`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `tb_strom_temp` */

insert  into `tb_strom_temp`(`id_strom`,`jumlah_pembayaran`,`jumlah_strom`) values (1,50000,15),(2,50000,15),(3,50000,15),(4,50000,15),(5,50000,15);

/*Table structure for table `tb_transaksi` */

DROP TABLE IF EXISTS `tb_transaksi`;

CREATE TABLE `tb_transaksi` (
  `id_transaksi` int(11) NOT NULL AUTO_INCREMENT,
  `id_pelanggan` int(11) NOT NULL,
  `no_token` varchar(25) NOT NULL,
  `id_strom` int(11) NOT NULL,
  `jumlah_strom` int(11) NOT NULL,
  `jumlah_pembayaran` int(11) NOT NULL,
  `waktu_pembelian` datetime NOT NULL,
  PRIMARY KEY (`id_transaksi`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tb_transaksi` */

insert  into `tb_transaksi`(`id_transaksi`,`id_pelanggan`,`no_token`,`id_strom`,`jumlah_strom`,`jumlah_pembayaran`,`waktu_pembelian`) values (1,1,'4354636',1,0,0,'2018-06-02 16:25:59');

/*Table structure for table `tb_transaksi_temp` */

DROP TABLE IF EXISTS `tb_transaksi_temp`;

CREATE TABLE `tb_transaksi_temp` (
  `id_transaksi` int(11) NOT NULL AUTO_INCREMENT,
  `id_pelanggan` int(11) NOT NULL,
  `no_token` varchar(25) NOT NULL,
  `id_strom` int(11) NOT NULL,
  `jumlah_strom` int(11) NOT NULL,
  `jumlah_pembayaran` int(11) NOT NULL,
  `waktu_pembelian` datetime NOT NULL,
  PRIMARY KEY (`id_transaksi`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `tb_transaksi_temp` */

insert  into `tb_transaksi_temp`(`id_transaksi`,`id_pelanggan`,`no_token`,`id_strom`,`jumlah_strom`,`jumlah_pembayaran`,`waktu_pembelian`) values (1,1,'4354636',1,0,0,'2018-06-02 16:25:59');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
