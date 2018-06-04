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
                        <form action="{{ route('meter.store') }}" method="POST">
                            @csrf
                            <div class="modal-body">
                                <div class="form-group row">
                                    <label for="voltage" class="col-md-4 col-form-label text-md-left">{{ __('Tegangan meter') }}</label>

                                    <div class="col-md-8">
                                        <input id="voltage" type="text" class="form-control{{ $errors->has('voltage') ? ' is-invalid' : '' }}" name="voltage" required>

                                        @if ($errors->has('voltage'))
                                            <span class="invalid-feedback">
                                                <strong>{{ $errors->first('voltage') }}</strong>
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
                        <th scope="col">Tegangan meter</th>
                        <th scope="col">Aksi</th>
                    </tr>
                </thead>      
                <tbody>
                    @if(count($meters))
                        @foreach ($meters as $meter)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $meter->tegangan_meter }} V</td>
                                <td>
                                    {{-- Edit --}}
                                    <button type="button" class="btn btn-primary btn-sm mr-1" data-toggle="modal" data-target="#updateModal{{$meter->id_meter}}"><i class="fa fa-edit"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="updateModal{{$meter->id_meter}}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                <h5 class="modal-title" id="exampleModalCenterTitle"><i class="fa fa-edit"></i> Ubah data meter</h5>
                                                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                    <span aria-hidden="true">&times;</span>
                                                </button>
                                                </div>
                                                <form method="POST" action="{{ route('meter.update',$meter->id_meter) }}">
                                                    @csrf
                                                    {{method_field('PUT')}}
                                                    <div class="modal-body">
                                                        <div class="form-group row">
                                                            <label for="voltage" class="col-md-4 col-form-label text-md-left">{{ __('Tegangan meter') }}</label>
                        
                                                            <div class="col-md-8">
                                                                <input id="voltage" type="text" class="form-control{{ $errors->has('voltage') ? ' is-invalid' : '' }}" name="voltage" value="{{ $meter->tegangan_meter }}" required>
                        
                                                                @if ($errors->has('voltage'))
                                                                    <span class="invalid-feedback">
                                                                        <strong>{{ $errors->first('voltage') }}</strong>
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
                                    <button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal{{$meter->id_meter}}"><i class="fa fa-times"></i></button>
                                    <!-- Modal -->
                                    <div class="modal fade" id="deleteModal{{ $meter->id_meter }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                                        <div class="modal-dialog modal-dialog-centered" role="document">
                                            <div class="modal-content">
                                                <div class="modal-header">
                                                    <h5 class="modal-title" id="exampleModalLongTitle"><i class="fa fa-times text-danger"></i> Konfirmasi</h5>
                                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                                        <span aria-hidden="true">&times;</span>
                                                    </button>
                                                </div>
                                                <div class="modal-body">
                                                    <p>Apakah Anda yakin menghapus jumlah pembayaran <b>{{$meter->tegangan_meter}}</b></p>
                                                </div>
                                                <div class="modal-footer">
                                                    <button type="button" class="btn btn-secondary btn-sm" data-dismiss="modal"><i class="fa fa-times"></i></button>
                                                    <form class="form group" action="{{ route('meter.destroy',$meter->id_meter) }}" method="POST">
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