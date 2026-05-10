
import numpy as np
from scipy.stats import norm, binom, poisson


def generate_normal_data(mean, std):
    """
    Generate x and y values for a normal distribution.
    """
    x_min = mean - max(4 * std, 10)
    x_max = mean + max(4 * std, 10)

    x = np.linspace(x_min, x_max, 400)
    y = norm.pdf(x, mean, std)

    return x, y

def generate_binomial_data(n, p):
    """
    Generate x and y values for a binomial distribution.
    """
    x = np.arange(0, n + 1)
    y = binom.pmf(x, n, p)

    return x, y

def generate_poisson_data(lam):
    """
    Generate x and y values for a Poisson distribution.
    """
    x = np.arange(0, max(15, int(lam * 3)))
    y = poisson.pmf(x, lam)

    return x, y

def build_distribution_parameters(distribution, dialog):
    """
    Extract parameter values from GUI inputs
    based on selected distribution.
    """
    if distribution == "Normal Distribution":
        return {
            "mean": dialog.mean_input.value(),
            "std_dev": dialog.std_input.value()
        }

    elif distribution == "Binomial Distribution":
        return {
            "n": dialog.n_input.value(),
            "p": dialog.p_input.value()
        }

    elif distribution == "Poisson Distribution":
        return {
            "lambda": dialog.lambda_input.value()
        }

    return {}

def apply_saved_plot_parameters(distribution_type, parameters, dialog):
    """
    Apply saved parameter values to GUI controls.
    """
    if distribution_type == "Normal Distribution":
        dialog.mean_input.setValue(parameters["mean"])
        dialog.std_input.setValue(parameters["std_dev"])

    elif distribution_type == "Binomial Distribution":
        dialog.n_input.setValue(parameters["n"])
        dialog.p_input.setValue(parameters["p"])

    elif distribution_type == "Poisson Distribution":
        dialog.lambda_input.setValue(parameters["lambda"])