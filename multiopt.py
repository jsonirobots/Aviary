import openmdao.api as om
import matplotlib.pyplot as plt
import numpy as np


class Paraboloid(om.ExplicitComponent):
    """
    Evaluates the equation f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3.
    """

    def __init__(self, coeffs, i):
        super().__init__()
        self.coeffs = coeffs
        self.idx = i

    def setup(self):
        self.add_input('x', val=0.0)
        self.add_input('y', val=0.0)

        self.add_output(f"f{self.idx}", val=0.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials('*', '*', method='fd')

    def compute(self, inputs, outputs):
        """
        f(x,y) = (x-3)^2 + xy + (y+4)^2 - 3

        Minimum at: x = 6.6667; y = -7.3333
        """
        x = inputs['x']
        y = inputs['y']

        outputs[f"f{self.idx}"] = (
            x + self.coeffs[0])**2 + x * y + (y + self.coeffs[1])**2 + self.coeffs[0]


class Compound(om.Group):
    def __init__(self, weights, coeffs):
        super().__init__()
        self.weights = weights
        self.coeffs = coeffs

    def setup(self):
        cycle = self.add_subsystem('cycle', om.Group(), promotes=['*'])
        for i, coeff in enumerate(self.coeffs):
            cycle.add_subsystem(f"f{i}",
                                Paraboloid(coeff, i),
                                promotes_inputs=['x', 'y'],
                                promotes_outputs=[f"f{i}"])
        cycle.set_input_defaults('x', 0)
        cycle.set_input_defaults('y', 0)
        objstr = "+".join([f"{self.weights[i]}*f{i}" for i in range(len(self.weights))])
        proms = [f"f{i}" for i in range(len(self.weights))]
        self.add_subsystem(
            'obj_cmp', om.ExecComp("obj=" + objstr),
            promotes=['obj', *proms])


if __name__ == "__main__":

    prob = om.Problem()
    weights = [0.1, 0.2, 1]
    coeffs = [[-3, 4, -3], [1, -5, -1], [5, -5, 4]]

    prob.model = Compound(weights, coeffs)
    # prob.setup()
    # initxy = (3, 4)
    # prob.set_val('x', initxy[0])
    # prob.set_val('y', initxy[1])
    # prob.run_model()

    prob.driver = om.ScipyOptimizeDriver()
    prob.driver.options['optimizer'] = 'SLSQP'
    prob.driver.options['tol'] = 1e-8

    prob.model.add_design_var('x', lower=0, upper=10)
    prob.model.add_design_var('y', lower=0, upper=10)
    prob.model.add_objective('obj')

    prob.model.approx_totals()
    prob.setup()
    prob.set_solver_print(level=0)
    prob.run_driver()

    fs = []
    for i in range(len(weights)):
        fs.append(prob.get_val(f'f{i}'))
        print(f"f{i}: {fs[-1]}")
    objval = prob.get_val('obj')
    print(f"compound: {objval}")
    xopt, yopt = prob.get_val('x'), prob.get_val('y')

    # plotting stuff
    x = np.linspace(-10, 10, 20)
    y = np.linspace(-10, 10, 20)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(121, projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    funcs = []
    for i in range(len(weights)):
        func = (X + coeffs[i][0])**2 + np.multiply(X, Y) +\
               (Y + coeffs[i][1])**2 + coeffs[i][2]
        ax.plot_surface(X, Y, func, alpha=0.7)
        # ax.plot(xopt, yopt, fs[i], marker='o', markersize=5)
        funcs.append(func)
    ax.legend([f"f{i}" for i in range(len(weights))], loc='upper left')
    ax2.plot_surface(
        X, Y, sum([func * weight for (func, weight) in zip(funcs, weights)]),
        alpha=0.6)
    ax2.plot(xopt, yopt, objval, marker='*', markersize=10)

    plt.show()

    # build the model
    # prob = om.Problem()
    # prob.model.add_subsystem(
    #     'parab1', Paraboloid([-3, 4, -3]),
    #     promotes_inputs=['x', 'y'])
    # prob.model.add_subsystem(
    #     'parab2', Paraboloid([-5, 6, -1]),
    #     promotes_inputs=['x', 'y'])

    # # define the component whose output will be constrained
    # # prob.model.add_subsystem(
    # #     'const', om.ExecComp('g = x + y'),
    # #     promotes_inputs=['x', 'y'])

    # prob.model.add_subsystem()

    # # Design variables 'x' and 'y' span components, so we need to provide a common initial
    # # value for them.
    # prob.model.set_input_defaults('x', 3.0)
    # prob.model.set_input_defaults('y', -4.0)

    # # setup the optimization
    # prob.driver = om.ScipyOptimizeDriver()
    # prob.driver.options['optimizer'] = 'COBYLA'

    # prob.model.add_design_var('x', lower=-50, upper=50)
    # prob.model.add_design_var('y', lower=-50, upper=50)
    # prob.model.add_objective('parab2.f_xy')

    # # to add the constraint to the model
    # prob.model.add_constraint('const.g', lower=0, upper=10.)

    # prob.setup()
    # prob.run_driver()
