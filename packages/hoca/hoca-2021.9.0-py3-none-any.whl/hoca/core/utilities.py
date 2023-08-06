# Copyright (C) 2021 Jean-Louis Paquelin <jean-louis.paquelin@villa-arson.fr>
#
# This file is part of the hoca (Higher-Order Cellular Automata) library.
#
# hoca is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hoca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with hoca.  If not, see <http://www.gnu.org/licenses/>.

class AutomataUtilities:
    """
    The 8 adjacent field cells are numbered from 0 to 8 (with 0 == 8 as 0 degree is the same direction as 360)
    7 0 1
    6 * 2
    5 4 3
    So the DIRECTION_TO_DELTA constant says for each direction from 0 to 7 how much the x and y
    coordinates vary.
    """
    DIRECTION_TO_DELTA = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

    @classmethod
    def get_dx_dy(cls, direction):
        """
        :param direction: an int denoting the direction of the adjacent field cell from a central position
        :return: a pair (int, int) of cartesian int offsets
        """
        direction %= 8

        return cls.DIRECTION_TO_DELTA[direction]

    @classmethod
    def get_x_y(cls, direction, x, y):
        """Computes a new pair of coordinates from x, y and the direction

        :param direction: an int denoting the direction of the adjacent field cell from a central position
        :param x: an int corresponding to an abscissa in the 2D plane of a field
        :param y: an int corresponding to an ordinate in the 2D plane of a field
        :return: a pair (int, int) of cartesian coordinates
        """
        dx, dy = AutomataUtilities.get_dx_dy(direction)
        x += dx
        y += dy

        return x, y

    @classmethod
    def wrap_coordinates(cls, x, y, width, height):
        """Computes a new pair of coordinates from x, y while keeping these coordinates within the width, height
        by folding the plane like a torus.

        :param x: an int corresponding to an abscissa in a 2D cartesian plane
        :param y: an int corresponding to an ordinate in a 2D cartesian plane
        :param width: an int corresponding to the width of a finite plane
        :param height: an int corresponding to the ordinate of a finite plane
        :return: a pair (int, int) of cartesian coordinates
        """
        # Wrap the coordinates around
        if x >= width:
            x = x - width
        elif x < 0:
            x = width + x

        if y >= height:
            y = y - height
        elif y < 0:
            y = height + y

        return x, y

    @classmethod
    def get_random_tuple(cls, min_max_sequence):
        """
        A function to produce a list of random values in [min, max].
        Instead of calling a random function multiple time having values depending in some way
        of each other, it creates a large int that is sliced to produce the returned sequence of
        random integers in [min, max].

        :param min_max_sequence: sequence of pair
        :return: a list of random values
        """
        pass
        # TODO: write it
