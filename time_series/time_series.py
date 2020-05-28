import numpy as np
from scipy import signal


class TimeSeries(object):
    """A class for manipulating time series data"""
    def __init__(self, raw_data, sr, makePSD=False):
        self.raw_data = raw_data
        self.sr = sr
        self.dt = 1.0/self.sr
        self.T = len(raw_data)*self.dt  # total time in seconds
        self.times = np.linspace(0, self.T, len(self.raw_data))
        self.PSD = None  # power spectral density
        self.freqs = None
        if makePSD is True:
            self.freqs, self.PSD = signal.periodogram(self.raw_data, self.sr)

    def __len__(self):
        return len(self.raw_data)

    def __array__(self):
        return self.raw_data

    def __getitem__(self, i):
        return self.raw_data[i]


class Windows(TimeSeries):
    """Break up a time series into smaller windows"""
    def __init__(self, ts, win_T, overlap=0.5):
        self._timeSeries = ts
        self.win_len = win_T
        self.overlap = overlap
        self.dN = int(self.win_len/self._timeSeries.dt) # numer of points in a window
        self._windows = []
        i = 0
        while len(self._timeSeries)-i >= self.dN: # so long as we still have enough to add, keep adding. Note: this truncates the series
            window_ts = TimeSeries(self._timeSeries[i:i+self.dN],
                                   self._timeSeries.sr)
            # roll the times array to set individual window times
            window_ts.times = np.roll(self._timeSeries.times, -i)[:self.dN]
            self._windows.append(window_ts)
            i += int((1-self.overlap)*self.dN)

    def __len__(self):
        return len(self._windows)

    def __getitem__(self, tuple):
        i, j = tuple
        return (self._windows[i])[j]

    def getTimes(self, i):
        return self._windows[i].times
        # I = int((1-self.overlap)*self.dN)*i
        # return self._timeSeries.getTimes()[I:]

    def __array__(self):
        return np.array(self[:, :])



if __name__ == "__main__":
    import matplotlib.pyplot as plt

    t = np.linspace(0, 10, 1000)
    y = np.sin(2*np.pi*5*t)
    ts = TimeSeries(y, 1/(t[1]-t[0]), makePSD=True)

    w = Windows(ts, 0.25)

    print(np.shape(w))

    plt.figure()
    plt.plot(ts.times, ts, 'k--', lw=2, alpha=0.5)
    for i in range(len(w)):
        plt.plot(w.getTimes(i), w[i, :], alpha=0.5)

    plt.figure()
    plt.semilogy(ts.freqs, ts.PSD)
    plt.ylim([1e-7, 1e2])
    plt.show()
