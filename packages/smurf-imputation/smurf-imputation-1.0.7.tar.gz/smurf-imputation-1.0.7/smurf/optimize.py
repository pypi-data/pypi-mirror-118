# _*_ coding: utf-8 _*_
"""
Time:     2021/7/22 17:34
Author:   WANG Bingchen
Version:  V 0.1
File:     optimize.py
Describe: 
"""


from scipy.special import psi
from numpy import log


def CVOptimize(A, G, H, u, Vg, Vc, v, g, c):
    DFG1 = (2 * u[g][c] / v[g][c]) * H[:, c] * log(u[g][c]) + u[g][c] * H[:, c] / v[g][c]
    DFG2 = -2 * u[g][c] * log(v[g][c]) * H[:, c] / v[g][c]
    DFG3 = -psi((u[g][c] ** 2) / v[g][c]) * 2 * u[g][c] * H[:, c] / v[g][c]
    DFG4 = psi(A[g][c] + ((u[g][c] ** 2) / v[g][c])) * 2 * u[g][c] * H[:, c] / v[g][c]
    DFG5 = -(2 * u[g][c] * H[:, c] / v[g][c]) * log(1 + u[g][c] / v[g][c]) - (
            A[g][c] + u[g][c] ** 2 / v[g][c]) * H[:, c] / (v[g][c] + u[g][c])
    DFG = DFG1 + DFG2 + DFG3 + DFG4 + DFG5

    DFH1 = (2 * u[g][c] / v[g][c]) * G[g, :] * log(u[g][c]) + u[g][c] * G[g, :] / v[g][c]
    DFH2 = -2 * u[g][c] * log(v[g][c]) * G[g, :] / v[g][c]
    DFH3 = -psi((u[g][c] ** 2) / v[g][c]) * 2 * u[g][c] * G[g, :] / v[g][c]
    DFH4 = psi(A[g][c] + u[g][c] ** 2 / v[g][c]) * 2 * u[g][c] * G[g, :] / v[g][c]
    DFH5 = -(2 * u[g][c] * G[g, :] / v[g][c]) * log(1 + u[g][c] / v[g][c]) - (
            A[g][c] + u[g][c] ** 2 / v[g][c]) * G[g, :] / (v[g][c] + u[g][c])
    DFH = DFH1 + DFH2 + DFH3 + DFH4 + DFH5

    DFVg1 = -(u[g][c] ** 2) * log(u[g][c]) / Vg[g][0] ** 2
    DFVg2 = (u[g][c] ** 2) * log(Vg[g][0]) / (Vg[g][0] ** 2) - (u[g][c] ** 2) / (Vg[g][0] ** 2)
    DFVg3 = psi((u[g][c] ** 2) / Vg[g][0]) * ((u[g][c] ** 2) / Vg[g][0] ** 2)
    DFVg4 = -psi(A[g][c] + u[g][c] ** 2 / Vg[g][0]) * ((u[g][c] ** 2) / Vg[g][0] ** 2)
    DFVg5 = ((u[g][c] ** 2) / (Vg[g][0] ** 2)) * log(1 + u[g][c] / Vg[g][0]) + (
            A[g][c] + u[g][c] ** 2 / Vg[g][0]) * (u[g][c] / (Vg[g][0] ** 2 + u[g][c] * Vg[g][0]))
    DFVg = DFVg1 + DFVg2 + DFVg3 + DFVg4 + DFVg5

    return DFG, DFH, DFVg


def FanoOptimize(A, G, H, u, bg, bc, b, g, c):
    DFG1 = -H[:, c] / b[g][c] * log(b[g][c])
    DFG2 = -psi(u[g][c] / b[g][c]) * H[:, c] / b[g][c]
    DFG3 = psi(A[g][c] + u[g][c] / b[g][c]) * H[:, c] / b[g][c]
    DFG4 = -(1 / b[g][c]) * log(1 + 1 / b[g][c]) * H[:, c]
    DFG = DFG1 + DFG2 + DFG3 + DFG4

    DFH1 = -G[g, :] / b[g][c] * log(b[g][c])
    DFH2 = -psi(u[g][c] / b[g][c]) * G[g][:] / b[g][c]
    DFH3 = psi(A[g][c] + u[g][c] / b[g][c]) * G[g][:] / b[g][c]
    DFH4 = -(1 / b[g][c]) * log(1 + 1 / b[g][c]) * G[g, :]
    DFH = DFH1 + DFH2 + DFH3 + DFH4

    DFBg1 = u[g][c] / (bg[g][0] ** 2) * (log(bg[g][0]) - 1)
    DFBg2 = psi(u[g][c] / bg[g][0]) * u[g][c] / (bg[g][0] ** 2)
    DFBg3 = -psi(A[g][c] + u[g][c] / bg[g][0]) * u[g][c] / (bg[g][0] ** 2)
    DFBg4 = -(u[g][c] * log(1 + 1 / bg[g][0]) / (bg[g][0] ** 2) + (A[g][c] * bg[g][0] + u[g][c]) / (
            (1 + bg[g][0]) * (bg[g][0] ** 2)))
    DFBg = DFBg1 + DFBg2 + DFBg3 + DFBg4

    return DFG, DFH, DFBg


def CCVOptimize(A, G, H, u, ag, ac, a, g, c):
    DFG1 = -H[:, c] / (a[g][c] * u[g][c])
    DFG2 = (A[g][c] + 1 / a[g][c]) * (H[:, c] / (u[g][c] * (a[g][c] * u[g][c] + 1)))
    DFG = DFG1 + DFG2

    DFH1 = -G[g, :] / (a[g][c] * u[g][c])
    DFH2 = (A[g][c] + 1 / a[g][c]) * (G[g, :] / (u[g][c] * (a[g][c] * u[g][c] + 1)))
    DFH = DFH1 + DFH2

    DFAg1 = (log(ag[g][0]) - 1) / (ag[g][0] ** 2)
    DFAg2 = log(u[g][c]) / (ag[g][0] ** 2)
    DFAg3 = psi(1 / ag[g][0]) / (ag[g][0] ** 2)
    DFAg4 = -psi(A[g][c] + (1 / ag[g][0])) / (ag[g][0] ** 2)
    DFAg5 = log(1 + 1 / (ag[g][0] * u[g][c])) / (ag[g][0] ** 2)
    DFAg6 = (A[g][c] + 1 / ag[g][0]) * (1 / (ag[g][0] * (u[g][c] ** 2 + 1)))
    DFAg = DFAg1 + DFAg2 + DFAg3 + DFAg4 + DFAg5 + DFAg6



    return DFG, DFH, DFAg