import unittest
import numpy as np
from plots import plots


def test_generate_normal_data_works_with_x_min_lower_than_10_():
    x, y = plots.generate_normal_data(0, 1)

    assert x[0] == -10

def test_generate_normal_data_works_with_x_min_bigger_than_10_():
    x, y = plots.generate_normal_data(0, 3)

    assert x[0] == -12

def test_generate_normal_data_works_with_x_max_lower_than_10_():
    x, y = plots.generate_normal_data(0, 1)

    assert x[-1] == 10

def test_generate_normal_data_works_with_x_max_bigger_than_10_():
    x, y = plots.generate_normal_data(0, 3)

    assert x[-1] == 12

def test_generate_binomial_data_return_right_x_lower_range():
    x, y = plots.generate_binomial_data(5,0.2)

    assert x[0] == 0
    
def test_generate_binomial_data_return_right_x_upper_range():
    x, y = plots.generate_binomial_data(5,0.2)

    assert x[-1] == 5

def test_generate_binomial_data_return_right_y_lower_range():
    x, y = plots.generate_binomial_data(5,0.2)

    assert np.isclose(y[0], 0.32768, atol=1e-5)

def test_generate_binomial_data_return_right_y_upper_range():
    x, y = plots.generate_binomial_data(5,0.2)

    assert np.isclose(y[-1], 0.00032, atol=1e-5)

def test_generate_poisson_data_return_right_x_lower_range():
    x, y = plots.generate_poisson_data(3)

    assert x[0] == 0

def test_generate_poisson_data_return_right_x_upper_range():
    x, y = plots.generate_poisson_data(3)

    assert x[-1] == 14

def test_generate_poisson_data_return_right_y_lower_range():
    x, y = plots.generate_poisson_data(3)

    assert np.isclose(y[0], 0.04979, atol=1e-5)

def test_generate_poisson_data_return_right_y_upper_range():
    x, y = plots.generate_poisson_data(3)

    assert np.isclose(y[-1], 0.00000, atol=1e-5)
