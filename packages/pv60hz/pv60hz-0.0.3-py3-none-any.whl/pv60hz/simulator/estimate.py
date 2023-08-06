# -*- coding: utf-8 -*-

from itertools import product
from multiprocessing.pool import Pool

import pandas as pd
import numpy as np
from pvlib.location import Location

from ..simulator.simulate import PVWattsV5


class AzimuthTiltEstimator(object):

    def __init__(self,
                 true_yield, weather,
                 latitude, longitude, altitude, albedo, capacity,
                 **kwargs):
        """__init__

        Parameters
        ----------

        true_yield : pd.Series
        weather : pd.DataFrame
        latitude : float
            - [-90, 90]
        longitude : float
            - [-180, 180]
        altitude : float
        albedo : float
            - [0, 1]
        capacity : float
            - plant capacity in kW
        **kwargs : passed to self.estimate_clearsky_curve

        Returns
        -------
        """

        assert isinstance(true_yield, pd.Series),\
            "true_yield is not a pd.Series object"
        assert isinstance(weather, pd.DataFrame),\
            "true_yield is not a pd.DataFrame object"
        assert 'temp_air' in weather,\
            "weather does not contain the 'temp_air' column"
        assert 'wind_speed' in weather,\
            "weather does not contain the 'wind_speed' column"

        loc = Location(latitude, longitude,
                       tz=weather.index.tz.zone, altitude=altitude)
        cs_irrads = loc.get_clearsky(weather.index)

        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude
        self._albedo = albedo
        self._capacity = capacity

        self._true_yield = self.estimate_clearsky_curve(true_yield, **kwargs)
        self._weather = weather[['temp_air', 'wind_speed']].join(cs_irrads)

    @staticmethod
    def estimate_clearsky_curve(values, window=15, min_periods=10,
                                center=True, closed='both', q=0.9):
        """estimate_clearsky_curve

        Parameters
        ----------

        values : pd.Series
        window : int
        min_periods : int
        center : bool
        closed : str
        q : float
            - calculates q-th quantile (q belongs to [0, 1])

        Returns
        -------
        cs_output : pd.Series
        """

        assert isinstance(values.index, pd.DatetimeIndex)

        resampled = values.resample('1h').asfreq().to_frame('out')
        resampled['hour'] = resampled.index.hour
        cs_output = resampled.groupby('hour').apply(
            lambda x: x.rolling(
                window, min_periods=min_periods,
                center=center, closed=closed).quantile(q)
        )
        cs_output.index = cs_output.index.droplevel(level='hour')
        cs_output = cs_output.loc[values.index]['out'].rename(values.name)

        return cs_output

    @staticmethod
    def get_param_grids(azimuth_range=[0, 360], num_azimuth=15,
                        tilt_range=[0, 90], num_tilt=10,
                        loss_range=[0, 0.2], num_loss=10):
        """get_param_grids

        Parameters
        ----------

        azimuth_range : list
        num_azimuth : int
        tilt_range : list
        num_tilt : int
        loss_range : list
        num_loss : int

        Returns
        -------
        grids : list
            [(azimuth1, tilt1, loss1),
             (azimuth2, tilt2, loss2),
             ...]
        """

        azimuth_range = np.sort(np.array(azimuth_range).clip(0, 360))
        tilt_range = np.sort(np.array(tilt_range).clip(0, 90))
        loss_range = np.sort(np.array(loss_range).clip(0, 1.))

        azimuth_grids = np.linspace(*azimuth_range, num_azimuth)
        tilt_grids = np.linspace(*tilt_range, num_tilt)
        loss_grids = np.linspace(*loss_range, num_loss)
        grids = list(product(azimuth_grids, tilt_grids, loss_grids))

        return grids

    def get_predict_yield(self, azimuth, tilt, loss):
        """get_predict_yield

        Parameters
        ----------

        azimuth : float
            - [0, 360]
        tilt : float
            - [0, 90]
        loss : float
            - [0, 1]

        Returns
        -------
        """

        simulator = PVWattsV5(
            self._latitude, self._longitude, altitude=self._altitude,
            capacity=self._capacity, albedo=self._albedo,
            surface_azimuth=azimuth, surface_tilt=tilt,
            losses_model='no_loss'
        )

        predict_yield = simulator(self._weather)
        predict_yield *= 1 - loss

        return predict_yield

    def _calc_loss(self, args):
        """_calc_loss

        Parameters
        ----------

        args : list or tuple
            - (azimuth, tilt, loss)

        Returns
        -------
        """

        azimuth, tilt, loss = args
        predict_yield = self.get_predict_yield(
            azimuth=azimuth, tilt=tilt, loss=loss
        )
        joined = pd.concat([self._true_yield, predict_yield], axis=1)
        error = (joined.true_yield - joined.predict_yield).abs().mean() /\
            self._capacity

        return error

    def __call__(self, grids=None, num_process=8):
        """__call__

        Parameters
        ----------

        grids : list
            - use the result of self.get_param_grids() if None
        num_process : int
            - the number of cpus for parallel computing

        Returns
        -------
        """

        if grids is None:
            grids = self.get_param_grids()

        p = Pool(num_process)
        losses = p.map(self._calc_loss, grids)
        p.close()

        data = pd.DataFrame(list(zip(*grids))).T
        data.columns = ['azimuth', 'tilt', 'loss']
        data['error'] = losses

        return data


if __name__ == '__main__':

    lat, lon = 33.306684945776105, 126.65711325387986
    capacity = 994.84

    true_yield = pd.read_pickle('examples/data/cs_curve/true_yield.pkl')
    cs_weather = pd.read_pickle('examples/data/cs_curve/cs_weather.pkl')

    estimator = AzimuthTiltEstimator(
        true_yield=true_yield['true_yield'],
        weather=cs_weather,
        latitude=lat, longitude=lon, altitude=0.,
        albedo=0.2, capacity=capacity,
    )
    result = estimator()

    print(result.head(30))
