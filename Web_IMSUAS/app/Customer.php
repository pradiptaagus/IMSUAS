<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Customer extends Model
{
    protected $table = 'tb_pelanggan';
    protected $primaryKey = 'id_pelanggan';
    protected $fillable = array('nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran');

    public $timestamps = false;
}
