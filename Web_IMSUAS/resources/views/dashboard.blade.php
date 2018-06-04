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
          <p><b>5</b></p>
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
  </div>
@endsection