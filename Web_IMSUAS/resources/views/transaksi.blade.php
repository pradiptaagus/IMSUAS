@extends('layout')

@section('page_title')
    Transaksi Indomaret
@endsection

@section('active2')
    active
@endsection

@section('content')
    <div class="card card-body mb-4 wow fadeIn">
        <div class="table-responsive">
            <table id="datatables" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Nama pelanggan</th>
                        <th scope="col">Alamat</th>
                        <th scope="col">No_meter</th>
                        <th scope="col">Tegangan meter</th>
                        <th scope="col">Waktu Pendaftaran</th>
                    </tr>
                </thead>      
                <tbody>
                    
                </tbody>
            </table>
        </div>
    </div>
@endsection