<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Strom extends Model
{
    protected $table = 'tb_strom';
    protected $primaryKey = 'id_strom';
    protected $fillable = array('jumlah_pembayaran', 'jumlah_strom');

    public $timestamps = false;
}
