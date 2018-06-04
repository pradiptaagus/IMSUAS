<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Transaction extends Model
{
    protected $table = 'tb_transaksi';
    protected $primaryKey = 'id_transaksi';
    protected $fillable = array('id_pelanggan', 'no_token', 'id_strom', 'jumlah_strom', 'jumlah_pembayaran');

    public $timestamps = false;
}
