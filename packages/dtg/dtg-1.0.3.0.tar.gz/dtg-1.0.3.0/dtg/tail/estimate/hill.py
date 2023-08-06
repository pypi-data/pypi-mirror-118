import numpy as np
import numba as nb

from dtg.tail.estimate.estimator import TailEstimator
from dtg.tail.estimate.jackknife import JackknifeEstimator
from dtg.tail.estimate.vries import DeVriesEstimator


class HillEstimator(TailEstimator):
    @staticmethod
    @nb.njit(fastmath=True)
    def estimate(x, k):
        return np.mean(np.log(x[-k - 1:])) - np.log(x[-k - 2])

    @staticmethod
    def check(ex):
        if np.sum(np.isnan(ex)) + np.sum(np.isinf(ex)) > 0:
            return False
        if ex <= 0:
            return False
        return True

    @staticmethod
    def AMSEE(x, tau=None):
        ks, smpl = np.arange(0, x.size - 1), []

        if tau is None:
            ro = -1
        else:
            ro = -1  # todo
        alls = [HillEstimator.estimate(x, k) for k in ks]
        bi = {str(k+1)+"-"+str(K+1): np.mean(alls[k: K+1]) - np.mean(alls[:K+1]) for K in ks for k in np.arange(K+1)}
        des = [DeVriesEstimator.estimate(x, k) for k in ks]

        ads = [np.mean([(des[k] - alls[k] + (bi[str(k+1)+"-"+str(K+1)]/dls((k+1)/(K+1), ro))) ** 2
                        for k in np.arange(K + 1)]) for K in ks]
        K = ks[2 + np.argmin([np.sum(
            [np.abs(((ads[K] - ads[K + i]) / i)) for i in [-2, -1, 1, 2]]) for K in np.arange(2, len(ads) - 2)]
        )]

        for i in ks:
            if ks[i] > K:
                break

            smpl.append((JackknifeEstimator.estimate(x, ks[i]) ** 2 / ks[i]) +
                        (
                    (1 - ro) * ((((K + 1) / (ks[i] + 1)) - 1) / ((((ks[i] + 1) / (K + 1)) ** ro) - 1)) * bi[str(ks[i]+1)
                                                                                                            +"-"+str(K+1)]) ** 2)
        ind = np.argmin(smpl)
        return alls[ind], ind


def dls(x, ro):
    if x == 1:
        return 1

    return - (x ** ro - 1) / (ro * (x ** (-1) - 1))
