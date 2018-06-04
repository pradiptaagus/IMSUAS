<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Meter extends Model
{
    protected $table = 'tb_meter';
    protected $fillable = array('id', 'tegangan_meter');

    public function customer(){
        return $this->hashMany('App\Customer');
    }
}
