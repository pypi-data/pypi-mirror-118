#
#     QuantLET-agents - Synchronous and asynchronous agents for discrete-event simulation.
#          This is related to the distribution and simulation facets defined as part of
#          the financial language SIGMA.
#
#     Copyright (C) 2006 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from collections import namedtuple
from itertools import product


class Shock(object):
    def __init__(self, **args):
        self.__dict__.update(args)


def benchmark(model, *args, **kwargs):
    #    properties = 'seq ' + ' '.join(kwargs.keys()) + ' ' + model_name
    #    Shock = namedtuple('Shock', properties)
    seqs = [kwargs[k] for k in kwargs]
    products = product(*seqs)  # cartesian product
    shocks = []
    seq = 0
    for p in products:
        i = 0
        d = dict(seq=seq)
        for k in kwargs:
            d[k] = p[i]
            i += 1
        shock = Shock(**d)
        seq += 1
        shocks.append(shock)

    for s in shocks:
        try:
            model(s)
            yield s
        except BaseException:
            print("exception on shock=%s" % s.__dict__)


montecarlo = benchmark
backtest = benchmark
