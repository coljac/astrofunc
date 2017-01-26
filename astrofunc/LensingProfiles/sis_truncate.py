__author__ = 'sibirrer'

import numpy as np

class SIS_truncate(object):
    """
    this class contains the function and the derivatives of the Singular Isothermal Sphere
    """
    def function(self, x, y, phi_E_trunc, r_trunc, center_x_trunc=0, center_y_trunc=0):
        x_shift = x - center_x_trunc
        y_shift = y - center_y_trunc
        r = np.sqrt(x_shift*x_shift + y_shift*y_shift)
        if isinstance(r, int) or isinstance(r, float):
            if r < r_trunc:
                f_ = phi_E_trunc * r
            elif r < 2*r_trunc:
                f_ = phi_E_trunc * r_trunc + 1./2*phi_E_trunc*(3-r/r_trunc)*(r-r_trunc)
            else:
                f_ = 3./2 * phi_E_trunc*r_trunc
        else:
            f_ = np.zeros_like(r)
            f_[r < r_trunc] = phi_E_trunc * r[r < r_trunc]
            r_ = r[(r < 2*r_trunc) & (r > r_trunc)]
            f_[(r < 2*r_trunc) & (r > r_trunc)] = phi_E_trunc * r_trunc + 1./2*phi_E_trunc*(3-r_/r_trunc)*(r_-r_trunc)
            f_[r > 2*r_trunc] = 3./2 * phi_E_trunc*r_trunc
        return f_

    def derivatives(self, x, y, phi_E_trunc, r_trunc, center_x_trunc=0, center_y_trunc=0):
        """
        returns df/dx and df/dy of the function
        """
        x_shift = x - center_x_trunc
        y_shift = y - center_y_trunc

        dphi_dr = self._dphi_dr(x_shift, y_shift, phi_E_trunc, r_trunc)
        dr_dx, dr_dy = self._dr_dx(x_shift, y_shift)
        f_x = dphi_dr * dr_dx
        f_y = dphi_dr * dr_dy
        return f_x, f_y

    def hessian(self, x, y, phi_E_trunc, r_trunc, center_x_trunc=0, center_y_trunc=0):
        """
        returns Hessian matrix of function d^2f/dx^2, d^f/dy^2, d^2/dxdy
        """
        x_shift = x - center_x_trunc
        y_shift = y - center_y_trunc
        dphi_dr = self._dphi_dr(x_shift, y_shift, phi_E_trunc, r_trunc)
        d2phi_dr2 = self._d2phi_dr2(x_shift, y_shift, phi_E_trunc, r_trunc)
        dr_dx, dr_dy = self._dr_dx(x, y)
        d2r_dx2, d2r_dy2, d2r_dxy = self._d2r_dx2(x_shift, y_shift)
        f_xx = d2r_dx2*dphi_dr + dr_dx**2*d2phi_dr2
        f_yy = d2r_dy2*dphi_dr + dr_dy**2*d2phi_dr2
        f_xy = d2r_dxy*dphi_dr + dr_dx*dr_dy*d2phi_dr2
        return f_xx, f_yy, f_xy

    def all(self, x, y, phi_E_trunc, r_trunc, center_x_trunc=0, center_y_trunc=0):
        """
        returns f,f_x,f_y,f_xx, f_yy, f_xy
        """
        x_shift = x - center_x_trunc
        y_shift = y - center_y_trunc
        r = np.sqrt(x_shift*x_shift + y_shift*y_shift)
        if isinstance(r, int) or isinstance(r, float):
            if r < r_trunc:
                f_ = phi_E_trunc * r
            elif r < 2*r_trunc:
                f_ = phi_E_trunc * r_trunc + 1./2*phi_E_trunc*(3-r/r_trunc)*(r-r_trunc)
            else:
                f_ = 3./2 * phi_E_trunc*r_trunc
        else:
            f_ = np.zeros_like(r)
            f_[r < r_trunc] = phi_E_trunc * r[r < r_trunc]
            r_ = r[(r < 2*r_trunc) & (r >= r_trunc)]
            f_[(r < 2*r_trunc) & (r >= r_trunc)] = phi_E_trunc * r_trunc + 1./2*phi_E_trunc*(3-r_/r_trunc)*(r_-r_trunc)
            f_[r >= 2*r_trunc] = 3./2 * phi_E_trunc*r_trunc

        dphi_dr = self._dphi_dr(x_shift, y_shift, phi_E_trunc, r_trunc)
        d2phi_dr2 = self._d2phi_dr2(x_shift, y_shift, phi_E_trunc, r_trunc)
        dr_dx, dr_dy = self._dr_dx(x, y)
        d2r_dx2, d2r_dy2, d2r_dxy = self._d2r_dx2(x_shift, y_shift)

        f_x = dphi_dr * dr_dx
        f_y = dphi_dr * dr_dy
        f_xx = d2r_dx2*dphi_dr + dr_dx**2*d2phi_dr2
        f_yy = d2r_dy2*dphi_dr + dr_dy**2*d2phi_dr2
        f_xy = d2r_dxy*dphi_dr + dr_dx*dr_dy*d2phi_dr2
        return f_, f_x, f_y, f_xx, f_yy, f_xy

    def _dphi_dr(self, x, y, phi_E_trunc, r_trunc):
        """

        :param x:
        :param y:
        :param r_trunc:
        :return:
        """
        r = np.sqrt(x*x + y*y)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                a = 0
            elif r < r_trunc:
                a = phi_E_trunc
            elif r < 2*r_trunc:
                a = phi_E_trunc * (2-r/r_trunc)
            else:
                a = 0
        else:
            a = np.zeros_like(r)
            a[(r < r_trunc) & (r > 0)] = phi_E_trunc
            r_ = r[(r < 2*r_trunc) & (r >= r_trunc)]
            a[(r < 2*r_trunc) & (r >= r_trunc)] = phi_E_trunc * (2-r_/r_trunc)
            a[r >= 2*r_trunc] = 0
        return a

    def _d2phi_dr2(self, x, y, phi_E_trunc, r_trunc):
        """
        second derivative of the potential in radial direction
        :param x:
        :param y:
        :param phi_E_trunc:
        :param r_trunc:
        :return:
        """
        r = np.sqrt(x*x + y*y)
        if isinstance(r, int) or isinstance(r, float):
            if r < r_trunc:
                a = 0
            elif r < 2*r_trunc:
                a = -phi_E_trunc/r_trunc
            else:
                a = 0
        else:
            a = np.zeros_like(r)
            a[r < r_trunc] = 0
            a[(r < 2*r_trunc) & (r > r_trunc)] = -phi_E_trunc/r_trunc
            a[r > 2*r_trunc] = 0
        return a

    def _dr_dx(self, x, y):
        """
        derivative of dr/dx, dr/dy
        :param x:
        :param y:
        :return:
        """

        r = np.sqrt(x**2 + y**2)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                r = 1
        else:
             r[r == 0] = 1
        return x/r, y/r

    def _d2r_dx2(self, x, y):
        """
        second derivative
        :param x:
        :param y:
        :return:
        """
        r = np.sqrt(x**2 + y**2)
        if isinstance(r, int) or isinstance(r, float):
            if r == 0:
                r = 1
        else:
             r[r == 0] = 1
        return y**2/r**3, x**2/r**3, -x*y/r**3