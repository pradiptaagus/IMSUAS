@extends('layout')

@section('page_title')
    Meter
@endsection

@section('active')
    active
@endsection

@section('active5')
    active
@endsection

@section('content')
    <div class="card card-body mb-4 wow fadeIn">
        <div class="table-responsive">
            <table id="datatables" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Tegangan meter</th>
                    </tr>
                </thead>      
                <tbody>
                    @if(count($meters))
                        @foreach ($meters as $meter)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $meter->tegangan_meter }}</td>
                            </tr>
                        @endforeach
                    @endif
                </tbody>
            </table>
        </div>
    </div>
@endsection