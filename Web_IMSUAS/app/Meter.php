<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Meter extends Model
{
    protected $table = 'tb_meter';
    protected $primaryKey = 'id_meter';
    protected $fillable = array('tegangan_meter');

    public $timestamps = false;
}
