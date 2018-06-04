@extends('layout')

@section('page_title')
    Strom
@endsection

@section('active')
    active
@endsection

@section('active4')
    active
@endsection

@section('content')
    <div class="card card-body mb-4 wow fadeIn">
        <div class="table-responsive">
            <table id="datatables" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Jumlah Pembayaran</th>
                        <th scope="col">Jumlah Strom</th>
                    </tr>
                </thead>      
                <tbody>
                    @if(count($stroms))
                        @foreach ($stroms as $strom)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $strom->jumlah_pembayaran }}</td>
                                <td>{{ $strom->jumlah_strom }}</td>
                            </tr>
                        @endforeach
                    @endif
                </tbody>
            </table>
        </div>
    </div>
@endsection