__author__ = 'sibirrer'

import numpy as np

class NoLens(object):
    """
    this is the trivial mapping without deflecting anything
    """
    def function(self, x, y):
        return np.zeros_like(x)

    def derivatives(self, x, y):
        f_x = np.zeros_like(x)
        f_y = np.zeros_like(x)
        return f_x, f_y

    def hessian(self, x, y):
        f_xx = np.zeros_like(x)
        f_yy = np.zeros_like(x)
        f_xy = np.zeros_like(x)
        return f_xx, f_yy, f_xy

    def all(self, x, y):
        f_ = np.zeros_like(x)
        f_x = np.zeros_like(x)
        f_y = np.zeros_like(x)
        f_xx = np.zeros_like(x)
        f_yy = np.zeros_like(x)
        f_xy = np.zeros_like(x)
        return f_, f_x, f_y, f_xx, f_yy, f_xy