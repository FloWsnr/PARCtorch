from PARCtorch.integrator.numintegrator import NumericalIntegrator


class RK4(NumericalIntegrator):
    def __init__(self, **kwarg):
        super(RK4, self).__init__(**kwarg)

    def forward(self, f, current, step_size):
        """
        RK4 integration. Fixed step, 4th order.

        Parameters
        ----------
        f: function, the function that returns time deriviative
        current: tensor, the current state and velocity variables
        step_size: float, integration step size

        Returns
        -------
        final_state: tensor with the same shape of ```current```, the next state and velocity varaibles
        update: tensor with the same shape of ```current```, the update in this step
        """
        # Compute k1
        k1 = f(current)
        # Compute k2
        inp_k2 = current + step_size * 1 / 2 * k1
        k2 = f(inp_k2)
        # Compute k3
        inp_k3 = current + step_size * 1 / 2 * k2
        k3 = f(inp_k3)
        # Compute k4
        inp_k4 = current + step_size * k3
        k4 = f(inp_k4)
        # Final
        update = 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        final_state = current + step_size * update
        return final_state, update
