@extends('layout')

@section('page_title')
    Dashboard
@endsection

@section('active1')
    active
@endsection

@section('content')
  <div class="row">
    <div class="col-md-6 col-lg-3">
      <div class="widget-small primary coloured-icon"><i class="icon fa fa-users fa-3x"></i>
        <div class="info">
          <h4>Users</h4>
          <p><b>{{ $sum_customers }}</b></p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-lg-3">
      <div class="widget-small info coloured-icon"><i class="icon fa fa-thumbs-o-up fa-3x"></i>
        <div class="info">
          <h4>Likes</h4>
          <p><b>25</b></p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-lg-3">
      <div class="widget-small warning coloured-icon"><i class="icon fa fa-files-o fa-3x"></i>
        <div class="info">
          <h4>Uploades</h4>
          <p><b>10</b></p>
        </div>
      </div>
    </div>
    <div class="col-md-6 col-lg-3">
      <div class="widget-small danger coloured-icon"><i class="icon fa fa-star fa-3x"></i>
        <div class="info">
          <h4>Stars</h4>
          <p><b>500</b></p>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card-body">
      <div class="table-responsive">
        <table id="datatables" class="table table-hover">
            <thead>
              <tr>
                  <th scope="col">#</th>
                  <th scope="col">No_meter</th>
                  <th scope="col">Nama pelanggan</th>
                  <th scope="col">Alamat</th>
                  <th scope="col">Tegangan meter</th>
                  <th scope="col">Waktu Pendaftaran</th>
              </tr>
            </thead>      
            <tbody>
              @if (count($customers))
                @foreach ($customers as $customer)
                  <tr data-toggle="modal" data-target="#transaction{{ $customer->id_pelanggan }}" style="cursor:pointer">
                    <td>{{ $loop->iteration }}</td>
                    <td>{{ $customer->no_meter }}</td>
                    <td>{{ $customer->nama_pelanggan }}</td>
                    <td>{{ $customer->alamat }}</td>
                    <td>{{ $customer->tegangan_meter }} V</td>
                    <td>{{ $customer->waktu_pendaftaran }}</td>
										<!-- Modal Transaksi -->
										<div class="modal fade" id="transaction{{ $customer->id_pelanggan }}" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
												<div class="modal-dialog modal-dialog-centered" role="document">
														<div class="modal-content">
																<div class="modal-header">
																<h5 class="modal-title" id="exampleModalCenterTitle"><i class="fa fa-edit"></i> Transaksi baru</h5>
																<button type="button" class="close" data-dismiss="modal" aria-label="Close">
																		<span aria-hidden="true">&times;</span>
																</button>
																</div>
																<form method="POST" action="{{ route('dashboard.store') }}">
																		@csrf
																		<div class="modal-body">
																				<div class="form-group row">
																					<label for="no_meter" class="col-md-4 col-form-label text-md-left">{{ __('No meter') }}</label>
			
																					<div class="col-md-8">
																							<input id="no_meter" type="text" class="form-control{{ $errors->has('no_meter') ? ' is-invalid' : '' }}" name="no_meter" value="{{ $customer->no_meter }}" disabled>
			
																							@if ($errors->has('no_meter'))
																									<span class="invalid-feedback">
																											<strong>{{ $errors->first('no_meter') }}</strong>
																									</span>
																							@endif
																					</div>
																				</div>

																				<div class="form-group row">
																					<label for="name" class="col-md-4 col-form-label text-md-left">{{ __('Nama pelanggan') }}</label>
			
																					<div class="col-md-8">
																						@foreach ($names as $name)
																							@if ($customer->nama_pelanggan == $name->nama_pelanggan)
																								<input id="name" type="text" class="form-control{{ $errors->has('name') ? ' is-invalid' : '' }}" name="name" value="{{ $name->nama_pelanggan }}" disabled>	
																								<input type="hidden" name="nama" value="{{ $name->id_pelanggan }}">
																							@endif
																						@endforeach																			
																						@if ($errors->has('name'))
																							<span class="invalid-feedback">
																									<strong>{{ $errors->first('name') }}</strong>
																							</span>
																						@endif
																					</div>
																				</div>   
																				
																				<div class="form-group row">
																					<label for="no_token" class="col-md-4 col-form-label text-md-left">{{ __('No token') }}</label>
			
																					<div class="col-md-8">
																							<input id="no_token" type="text" class="form-control{{ $errors->has('no_token') ? ' is-invalid' : '' }}" name="no_token" required>
			
																							@if ($errors->has('no_token'))
																								<span class="invalid-feedback">
																										<strong>{{ $errors->first('no_token') }}</strong>
																								</span>
																							@endif
																					</div>
																				</div>    

																				<div class="form-group row">
																						<label for="voltage" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah strom') }}</label>
				
																						<div class="col-md-8">
																								<select id="select" name="voltage" class="custom-select">
																										@foreach($stroms as $strom)
																												<option value="{{$strom->id_strom}}">{{$strom->jumlah_strom}} kWH</option>
																												<input type="hidden" name="jumlah_strom" value="{{ $strom->jumlah_strom }}">
																												<input type="hidden" name="jumlah_pembayaran" value="{{ $strom->jumlah_pembayaran }}">
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
																					<label for="jml_pembayaran" class="col-md-4 col-form-label text-md-left">{{ __('Jumlah pembayaran') }}</label>
			
																					<div class="col-md-8">
																							<input id="jml_pembayaran" type="text" class="form-control{{ $errors->has('jml_pembayaran') ? ' is-invalid' : '' }}" name="jml_pembayaran" disabled>
			
																							@if ($errors->has('jml_pembayaran'))
																								<span class="invalid-feedback">
																										<strong>{{ $errors->first('no_token') }}</strong>
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
                  </tr>
                @endforeach
              @endif
            </tbody>
        </table>
      </div>
    </div>
  </div>
@endsection

@section('script')

@endsection