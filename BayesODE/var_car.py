"""
.. module:: var_car

Variance function for the CAR(p) process:

.. math:: var(X_t)

"""

import numpy as np
import BayesODE._mou_car as mc

def var_car(tseq, roots, sigma=1.):
    """Computes the variance function for the CAR(p) process :math: `var(X_t)`
    
    Parameters
    ----------
    
    tseq: [N] :obj:`numpy.ndarray` of float
        Time points at which :math: `x_t` is evaluated. 
    roots: [p] :obj:`numpy.ndarray` of float
        Roots to the p-th order polynomial of the car(p) process (roots must be negative)
    sigma: float
        Parameter in mOU volatility matrix

    Returns
    -------
    
    V: [N, p, p]  numpy.ndarray
        Evaluates :math:`var(X_t)`.
    """
    p = len(roots)
    delta = np.array(-roots)
    Sigma_tilde, Q = mc._mou_car(roots, sigma)

    V = np.zeros((len(tseq), p, p))
    for t in range(len(tseq)):
        V_tilde = np.zeros((p, p))
        for i in range(p):
            for j in range(i, p):
                V_tilde[i, j] = Sigma_tilde[i, j] / (delta[i] + delta[j]) * (
                    1.0 - np.exp(- (delta[i] + delta[j]) * tseq[t]))  # V_tilde
                V_tilde[j, i] = V_tilde[i, j]

        V[t] = np.linalg.multi_dot([Q, V_tilde, Q.T])  # V_deltat

    return V
