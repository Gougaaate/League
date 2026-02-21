import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import correlate

def findDelay(t1, data1, t2, data2):

    t_min = max(t1.min(), t2.min())     # common time range
    t_max = min(t1.max(), t2.max())

    dt = min(np.median(np.diff(t1)), np.median(np.diff(t2)))   # temporary uniform grid
    t_common = np.arange(t_min, t_max, dt)

    f1 = interp1d(t1, data1, kind='linear', fill_value="extrapolate")
    f2 = interp1d(t2, data2, kind='linear', fill_value="extrapolate")

    data1_i = f1(t_common)
    data2_i = f2(t_common)

    d1 = data1_i - np.mean(data1_i)   # need to remove mean
    d2 = data2_i - np.mean(data2_i)

    corr = correlate(d1, d2, mode='full')
    lags = np.arange(-len(d1)+1, len(d1))

    best_lag = lags[np.argmax(corr)]

    delay = best_lag * dt

    return delay

if __name__ == "__main__":
    # create test data
    t1 = np.linspace(0.1, 10.8, 224)
    t2 = np.linspace(1.4, 13, 111)

    data1 = np.sin(2*np.pi*t1 +1)
    data2 = np.sin(2*np.pi*(t2+0.4) +1)

