@extends('layout')

@section('page_title')
    Pelanggan
@endsection

@section('active')
    active
@endsection

@section('active3')
    active
@endsection

@section('content')
    <div class="card card-body mb-4 wow fadeIn">
        <div class="table-responsive">
            <button type="button" class="btn btn-primary mb-3" data-toggle="modal" data-target="#create-team">
                <i class="fa fa-plus"></i>
            </button>
            <!-- Modal -->
            <div class="modal fade" id="create-team" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"><i class="fa fa-plus"></i> Tambah pelanggan</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <form action="{{ route('customer.store') }}" method="POST">
                            @csrf
                            <div class="modal-body">
                                <div class="form-group row">
                                    <label for="name" class="col-md-4 col-form-label text-md-left">{{ __('Nama pelanggan') }}</label>

                                    <div class="col-md-8">
                                        <input id="name" type="text" class="form-control" name="name">

                                        @if ($errors->has('name'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('name') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>

                                <div class="form-group row">
                                    <label for="address" class="col-md-4 col-form-label text-md-left">{{ __('Alamat') }}</label>

                                    <div class="col-md-8">
                                        <textarea name="address" id="address" class="form-control{{ $errors->has('address') ? ' is-invalid' : '' }}" required></textarea>

                                        @if ($errors->has('address'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('address') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>

                                <div class="form-group row">
                                    <label for="voltage" class="col-md-4 col-form-label text-md-left">{{ __('Tegangan meter') }}</label>

                                    <div class="col-md-8">
                                        <select name="voltage" class="custom-select">
                                            @foreach($meters as $meter)
                                                <option value="{{ $meter->id_meter }}">{{ $meter->tegangan_meter }}</option>
                                            @endforeach
                                        </select>

                                        @if ($errors->has('voltage'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('voltage') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>

                                <div class="form-group row">
                                    <label for="no_meter" class="col-md-4 col-form-label text-md-left">{{ __('No meter') }}</label>

                                    <div class="col-md-8">
                                        <input id="no_meter" type="text" class="form-control{{ $errors->has('no_meter') ? ' is-invalid' : '' }}" name="no_meter" required>

                                        @if ($errors->has('no_meter'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('no_meter') }}</strong>
                                            </span>
                                        @endif
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                <button type="submit" name="submit" value="Simpan" class="btn btn-primary"><i class="fa fa-save"></i></button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <table id="datatables" class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Nama pelanggan</th>
                        <th scope="col">Alamat</th>
                        <th scope="col">Tegangan meter</th>
                        <th scope="col">No meter</th>
                        <th scope="col">Waktu Pendaftaran</th>
                        <th scope="col">Aksi</th>
                    </tr>
                </thead>      
                <tbody>
                    @if(count($customers))
                        @foreach ($customers as $customer)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $customer->nama_pelanggan }}</td>
                                <td>{{ $customer->alamat }}</td>
                                <td>{{ $customer->tegangan_meter }}</td>
                                <td>{{ $customer->no_meter }}</td>
                                <td>{{ $customer->waktu_pendaftaran }}</td>
                                <td>
                                    <center>
                                        {{-- Edit --}}
                                        <button type="button" class="btn btn-primary mr-1" data-toggle="modal" data-target="#updateModal{{$customer->id_pelanggan}}"><i class="fa fa-edit"></i></button>
                                        <!-- Modal -->
                                        <div class="modal fade" id="updateModal{{$customer->id_pelanggan}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                            <div class="modal-dialog modal-dialog-centered" role="document">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                    <h5 class="modal-title" id="exampleModalCenterTitle"><i class="fa fa-edit"></i> Ubah data pelanggan</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                        <span aria-hidden="true">&times;</span>
                                                    </button>
                                                    </div>
                                                    <form method="POST" action="{{ route('customer.update',$customer->id_pelanggan) }}">
                                                        @csrf
                                                        {{method_field('PUT')}}
                                                        <div class="modal-body">
                                                            <div class="form-group row">
                                                                <label for="name" class="col-md-4 col-form-label text-md-left">{{ __('Nama pelanggan') }}</label>
                            
                                                                <div class="col-md-8">
                                                                    <input id="name" type="text" class="form-control{{ $errors->has('name') ? ' is-invalid' : '' }}" name="name" value="{{ $customer->nama_pelanggan }}">
                            
                                                                    @if ($errors->has('name'))
                                                                        <span class="invalid-feedback">
                                                                            <strong>{{ $errors->first('name') }}</strong>
                                                                        </span>
                                                                    @endif
                                                                </div>
                                                            </div>
                            
                                                            <div class="form-group row">
                                                                <label for="address" class="col-md-4 col-form-label text-md-left">{{ __('Alamat') }}</label>
                            
                                                                <div class="col-md-8">
                                                                    <textarea name="address" id="address" class="form-control{{ $errors->has('address') ? ' is-invalid' : '' }}" required>{{ $customer->alamat }}</textarea>
                            
                                                                    @if ($errors->has('address'))
                                                                        <span class="invalid-feedback">
                                                                            <strong>{{ $errors->first('address') }}</strong>
                                                                        </span>
                                                                    @endif
                                                                </div>
                                                            </div>
                            
                                                            <div class="form-group row">
                                                                <label for="voltage" class="col-md-4 col-form-label text-md-left">{{ __('Tegangan meter') }}</label>
                            
                                                                <div class="col-md-8">
                                                                    <select name="voltage" class="custom-select">
                                                                        @foreach($meters as $meter)
                                                                            <option @if($customer->id_meter == $meter->id_meter) selected @endif value="{{$meter->id_meter}}">{{$meter->tegangan_meter}}</option>
                                                                        @endforeach
                                                                    </select>
                            
                                                                    @if ($errors->has('voltage'))
                                                                        <span class="invalid-feedback">
                                                                            <strong>{{ $errors->first('voltage') }}</strong>
                                                                        </span>
                                                                    @endif
                                                                </div>
                                                            </div>
                            
                                                            <div class="form-group row">
                                                                <label for="no_meter" class="col-md-4 col-form-label text-md-left">{{ __('No meter') }}</label>
                            
                                                                <div class="col-md-8">
                                                                    <input id="no_meter" type="text" class="form-control{{ $errors->has('no_meter') ? ' is-invalid' : '' }}" name="no_meter" value="{{ $customer->no_meter }}" required>
                            
                                                                    @if ($errors->has('no_meter'))
                                                                        <span class="invalid-feedback">
                                                                            <strong>{{ $errors->first('no_meter') }}</strong>
                                                                        </span>
                                                                    @endif
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                            <button type="submit" class="btn btn-primary"><i class="fa fa-save"></i></button>
                                                        </div>
                                                    </form>
                                                </div>
                                            </div>
                                        </div>

                                        {{-- Delete --}}
                                        <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#deleteModal{{$customer->id_pelanggan}}"><i class="fa fa-times"></i></button>
                                        <!-- Modal -->
                                        <div class="modal fade" id="deleteModal{{ $customer->id_pelanggan }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                            <div class="modal-dialog modal-dialog-centered" role="document">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title" id="exampleModalLongTitle"><i class="fa fa-times text-danger"></i> Konfirmasi</h5>
                                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                            <span aria-hidden="true">&times;</span>
                                                        </button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <p>Apakah Anda yakin menghapus pelanggan <b>{{$customer->nama_pelanggan}}</b></p>
                                                    </div>
                                                    <div class="modal-footer">
                                                        <button type="button" class="btn btn-secondary" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                        <form class="form group" action="{{ route('customer.destroy',$customer->id_pelanggan) }}" method="POST">
                                                            @csrf
                                                            {{method_field('DELETE')}}
                                                            <button style="border-radius: 0px" type="submit" class="btn btn-danger"><i class="fa fa-trash"></i></button>
                                                        </form>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </center>
                                </td>
                            </tr>
                        @endforeach
                    @endif
                </tbody>
            </table>
        </div>
    </div>
@endsection