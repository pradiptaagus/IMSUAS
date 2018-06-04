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
            <button type="button" class="btn btn-primary btn-sm mb-3" data-toggle="modal" data-target="#create">
                <i class="fa fa-plus"></i>
            </button>
            <!-- Modal -->
            <div class="modal fade" id="create" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"><i class="fa fa-plus"></i> Tambah data strom</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <form action="{{ route('strom.store') }}" method="POST">
                            @csrf
                            <div class="modal-body">
                                <div class="form-group row">
                                    <label for="cost" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah pembayaran') }}</label>

                                    <div class="col-md-8">
                                        <input id="cost" type="text" class="form-control{{ $errors->has('cost') ? ' is-invalid' : '' }}" name="cost" required>

                                        @if ($errors->has('cost'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('cost') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>

                                <div class="form-group row">
                                    <label for="strom_result" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah strom') }}</label>

                                    <div class="col-md-8">
                                        <input id="strom_result" type="text" class="form-control{{ $errors->has('strom_result') ? ' is-invalid' : '' }}" name="strom_result" required>

                                        @if ($errors->has('strom_result'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('strom_result') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                <button type="submit" name="submit" value="Simpan" class="btn btn-primary btn-sm"><i class="fa fa-save"></i></button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <table id="datatables" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Jumlah Pembayaran</th>
                        <th scope="col">Jumlah Strom</th>
                        <th scope="col">Aksi</th>
                    </tr>
                </thead>      
                <tbody>
                    @if(count($stroms))
                        @foreach ($stroms as $strom)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>Rp. {{ $strom->jumlah_pembayaran }}</td>
                                <td>{{ $strom->jumlah_strom }} kWH</td>
                                <td>
                                    {{-- Edit --}}
                                    <button type="button" class="btn btn-primary btn-sm mr-1" data-toggle="modal" data-target="#updateModal{{$strom->id_strom}}"><i class="fa fa-edit"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="updateModal{{$strom->id_strom}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                <h5 class="modal-title" id="exampleModalCenterTitle"><i class="fa fa-edit"></i> Ubah data pelanggan</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                                </div>
                                                <form method="POST" action="{{ route('strom.update',$strom->id_strom) }}">
                                                    @csrf
                                                    {{method_field('PUT')}}
                                                    <div class="modal-body">
                                                        <div class="form-group row">
                                                            <label for="cost" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah pembayaran') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="cost" type="text" class="form-control{{ $errors->has('cost') ? ' is-invalid' : '' }}" name="cost" value="{{ $strom->jumlah_pembayaran }}" required>
                        
                                                                @if ($errors->has('name'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('name') }}</strong>
                                                                    </span>
                                                                @endif
                                                            </div>
                                                        </div>
                                                    
                                                        <div class="form-group row">
                                                            <label for="strom_result" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah strom') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="strom_result" type="text" class="form-control{{ $errors->has('strom_result') ? ' is-invalid' : '' }}" name="strom_result" value="{{ $strom->jumlah_strom }}" required>
                        
                                                                @if ($errors->has('strom_result'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('strom_result') }}</strong>
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
                                    <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal{{$strom->id_strom}}"><i class="fa fa-times"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="deleteModal{{ $strom->id_strom }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" id="exampleModalLongTitle"><i class="fa fa-times text-danger"></i> Konfirmasi</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                        <span aria-hidden="true">&times;</span>
                                                    </button>
                                                </div>
                                                <div class="modal-body">
                                                    <p>Apakah Anda yakin menghapus jumlah pembayaran <b>{{$strom->jumlah_pembayaran}}</b></p>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                    <form class="form group" action="{{ route('strom.destroy',$strom->id_strom) }}" method="POST">
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