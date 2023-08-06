import arrow
from unittest.mock import patch
import datetime
import pytest
import pytz

from pv60hz.loader.gfs import GFSLoader
from pv60hz.exceptions import LatLonInvalidException

simul_date_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><title>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</title></head><body bgcolor="#ffffff"><h2 align=center>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</h2><h2 align=center>g2sub V1.1</h2><p>g2subset (grib2 subset)  allows you to subset (time, field, level, or region) a GRIB2 file and
sends you the result<br>&nbsp;<br><br><font color=red>Subdirectory</font><p><table border=0><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210831">gfs.20210831</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830">gfs.20210830</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210829">gfs.20210829</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210828">gfs.20210828</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210827">gfs.20210827</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210826">gfs.20210826</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210825">gfs.20210825</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210824">gfs.20210824</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210823">gfs.20210823</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210822">gfs.20210822</a></tr></table></form><br><font color=red>Select subdirectory from above list.</font><small> <p align=left><p align=left><small>g2sub 1.1.0.beta-6 and comments: Wesley.Ebisuzaki@noaa.gov, Jun.Wang@noaa.gov<br></small></body></html>
"""

simul_datetime_data = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html><head><title>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</title></head><body bgcolor="#ffffff"><h2 align=center>Data Transfer: NCEP GFS Forecasts (0.50 degree grid)</h2><h2 align=center>g2sub V1.1</h2><p>g2subset (grib2 subset)  allows you to subset (time, field, level, or region) a GRIB2 file and
sends you the result<br>&nbsp;<br><font color=red>Directory:&nbsp&nbsp&nbsp;</font>/gfs.20210830<br><br><font color=red>Subdirectory</font><p><table border=0><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F18">18</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F12">12</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F06">06</a></tr><tr><td>&nbsp&nbsp&nbsp;<a href="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p50.pl?dir=%2Fgfs.20210830%2F00">00</a></tr></table></form><br><font color=red>Select subdirectory from above list.</font><small> <p align=left><p align=left><small>g2sub 1.1.0.beta-6 and comments: Wesley.Ebisuzaki@noaa.gov, Jun.Wang@noaa.gov<br></small></body></html>
"""

simulate = [
    "2021083118",
    "2021083112",
    "2021083106",
    "2021083100",
    "2021083018",
    "2021083012",
    "2021083006",
    "2021083000",
    "2021082918",
    "2021082912",
    "2021082906",
    "2021082900",
    "2021082818",
    "2021082812",
    "2021082806",
    "2021082800",
    "2021082718",
    "2021082712",
    "2021082706",
    "2021082700",
    "2021082618",
    "2021082612",
    "2021082606",
    "2021082600",
    "2021082518",
    "2021082512",
    "2021082506",
    "2021082500",
    "2021082418",
    "2021082412",
    "2021082406",
    "2021082400",
    "2021082318",
    "2021082312",
    "2021082306",
    "2021082300",
    "2021082218",
    "2021082212",
    "2021082206",
    "2021082200",
]


def mock_get_html_page(*args, **kwargs):
    if "dir=" not in args[0]:
        return simul_date_data
    else:
        return simul_datetime_data


@patch("pv60hz.loader.gfs.GFSLoader.get_html_page")
def test_collect_simulate(mock_func):
    ins = GFSLoader()
    mock_func.side_effect = mock_get_html_page
    r = ins.refresh_simulation_time()
    assert len(r) == len(simulate)
    for i in range(len(simulate)):
        s = datetime.datetime.strptime(simulate[i], "%Y%m%d%H").replace(
            tzinfo=pytz.timezone("UTC")
        )
        assert s == r[i]


def test_latlon2grid():
    ins = GFSLoader()
    r = ins.latlon2grid(37.123, 126.598)
    assert r == ([105, 106], [253, 254])


def test_latlon2grid_invalid():
    ins = GFSLoader()
    with pytest.raises(LatLonInvalidException) as e_info:
        ins.latlon2grid(-999, -999)
