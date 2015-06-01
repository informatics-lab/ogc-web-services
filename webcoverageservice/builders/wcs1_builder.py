"""
Build appropriate requests for WCS1 requests.

"""
from webcoverageservice.builders.param_checks import Checks

def build_getCapabilities_req():
    return {"REQUEST" : "GetCapabilities"}

def build_describeCoverage_req(coverage_id):
    return {"REQUEST"  : "DescribeCoverage",
            "COVERAGE" : coverage_id}

def build_getCoverage_req(coverage_id, format=None, crs=None, elevation=None,
                          bbox=None, dim_run=None, time=None,
                          dim_forecast=None, width=None, height=None,
                          resx=None, resy=None, interpolation=None):
    """
    Create a dictionary of valid parameters for getCoverage method.

    Notes:

    When specifing times; dim_run, time and dim_forecast cannot all be given
    (even if they fit). Only a maximum of two can be specified.

    When specifying resolutions, width and height specify how many grid boxes
    are returned, the size of the boxes is consequential. resx and resy specify
    the size of the grid boxes and the number of grid boxes is consequential.
    They can not be used together (even if the fit).

    This function does not verify if the given parameters are available, it
    only asserts correct formats.

    Args:

    * coverage_id: string
        Name of the coverage.

    Kwargs:

    * format: string
        The format for the data to be returned in, e.g. NetCDF3

    * crs: string
        The coordinate reference system, e.g. EPSG:4326

    * elevation: string
        The veritcal level description.

    * bbox: list
        Must contain 4 values in the format [x-min, y-min, x-max, y-max].
        Values can be given as integers, floats or strings. Default is the
        entire field is returned.

    * dim_run: string (date string)
        The model run time. This can be specified using most convential
        date descriptions e.g. 1/2/2015 or 2015-02-01 or 1st January 2015.
        Default is the latest run (unless time AND dim_forecast are given).

    * time: string (date string, see dim_run)
        The forecast time. Default is the first forecast time from the
        dim_run (unless dim_run AND dim_forecast are given).

    * dim_forecast: string
        The time releative to the dim_run e.g. PT36H is 36 hours from the
        model run time. Default is PT0H (unless dim_run AND time are
        given).

    * width/height: integer
        The number of gridpoints in the x (width) and y (height) within
        the bounding box. Interpolation is used.

    * resx/resy: float
        The size of a gridpoint in the x/y direction. This is an
        alternative method to specifing the width/height. Interpolation is
        used.

    * interpolation: string
        The interpolation method used if data is re-gridded.

    returns:
        dictionary

    """
    checker = Checks()
    param_dict  = {"REQUEST"  : "GetCoverage",
                   "COVERAGE" : coverage_id}

    if format:
        param_dict["FORMAT"] = format

    if crs:
        param_dict["CRS"] = crs

    if elevation:
        param_dict["ELEVATION"] = elevation

    if bbox:
        checker.check_bbox(bbox)
        bbox_str = checker.sort_bbox(bbox)
        param_dict["BBOX"] = bbox_str

    # Time parameters.
    if dim_run and time and dim_forecast:
        raise UserWarning("Cannot use more than 2 of dim_run, "\
                          "dim_forecast or time parameters together.")
    if dim_run:
        dim_run = checker.sort_time(dim_run)
        param_dict["DIM_RUN"] = dim_run
    if time:
        time = checker.sort_time(time)
        param_dict["TIME"] = time
    if dim_forecast:
        checker.check_dim_forecast(dim_forecast)
        param_dict["DIM_FORECAST"] = dim_forecast

    # Resolution parameters.
    if width and resx:
        raise UserWarning("Cannot specify width and resx together; one "\
                          "implies the other.")
    if width:
        width = checker.sort_grid_num(width)
        param_dict["WIDTH"] = width
    if resx:
        resx = checker.sort_grid_size(resx)
        param_dict["RESX"] = resx

    if height and resy:
        raise UserWarning("Cannot specify height and resy together; one "\
                          "implies the other.")
    if height:
        height = checker.sort_grid_num(height)
        param_dict["HEIGHT"] = height
    if resy:
        resy = checker.sort_grid_size(resy)
        param_dict["RESY"] = resy

    if interpolation:
        param_dict["INTERPOLATION"] = interpolation

    return param_dict
