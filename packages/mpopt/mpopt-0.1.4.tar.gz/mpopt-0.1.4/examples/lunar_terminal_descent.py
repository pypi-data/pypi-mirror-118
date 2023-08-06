#
# Copyright (c) 2020 LA EPFL.
#
# This file is part of MPOPT
# (see http://github.com/mpopt).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
"""
Created: 11th April 2021
Author : Devakumar Thammisetty
"""
import numpy as np

try:
    from mpopt import mp
except ModuleNotFoundError:
    from context import mpopt
    from mpopt import mp

import casadi as ca

ocp = mp.OCP(n_states=5, n_controls=2)


def dynamics0(x, u, t):
    return [
        x[2],
        x[3],
        u[0] / x[4],
        u[1] / x[4] - 1.6,
        -ca.sqrt(u[0] ** 2 + u[1] ** 2) / (312 * 9.81),
    ]


ocp.dynamics[0] = dynamics0


def running_cost0(x, u, t):

    return u[0]


def terminal_cost0(xf, tf, x0, t0):
    return xf[4]


ocp.terminal_costs[0] = terminal_cost0


def terminal_constraints0(xf, tf, x0, t0):

    return [xf[0], xf[1], xf[2], xf[3]]


ocp.terminal_constraints[0] = terminal_constraints0


def path_constraints0(x, u, t):
    return [
        u[0] * u[0] + u[1] * u[1] - 3200 * 3200,
        -u[0] * u[0] - u[1] * u[1] + 1600 * 1600,
    ]


ocp.path_constraints[0] = path_constraints0

# ocp.tf0[0] = 1000.0
# ocp.x00[0] = [-735000.0, 30000.0, 1683.0, 0.0, 1732.0]
# ocp.lbx[0] = [-np.inf, 0.0, 0.0, -500.0, 700.0]
# ocp.ubx[0] = [0.0, 50000.0, 2000.0, 1000.0, 1732.0]
# ocp.lbu[0] = [-3200.0, -3200.0]
# ocp.ubu[0] = [3200.0, 3200.0]
# ocp.lbtf[0], ocp.ubtf[0] = 500, 1500.0

ocp.tf0[0] = 300.0
ocp.x00[0] = [-2000.0, 800.0, 350.0, -55.0, 1080.0]
ocp.lbx[0] = [-np.inf, 0.0, 0.0, -500.0, 700.0]
ocp.ubx[0] = [0.0, 50000.0, 2000.0, 1000.0, 1080.0]
ocp.lbu[0] = [-3200.0, -3200.0]
ocp.ubu[0] = [3200.0, 3200.0]
ocp.lbtf[0], ocp.ubtf[0] = 0, 1000.0

ocp.scale_x = np.array([1 / 700000.0, 1 / 30000.0, 1 / 1000.0, 1 / 1000.0, 1 / 1732.0])
ocp.scale_u = np.array([1 / 3200.0, 1 / 3200.0])
ocp.scale_t = 1 / 1000.0

ocp.validate()

if __name__ == "__main__":
    mpo = mp.mpopt(ocp, 4, 6)
    sol = mpo.solve()
    post = mpo.process_results(sol, plot=True)
    mp.plt.title(
        f"non-adaptive solution segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
    )

    # mpo = mp.mpopt_h_adaptive(ocp, 10, 4)
    # sol = mpo.solve(
    #     max_iter=3, mpopt_options={"method": "residual", "sub_method": "merge_split"}
    # )
    # post = mpo.process_results(sol, plot=True)
    # mp.plt.title(
    #     f"Adaptive solution: merge_split : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
    # )
    #
    # mpo = mp.mpopt_h_adaptive(ocp, 10, 4)
    # sol = mpo.solve(
    #     max_iter=2, mpopt_options={"method": "residual", "sub_method": "equal_area"}
    # )
    # post = mpo.process_results(sol, plot=True)
    # mp.plt.title(
    #     f"Adaptive solution: equal_residual : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
    # )
    #
    # mpo = mp.mpopt_h_adaptive(ocp, 5, 4)
    # sol = mpo.solve(
    #     max_iter=10, mpopt_options={"method": "control_slope", "sub_method": ""}
    # )
    # post = mpo.process_results(sol, plot=True)
    # mp.plt.title(
    #     f"Adaptive solution: Control slope : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
    # )
    #
    # mpo = mp.mpopt_adaptive(ocp, 3, 2)
    # mpo.lbh[0] = 1e-6
    # mpo.mid_residuals = True
    # sol = mpo.solve()
    # post = mpo.process_results(sol, plot=True)
    # mp.plt.title(
    #     f"Adaptive solution: Direct opt. : segments = {mpo.n_segments} poly={mpo.poly_orders[0]}"
    # )

    mp.plt.show()
