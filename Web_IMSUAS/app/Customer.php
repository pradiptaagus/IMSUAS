<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Customer extends Model
{
    protected $table = 'tb_pelanggan';
    protected $fillable = array('nama_pelanggan', 'alamat', 'id_meter', 'no_meter', 'waktu_pendaftaran');

    public $timestamps = false;

    public function meter(){
        return $this->belongsTo('App\Meter', 'id_meter');
    }
}
