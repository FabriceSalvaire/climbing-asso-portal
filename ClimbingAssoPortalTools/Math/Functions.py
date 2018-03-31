####################################################################################################
#
# Climbing Asso Portal - A Portal for Climbing Club (Association)
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

from math import exp, sqrt, log, pi, modf

####################################################################################################

SQRT_2_PI = sqrt(2.*pi)

####################################################################################################

def rint(f):
    return int(round(f))

def even(n):
    return n & 1 == 0

def odd(n):
    return n & 1 == 1

# Fixme: sign_of ?
def sign(x):
    return cmp(x, 0)

def middle(a, b):
    return .5 * (a + b)

def epsilon_float(a, b, epsilon = 1e-3):
    return abs(a-b) <= epsilon

def log2(x):
    return log(x)/log(2)

####################################################################################################

def trignometric_clamp(x):

    """ Clamp *x* in the range [-1.,1]. """

    if x > 1.:
        return 1.
    elif x < -1.:
        return -1.
    else:
        return x

####################################################################################################

def is_in_trignometric_range(x):
    return -1. <= x <= 1

####################################################################################################

def is_power_of_two(n):

    if n == 1 or n == 2:
        return True
    else:
        fractional_part, integer_part = modf(log2(n))
        return fractional_part == .0

####################################################################################################

# Prime Numbers : 2 3 5 7 11 13 ...

def is_prime(n):
    return not [x for x in xrange(2, int(sqrt(n)) + 1) if n%x == 0]

####################################################################################################

def number_of_bits(x):

    return rint(log(float(x))/log(2.))

####################################################################################################

def gaussian(x, parameters, index_integral, index_mean, index_sigma):

    #
    # g (x) = integral / (sigma * SQRT_2_PI) * exp (-.5 * ((x - mean)/sigma)^2)
    #
    # 1<exp>, 4 <*>, 2 </> and 1 <->
    #

    integral = parameters[index_integral]
    mean = parameters[index_mean]
    sigma = parameters[index_sigma]

    return integral / (sigma * SQRT_2_PI) * exp(-.5 * ((x - mean)/sigma)**2)

####################################################################################################

def gaussian_opt(x, parameters, index_normalisation, index_mean, index_inverse_sigma):

    #
    # g (x) = integral / (sigma * SQRT_2_PI) * exp (-.5 * ((x - mean)/sigma)^2)
    #
    # g_factorized (x) = normalisation * exp (-.5 * ((x - mean)*inverse_sigma)^2)
    #
    # 1<exp>, 4 <*> and 1 <->
    #

    normalisation = parameters[index_normalisation]
    mean = parameters[index_mean]
    inverse_sigma = parameters[index_inverse_sigma]

    return normalisation * exp(-.5 * ((x - mean)*inverse_sigma)**2)

####################################################################################################

class GaussianAndPol0:

    # Fixme:
    number_of_parameters = 4
    constant, integral, mean, sigma = range(number_of_parameters)

    def __call__(self, x, parameters):

        return (parameters[self.constant] +
                gaussian(x[0],
                         parameters,
                         self.integral, self.mean, self.sigma))

####################################################################################################

class GaussianOptAndPol0:

    # Fixme:
    number_of_parameters = 4
    constant, integral, mean, inverse_sigma = range(number_of_parameters)

    def __call__(self, x, parameters):

        return (parameters[self.constant] +
                gaussian_opt(x[0],
                             parameters,
                             self.integral, self.mean, self.inverse_sigma))

####################################################################################################

def compute_efficiency(numerator, denominator):

    numerator = float(numerator)
    denominator = float(denominator)

    if denominator != .0:
        efficiency = numerator / denominator
    else:
        efficiency = 0. # NAN

    if denominator != .0 and numerator != denominator:
        en = sqrt(numerator)
        ed = sqrt(denominator)
        # n2 = numerator**2
        d2 = denominator**2
        # e2 = efficiency**2
        en2 = en**2
        # ed2 = ed**2
        eed  = efficiency * ed
        eed2 = eed**2
        ee = abs( ( (1.-2.*efficiency)*en2 + eed2 ) / d2 )
        # ee = abs( (en2/ed2)*(ed2-en2) / d2 ) # cf. Eram Rizvi
        efficiency_error = sqrt(ee)
    else:
        # Check references
        efficiency_error = .0

    return efficiency, efficiency_error

####################################################################################################

def to_percent(x):
    return 100. * x
