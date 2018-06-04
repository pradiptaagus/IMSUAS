<?php

namespace App\Http\Controllers;

use DB;
use Illuminate\Http\Request;
use App\Customer;
use App\Transaction;
use App\Strom;

class DashboardController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $names = Customer::all();
        $customers = DB::table('tb_pelanggan')
                        ->join('tb_meter', 'tb_pelanggan.id_meter', '=', 'tb_meter.id_meter')
                        ->select('tb_pelanggan.*', 'tb_meter.tegangan_meter')->orderBy('id_pelanggan', 'desc')->get();
        $sum_customers = Customer::all()->count();
        $sum_transactions = Transaction::all()->count();
        $stroms = Strom::all();
        return view('dashboard', compact('customers','sum_transactions', 'sum_customers', 'stroms', 'names'));
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $transaction = new Transaction;
        
        
        if ($request->voltage == 1) {
            $jml_pembayaran = 60000;
            $jml_strom = 50;
        }elseif ($request->voltage == 2) {
            $jml_pembayaran = 35000;
            $jml_strom = 30;
        }elseif ($request->voltage == 3) {
            $jml_pembayaran = 20000;
            $jml_strom = 20;
        }

        $transaction->id_pelanggan = $request->nama;
        $transaction->no_token = $request->no_token;
        $transaction->id_strom = $request->voltage;
        $transaction->jumlah_strom = $jml_strom;
        $transaction->jumlah_pembayaran = $jml_pembayaran;
        $transaction->waktu_pembelian = date("Y-m-d H:i:s");

        $transaction->save();
        return redirect('/');
    }

}
