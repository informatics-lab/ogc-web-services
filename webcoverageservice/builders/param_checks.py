"""
Module containing checker functions for user input when building a request.

"""
import dateutil.parser

def check_dim_forecast(dim_fcst):
    """
    Check the dim_forecast is valid format.

    """
    # Can this be improved? Is format always PT{number}{H/M/S}?
    if not isinstance(dim_fcst, str):
        raise ValueError("dim_forecast must be given as a string.")

def sort_grid_num(grid_num):
    """
    Check number grid points is valid integer like.

    """
    if not isinstance(grid_num, int):
        err = ValueError("width/height values must be integer like.")
        if isinstance(grid_num, str):
            try:
                grid_num = int(grid_num)
            except ValueError:
                raise err
        elif isinstance(grid_num, float):
            if grid_num % 1 != 0:
                raise err
            else:
                grid_num = int(grid_num)
        else:
            raise err
    return grid_num

def sort_grid_size(grid_size):
    """
    Check number grid points is valid format.

    """
    try:
        return float(grid_size)
    except ValueError:
        raise ValueError("resx/resy values must be float like.")

def sort_time(time):
    """
    Check time string is valid time format and return in ISO format.

    """
    try:
        # Returns a datetime object.
        dtime = dateutil.parser.parse(time, ignoretz=True)
    except ValueError, AttributeError:
        raise ValueError("Invalid time argument given: %s" % time)
    time_str = dtime.isoformat()
    if time_str[-1] != "Z":
        time_str += "Z"
    return time_str

def check_bbox(bbox):
    """
    Check bbox is valid.

    """
    if type(bbox) not in [list, tuple]:
        raise UserWarning("bbox argument must be a list.")
    if len(bbox) != 4:
        raise UserWarning("bbox must contain 4 values, %s found."\
                          % len(bbox))

    bbox_flts = []
    for val in bbox:
        try:
            bbox_flts.append(float(val))
        except:
            raise UserWarning("All bbox values must be numbers.")
    # Check min and max values are sensible.
    if bbox_flts[0] > bbox_flts[2] or bbox_flts[1] > bbox_flts[3]:
        raise UserWarning("bbox min value larger than max. Format must be"\
                          " [x-min, y-min, x-max, y-max]")


def sort_bbox(bbox):
    """
    Convert bbox into string format required for WCS request.

    """
    return ",".join([str(val) for val in bbox])
