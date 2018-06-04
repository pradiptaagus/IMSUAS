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
                        <th scope="col">No meter</th>
                        <th scope="col">No token</th>
                        <th scope="col">Jumlah strom</th>
                        <th scope="col">Jumlah pembayaran</th>
                        <th scope="col">Waktu pembelian</th>
                        <th scope="col">Aksi</th>
                    </tr>
                </thead>      
                <tbody>
                    @if (count($transactions))
                        @foreach ($transactions as $transaction)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $transaction->nama_pelanggan }}</td>
                                <td>{{ $transaction->no_meter }}</td>
                                <td>{{ $transaction->no_token }}</td>
                                <td>{{ $transaction->jumlah_strom }} kWH</td>
                                <td>Rp. {{ $transaction->jumlah_pembayaran }}</td>
                                <td>{{ $transaction->waktu_pembelian }}</td>
                                <td>
                                    {{-- Edit --}}
                                    <button type="button" class="btn btn-primary btn-sm mr-1" data-toggle="modal" data-target="#updateModal{{$transaction->id_transaksi}}"><i class="fa fa-edit"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="updateModal{{$transaction->id_transaksi}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                <h5 class="modal-title" id="exampleModalCenterTitle"><i class="fa fa-edit"></i> Ubah data pelanggan</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                                </div>
                                                <form method="POST" action="{{ route('transaction.update',$transaction->id_transaksi) }}">
                                                    @csrf
                                                    {{method_field('PUT')}}
                                                    <div class="modal-body">
                                                        <div class="form-group row">
                                                            <label for="cost" class="col-md-4 col-form-label text-md-left">{{ __('Nama pelanggan') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="cost" type="text" class="form-control{{ $errors->has('cost') ? ' is-invalid' : '' }}" name="cost" value="{{ $transaction->nama_pelanggan }}" disabled>
                        
                                                                @if ($errors->has('name'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('name') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>
                                                        
                                                        <div class="form-group row">
                                                            <label for="no_meter" class="col-md-4 col-form-label text-md-left">{{ __('No meter') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="no_meter" type="text" class="form-control{{ $errors->has('no_meter') ? ' is-invalid' : '' }}" name="no_meter" value="{{ $transaction->no_meter }}" disabled>
                        
                                                                @if ($errors->has('no_meter'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('no_meter') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>

                                                        <div class="form-group row">
                                                            <label for="no_token" class="col-md-4 col-form-label text-md-left">{{ __('No token') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="no_token" type="text" class="form-control{{ $errors->has('no_token') ? ' is-invalid' : '' }}" name="no_token" value="{{ $transaction->no_token }}" required>
                        
                                                                @if ($errors->has('no_token'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('no_token') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>

                                                        <div class="form-group row">
                                                            <label for="jml_strom" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah strom') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="jml_strom" type="text" class="form-control{{ $errors->has('jml_strom') ? ' is-invalid' : '' }}" name="jml_strom" value="{{ $transaction->jumlah_strom }}" required>
                        
                                                                @if ($errors->has('jml_strom'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('jml_strom') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>

                                                        <div class="form-group row">
                                                            <label for="jml_pembayaran" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah pembayaran') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="jml_pembayaran" type="text" class="form-control{{ $errors->has('jml_pembayaran') ? ' is-invalid' : '' }}" name="jml_pembayaran" value="{{ $transaction->jumlah_pembayaran }}" required>
                        
                                                                @if ($errors->has('jml_pembayaran'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('jml_pembayaran') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                        <button type="submit" class="btn btn-primary btn-sm"><i class="fa fa-save"></i></button>
                                                    </div>
                                                </form>
                                            </div>
                                        </div>
                                    </div>

                                    {{-- Delete --}}
                                    <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal{{$transaction->id_transaksi}}"><i class="fa fa-times"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="deleteModal{{ $transaction->id_transaksi }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" id="exampleModalLongTitle"><i class="fa fa-times text-danger"></i> Konfirmasi</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                        <span aria-hidden="true">&times;</span>
                                                    </button>
                                                </div>
                                                <div class="modal-body">
                                                    <p>Apakah Anda yakin menghapus transaksi <b>{{$transaction->id_transaksi}}</b></p>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                    <form class="form group" action="{{ route('strom.destroy',$transaction->id_transaksi) }}" method="POST">
                                                        @csrf
                                                        {{method_field('DELETE')}}
                                                        <button style="border-radius: 0px" type="submit" class="btn btn-danger btn-sm"><i class="fa fa-trash"></i></button>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </td>                           
                            </tr>
                        @endforeach
                    @endif
                </tbody>
            </table>
        </div>
    </div>
@endsection