<?php

namespace App\Http\Controllers;

use DB;
use Illuminate\Http\Request;
use App\Transaction;
use App\Meter;

class TransactionController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $transactions = DB::table('tb_transaksi')
                            ->join('tb_strom', 'tb_transaksi.id_strom', '=', 'tb_strom.id_strom')
                            ->join('tb_pelanggan', 'tb_transaksi.id_pelanggan', '=', 'tb_pelanggan.id_pelanggan')
                            ->select('tb_transaksi.*', 'tb_pelanggan.nama_pelanggan', 'tb_pelanggan.no_meter')->orderBy('id_transaksi', 'desc')->get();
        // return $transactions;
        return view('transaksi', compact('transactions'));
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $transaction = New Transaction;

        $transaction->id_pelanggan = $request->customer;
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
    }
}
