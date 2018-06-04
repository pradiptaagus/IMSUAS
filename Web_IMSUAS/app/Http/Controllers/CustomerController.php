<?php

namespace App\Http\Controllers;

use DB;
use Illuminate\Http\Request;
use App\Customer;
use App\Meter;

class CustomerController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $meters = Meter::all();
        $customers = DB::table('tb_pelanggan')
                        ->join('tb_meter', 'tb_pelanggan.id_meter', '=', 'tb_meter.id_meter')
                        ->select('tb_pelanggan.*', 'tb_meter.tegangan_meter')->get();
        // return $customers;
        return view('pelanggan', compact('customers', 'meters'));
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
        $customer = new Customer;

        $customer->nama_pelanggan = $request->name;
        $customer->alamat = $request->address;
        $customer->id_meter = $request->voltage;
        $customer->no_meter = $request->no_meter;
        $customer->waktu_pendaftaran = date("Y-m-d H:i:s");

        $customer->save();
        return redirect('/customer');
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
        $customer = Customer::find($id);

        $customer->nama_pelanggan = $request->name;
        $customer->alamat = $request->address;
        $customer->id_meter = $request->voltage;
        $customer->no_meter = $request->no_meter;
        $customer->waktu_pendaftaran = date("Y-m-d H:i:s");

        $customer->save();
        return redirect('/customer');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $customer = Customer::find($id);
		if ($customer) {
			$customer->delete();
		}
		return redirect('/customer');
    }
}
