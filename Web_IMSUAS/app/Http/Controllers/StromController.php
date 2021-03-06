<?php

namespace App\Http\Controllers;

use DB;
use Illuminate\Http\Request;
use App\Strom;

class StromController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $stroms = Strom::all();
        return view('strom', compact('stroms'));
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
        $strom = new Strom;

        $strom->jumlah_pembayaran = $request->cost;
        $strom->jumlah_strom = $request->strom_result;

        $strom->save();
        return redirect('/strom');
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
        $strom = Strom::find($id);

        $strom->jumlah_pembayaran = $request->cost;
        $strom->jumlah_strom = $request->strom_result;

        $strom->save();
        return redirect('/strom');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $strom = Strom::where('id_strom', '=', $id);

        $strom->delete();

        return redirect('/strom');
    }
}
