
import netCDF4 as nc

# FIXME: these are really just copies of the forcing_file input.

def create_mom_nudging_file(filename, var_name, var_longname,
                            var_units, start_date, forcing_file):

    ff = nc.Dataset(forcing_file)
    f = nc.Dataset(filename, 'w')

    f.createDimension('st_ocean', ff.dimensions['ZT'].size)
    f.createDimension('time')
    f.createDimension('xt_ocean', ff.dimensions['GRID_X_T'].size)
    f.createDimension('yt_ocean', ff.dimensions['GRID_Y_T'].size)

    zt = f.createVariable('st_ocean', 'f8', ('st_ocean'))
    zt.long_name = 'tcell zstar depth'
    zt.units = 'meters'
    zt.cartesian_axis = 'Z'
    zt.positivne = 'down'
    zt[:] = ff.variables['ZT'][:]

    lats = f.createVariable('yt_ocean', 'f8', ('yt_ocean'))
    lats.long_name = 'tcell latitude'
    lats.units = 'degree_N'
    lats.cartesian_axis = 'Y'
    lats[:] = ff.variables['GRID_Y_T'][:]

    lons = f.createVariable('xt_ocean', 'f8', ('xt_ocean'))
    lons.long_name = 'tcell longitude'
    lons.units = 'degree_E'
    lons.cartesian_axis = 'X'
    lons[:] = ff.variables['GRID_X_T'][:]

    time = f.createVariable('time', 'f8', ('time'))
    time.long_name = 'time'
    time.units = "days since {}-{}-{} 00:00:00".format(str(start_date.year).zfill(4),
                                                       str(start_date.month).zfill(2),
                                                       str(start_date.day).zfill(2))
    time.cartesian_axis = "T"
    time.calendar_type = "GREGORIAN"
    time.calendar = "GREGORIAN"

    var = f.createVariable(var_name, 'f8',
                           ('time', 'st_ocean', 'yt_ocean', 'xt_ocean'),
                           fill_value=-1.e+34)
    var.missing_value = -1.e+34
    var.long_name = var_longname
    var.units = var_units

    ff.close()
    f.close()


def create_nemo_nudging_file(filename, var_name, var_longname,
                              var_units, start_date, forcing_file):

    ff = nc.Dataset(forcing_file)
    f = nc.Dataset(filename, 'w')

    f.createDimension('y', ff.variables['nav_lon'].shape[0])
    f.createDimension('x', ff.variables['nav_lon'].shape[1])
    f.createDimension('z', ff.variables['depth'].size)
    f.createDimension('time_counter')

    lats = f.createVariable('nav_lat', 'f8', ('y', 'x'))
    lats[:] = ff.variables['nav_lat'][:]

    lons = f.createVariable('nav_lon', 'f8', ('y', 'x'))
    lons[:] = ff.variables['nav_lon'][:]

    depth = f.createVariable('depth', 'f8', ('z'))
    depth[:] = ff.variables['depth'][:]

    time = f.createVariable('time_counter', 'f8', ('time_counter'))
    time.long_name = 'time'
    time.units = "days since {}-{}-{} 00:00:00".format(str(start_date.year).zfill(4),
                                                       str(start_date.month).zfill(2),
                                                       str(start_date.day).zfill(2))
    time.cartesian_axis = "T"

    var = f.createVariable(var_name, 'f8', ('time_counter', 'z', 'y', 'x'))
    var.long_name = var_longname
    var.units = var_units

    f.close()
