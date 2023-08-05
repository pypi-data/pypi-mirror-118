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

from abc import ABC, abstractmethod

from quantlet_streaming.iterables import Canonical
from quantlet_streaming.metadata import expects
from quantlet_streaming.stream import QLet


class Agent(ABC):
    def __init__(self, label, env):
        self.label = label
        self.env = env
        self.action = env.process(self.run(env))

    def run(self, env):
        while True:
            self.simulate(env)

    def process(self, f):
        return self.env.process(f)

    def timeout(self, timeout):
        return self.env.timeout

    @abstractmethod
    def simulate(self, env):
        pass


@QLet
@expects(Canonical)
def add(iterable):
    """ Candidate for quantlet_streaming.iterables """

    return sum(iterable)
