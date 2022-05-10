"""
Module containing additional shapes for Pygame.
Includes a Circle and Polygon objects.
Supports pixel perfect collision for extension objects and normal pygame objects.
"""

import pygame
from math import sqrt, cos, sin, radians

class Circle:
    def __init__(self, center: tuple, radius: float):
        """
        Creates a Circle object
        Arguments:
            center: (x, y)
            radius: float
        """
        self._x, self._y = center[0], center[1]
        self._center = list(center)
        self.radius = radius
        self.rect = pygame.Rect(self._center[0]-radius, self._center[1]-radius, 2*radius, 2*radius)

    def collidepoint(self, coord):
        """
        Test if a point is inside the circle. 
        Arguments:
            coord: coordinate of point, (x, y)
        Returns:
            True if point is inside circle and False if not
        """
        length = sqrt((self._x-coord[0])**2 + (self._y-coord[1])**2)
        if length <= self.radius: 
            return True
        return False

    def collidelines(self, lines):
        for line in lines:
            if line[0] not in ["x", "y"]:
                m_in = -1/line[0]
                c_in = self._y - (m_in*self._x)
                x = (c_in-line[1]) / (line[0]-m_in)
                y = (m_in*x) + c_in
                length = sqrt((self._x - x)**2 + (self._y - y)**2)
                if (length <= self.radius) and (line[3][0] <= x <= line[3][1]):
                    return True

            elif line[0] == "x":
                point = self.radius**2 - (line[1]-self._x)**2
                if point < 0: 
                    continue
                y1 = self._y + sqrt(point)
                y2 = self._y - sqrt(point)
                if (line[4][0] <= self._y <= line[4][1]) and (line[4][0] <= y1 <= line[4][1]) and (line[4][0] <= y2 <= line[4][1]):
                    return True
            elif line[0] == "y":
                point = self.radius**2 - (line[1]-self._y)**2
                if point < 0: 
                    continue
                x1 = self._x + sqrt(point)
                x2 = self._x - sqrt(point)
                if (line[3][0] <= self._x <= line[3][1]) and (line[3][0] <= x1 <= line[3][1]) and (line[3][0] <= x2 <= line[3][1]):
                    return True
        
        return False

    def collideline(self, line):
        if line[0] not in ["x", "y"]:
            m_in = -1/line[0]
            c_in = self._y - (m_in*self._x)
            x = (c_in-line[1]) / (line[0]-m_in)
            y = (m_in*x) + c_in
            length = sqrt((self._x - x)**2 + (self._y - y)**2)
            if (length <= self.radius) and (line[3][0] <= x <= line[3][1]):
                return True

        elif line[0] == "x":
            point = self.radius**2 - (line[1]-self._x)**2
            if point < 0: 
                return False
            y1 = self._y + sqrt(point)
            y2 = self._y - sqrt(point)
            if (line[4][0] <= self._y <= line[4][1]) and (line[4][0] <= y1 <= line[4][1]) and (line[4][0] <= y2 <= line[4][1]):
                return True

        elif line[0] == "y":
            point = self.radius**2 - (line[1]-self._y)**2
            if point < 0: 
                return False
            x1 = self._x + sqrt(point)
            x2 = self._x - sqrt(point)
            if (line[3][0] <= self._x <= line[3][1]) and (line[3][0] <= x1 <= line[3][1]) and (line[3][0] <= x2 <= line[3][1]):
                return True
        
        return False

    def collidepolygon(self, polygon):
        if self.rect.colliderect(polygon.rect):
            if polygon.collidepoint(self._center):
                return True
            
            for coord in polygon.coordinates:
                if self.collidepoint(coord):
                    return True

            if self.collidelines(polygon.boundaries):
                return True
            
        else:
            return False

    def colliderect(self, rect: pygame.Rect):
        """
        Test if a Circle object is colliding with a pygame.Rect object
        Arguments:
            rect: pygame.Rect object
        Returns:
            True if collision detected and False if not
        """
        x_1, x_2 = rect.x, rect.right
        y_1, y_2 = rect.y, rect.bottom
        c_1, c_2, c_3, c_4 = (x_1, y_1), (x_2, y_1), (x_2, y_2), (x_1, y_2)
        l_1 = sqrt((self._x-c_1[0])**2 + (self._y-c_1[1]) **2)
        l_2 = sqrt((self._x-c_2[0])**2 + (self._y-c_2[1]) **2)
        l_3 = sqrt((self._x-c_3[0])**2 + (self._y-c_3[1]) **2)
        l_4 = sqrt((self._x-c_4[0])**2 + (self._y-c_4[1]) **2)

        if self.rect.colliderect(rect):
            if (x_1 <= self._x < x_2) and (y_1 <= self._y < y_2):  # Check if the circle's center is in the rect
                return True
            
            elif (l_1 < self.radius) or (l_2 < self.radius) or (l_3 < self.radius) or (l_4 < self.radius):  # Check if the circle is within the rect's corners
                return True
            
            elif ((abs(self._x - x_1) < self.radius) or ((abs(self._x - x_2) < self.radius))) and (y_1 <= self._y < y_2):  # Check if the center of the circle is close to the horizontal component of the rect
                return True

            elif ((abs(self._y - y_1) < self.radius) or ((abs(self._y - y_2) < self.radius))) and (x_1 <= self._x < x_2):  # Check if the center of the circle is close to the verticle component of the rect
                return True

        return False

    def collidecircle(self, circle):
        """
        Test if a Circle object is colliding with another Circle object
        Arguments:
            circle: Circle object
        Returns:
            True if collision detected and False if not
        """
        distance = sqrt((self._x-circle.x)**2 + (self._y-circle.y)**2)  # Check if the centers of the circles' are within range of one another
        if distance < (circle.radius+self.radius):
            return True
        else:
            return

    def move(self, x: float, y: float):
        self.x += x
        self.y += y
        return self

    def draw(self, surface, color, width=0):
        pygame.draw.circle(surface, color, self._center, self.radius, width)

    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, center):
        self._center = center
        self._x = center[0]
        self._y = center[1]
        self.rect = pygame.Rect(self._center[0]-self.radius, self._center[1]-self.radius, 2*self.radius, 2*self.radius)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = x
        self._center[0] = x
        self.rect = pygame.Rect(self._center[0]-self.radius, self._center[1]-self.radius, 2*self.radius, 2*self.radius)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, y):
        self._y = y
        self._center[1] = y
        self.rect = pygame.Rect(self._center[0]-self.radius, self._center[1]-self.radius, 2*self.radius, 2*self.radius)


class Polygon:
    def __init__(self, coordinates: list):
        """
        Creates a Polygon object
        Arguments:
            coordinates: a list of coordinates
        """
        self.reorder_coords(coordinates)
        self.create_center()
        self.create_boundaries()

    def reorder_coords(self, coordinates):
        """Re-organise the coordinates and define the midpoint of the Polygon"""
        copy_coords = []
        [copy_coords.append(i) for i in coordinates if i not in copy_coords]


        lengths = [sqrt(i[0]**2 + i[1]**2) for i in copy_coords]
        next_coord = copy_coords[lengths.index(min(lengths))]
        self._coordinates = [list(next_coord)]
        copy_coords.remove(next_coord)

        for j in range(len(copy_coords)):
            right_coords = [i for i in copy_coords if i[0] >= next_coord[0]]
            left_coords = [i for i in copy_coords if i[0] < next_coord[0]]
            if len(right_coords) > 0:
                lengths = [sqrt((next_coord[0] - i[0])**2 + (next_coord[1] - i[1])**2) for i in right_coords]
                next_coord = right_coords[lengths.index(min(lengths))]
            else:
                lengths = [sqrt((next_coord[0] - i[0])**2 + (next_coord[1] - i[1])**2) for i in left_coords]
                next_coord = left_coords[lengths.index(min(lengths))]
            self._coordinates.append(list(next_coord))
            copy_coords.remove(next_coord)
        
        self._coordinates.append(self._coordinates[0])

        x, y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)

    def create_center(self):
        self._center = [sum([i[0] for i in self._coordinates[1:]]) / len(self._coordinates[1:]), sum([i[1] for i in self._coordinates[1:]]) / len(self._coordinates[1:])]

    def create_boundaries(self):
        """Generate the polygon's boundaries for collision testing"""

        self.boundaries = []
        for i in range(len(self.coordinates)-1):

            if self.coordinates[i][0] == self.coordinates[i+1][0]:
                gradient = "x"
                y_intercept = self.coordinates[i][0]
                if self.coordinates[i][0] >= self._center[0]: 
                    comparator = "<="
                else: 
                    comparator = ">="

            elif self.coordinates[i][1] == self.coordinates[i+1][1]:
                gradient = "y"
                y_intercept = self.coordinates[i][1]
                if self.coordinates[i][1] >= self._center[1]: 
                    comparator = "<="
                else: 
                    comparator = ">="

            else:
                gradient = (self.coordinates[i][1]-self.coordinates[i+1][1]) / (self.coordinates[i][0]-self.coordinates[i+1][0])
                y_intercept = self.coordinates[i][1] - (gradient*self.coordinates[i][0])
                if (gradient*self._center[0]) + y_intercept >= self._center[1]: 
                    comparator = "<="
                else: 
                    comparator = ">="

            x, y = zip(*self._coordinates[i:i+2])

            self.boundaries.append([gradient, y_intercept, comparator, (min(x), max(x)), (min(y), max(y))])

    def collidepoint(self, coord):
        """
        Test if a point is inside the polygon.
        Arguments:
            coord: coordinate of point, (x, y)
        Returns:
            True if point is within the polygon and False if not
        """
        collision = False
        for line in self.boundaries:
            if line[0] == "x":
                if line[2] == "<=": 
                    if (coord[0] <= line[1]):
                        collision = True
                    else: 
                        return False
                else: 
                    if (coord[0] >= line[1]):
                        collision = True
                    else: 
                        return False

            elif line[0] == "y":
                if line[2] == "<=": 
                    if (coord[1] <= line[1]):
                        collision = True
                    else: 
                        return False
                else: 
                    if (coord[1] >= line[1]):
                        collision = True
                    else: 
                        return False

            else:
                if line[2] == "<=":
                    if coord[1] <= (line[0]*coord[0]) + line[1]:
                        collision = True
                    else: 
                        return False
                else:
                    if coord[1] >= (line[0]*coord[0]) + line[1]:
                        collision = True
                    else: 
                        return False

        return collision

    def collidelines(self, lines):
        """
        Test if a line is colliding with the polygon.
        Arguments:
            lines: a list of values used.
        Returns:
            True if intersection detected and False if not
        """

        for boundary in self.boundaries:
            for line in lines:
                if (boundary[0] == line[0]) and (boundary[1] == line[1]): 
                    return True
                elif (boundary[0] == "x") and (line[0] == "y") and (boundary[4][0] <= line[1] <= boundary[4][1]) and (line[3][0] <= boundary[1] <= line[3][1]): 
                    return True
                elif (boundary[0] == "y") and (line[0] == "x") and (boundary[3][0] <= line[1] <= boundary[3][1]) and (line[4][0] <= boundary[1] <= line[4][1]): 
                    return True

                elif boundary[0] not in ["x", "y"]:
                    if (line[0] == "x") and (boundary[3][0] <= line[1] <= boundary[3][1]) and (line[4][0] <= (line[1]*boundary[0])+boundary[1] <= line[4][1]): 
                        return True
                    elif (line[0] == "y") and (boundary[4][0] <= line[1] <= boundary[4][1]) and (line[3][0] <= (line[1]-boundary[1])/boundary[0] <= line[3][1]): 
                        return True
                    elif line[0] not in ["x", "y"]:
                        if boundary[0] == line[0]: 
                            continue
                        elif (boundary[3][0] <= (line[1]-boundary[1])/(boundary[0]-line[0]) <= boundary[3][1]) and (line[3][0] <= (line[1]-boundary[1])/(boundary[0]-line[0]) <= line[3][1]):
                            return True
        
        return False

    def collideline(self, line):
        """
        Test if a line is colliding with the polygon.
        Arguments:
            line: a list of values used.
        Returns:
            True if intersection detected and False if not
        """

        for boundary in self.boundaries:
            if (boundary[0] == line[0]) and (boundary[1] == line[1]): 
                return True
            elif (boundary[0] == "x") and (line[0] == "y") and (boundary[4][0] <= line[1] <= boundary[4][1]) and (line[3][0] <= boundary[1] <= line[3][1]): 
                return True
            elif (boundary[0] == "y") and (line[0] == "x") and (boundary[3][0] <= line[1] <= boundary[3][1]) and (line[4][0] <= boundary[1] <= line[4][1]): 
                return True

            elif boundary[0] not in ["x", "y"]:
                if (line[0] == "x") and (boundary[3][0] <= line[1] <= boundary[3][1]) and (line[4][0] <= (line[1]*boundary[0])+boundary[1] <= line[4][1]): 
                    return True
                elif (line[0] == "y") and (boundary[4][0] <= line[1] <= boundary[4][1]) and (line[3][0] <= (line[1]-boundary[1])/boundary[0] <= line[3][1]): 
                    return True
                elif line[0] not in ["x", "y"]:
                    if boundary[0] == line[0]: continue
                    elif (boundary[3][0] <= (line[1]-boundary[1])/(boundary[0]-line[0]) <= boundary[3][1]) and (line[3][0] <= (line[1]-boundary[1])/(boundary[0]-line[0]) <= line[3][1]): 
                        return True

        return False

    def colliderect(self, rect: pygame.Rect):
        """
        Test if a pygame.Rect object is colliding with the polygon.
        Arguments:
            rect: pygame.Rect object
        Returns:
            True if collision detected and False if not
        """

        rect_coords = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]

        rect_lines = [["y", rect.top, "", (rect.left, rect.right), (rect.top, rect.top)], 
                    ["x", rect.right, "", (rect.right, rect.right), (rect.top, rect.bottom)], 
                    ["y", rect.bottom, "", (rect.left, rect.right), (rect.bottom, rect.bottom)], 
                    ["x", rect.left, "", (rect.left, rect.left), (rect.top, rect.bottom)]
        ]

        if self.rect.colliderect(rect):
            for coord in self._coordinates:
                if rect.collidepoint(coord):
                    return True

            for coord in rect_coords:
                if self.collidepoint(coord):
                    return True
                    
            if self.collidelines(rect_lines):
                return True
        
        return False

    def collidecircle(self, circle):
        if self.rect.colliderect(circle.rect):
            if self.collidepoint(circle.center):
                return True
            
            for coord in self._coordinates:
                if circle.collidepoint(coord):
                    return True

            if circle.collidelines(self.boundaries):
                return True
        
        return False

    def collidepolygon(self, polygon):
        if self.rect.colliderect(polygon.rect):
            for coord in self._coordinates:
                if polygon.collidepoint(coord):
                    return True
            
            for coord in polygon.coordinates:
                if self.collidepoint(coord):
                    return True
        
            if self.collidelines(polygon.boundaries):
                return True

        return False

    def collideline_object(self, line):
        """
        Test if a line object is colliding with the polygon.
        """
        if self.rect.colliderect(line.rect):
            for coord in line.coordinates:
                if self.collidepoint(coord):
                    return True
        
            if self.collideline(line.boundary):
                return True

        return False

    def draw(self, surface, color, width=0):
        """
        Equivilent of the function pygame.draw.polygon.
        Arguments:
            surface: pygame.Surface object
            color: color value, tuple
        """

        pygame.draw.polygon(surface, color, self._coordinates, width)
    
    def manual_draw(self, surface, color, width=0):
        """Draw an outline of the polygon"""

        for i in range(len(self._coordinates)-1):
            pygame.draw.line(surface, color, self._coordinates[i], self._coordinates[i+1], width)

    def aadraw(self, surface, color):
        """Draw an anti-aliased outline of the polygon"""

        for i in range(len(self._coordinates)-1):
            pygame.draw.aaline(surface, color, self._coordinates[i], self._coordinates[i+1])

    def move(self, x: float=0, y: float=0):
        """
        Move the polygon by a vector.
        Arguments:
            x: magnitude of horizontal movement
            y: magnitude of verticle movement
        """

        self._coordinates = [[coord[0]+x, coord[1]+y] for coord in self._coordinates]

        _x, _y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(_x), min(_y), max(_x)-min(_x)+1, max(_y)-min(_y)+1)
        
        self._center[0] += x
        self._center[1] += y
        self.create_boundaries()

        return self

    def move_by(self, x: float=0, y: float=0):
        """
        Move the polygon by a vector.
        Arguments:
            x: magnitude of horizontal movement
            y: magnitude of verticle movement
        """

        self._coordinates = [[coord[0]+x, coord[1]+y] for coord in self._coordinates]

        _x, _y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(_x), min(_y), max(_x)-min(_x)+1, max(_y)-min(_y)+1)
        
        self._center[0] += x
        self._center[1] += y
        self.create_boundaries()

        return self

    def move_to(self, position: tuple):
        """
        Move the polygon's center to a specified coordinate.
        Arguments:
            position: new coordinate to move to
        """

        self.move_by(position[0]-self._center[0], position[1]-self._center[1])
        return self

    def rotate(self, angle, center: tuple=None):
        """
        Roate the polygon around a point
        Arguments:
            angle: in degrees
            center: point of rotation (x, y)
        """

        if not center:
            center = self._center
        
        angle = radians(angle)
        for i in range(len(self._coordinates)):
            self._coordinates[i] = [cos(angle)*(self._coordinates[i][0]-center[0]) - sin(angle)*(self._coordinates[i][1]-center[1]) + center[0], 
                                    sin(angle)*(self._coordinates[i][0]-center[0]) + cos(angle)*(self._coordinates[i][1]-center[1]) + center[1]
            ]

        self.reorder_coords(self._coordinates)
        self.create_center()
        self.create_boundaries()

        return self

    def enlarge(self, scale_factor=1, center=None):
        if center == None: 
            center = self._center

        for i in range(len(self._coordinates)):
            self._coordinates[i] = [scale_factor*(self._coordinates[i][0]-center[0]) + center[0], 
                                    scale_factor*(self._coordinates[i][1]-center[1]) + center[1]
            ]

        x, y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)
        self.create_center()
        self.create_boundaries()

        return self

    @property
    def coordinates(self):
        return self._coordinates
    @coordinates.setter
    def coordinates(self, coordinates):
        self.reorder_coords(coordinates)
        self.create_center()
        self.create_boundaries()
        return self

    @property
    def center(self):
        return self._center
    @center.setter
    def center(self, center):
        vector = [center[0]-self._center[0], center[1]-self._center[1]]
        for i in range(len(self._coordinates)):
            self._coordinates[i] = [self._coordinates[i][0]+vector[0], self._coordinates[i][1]+vector[1]]

        x, y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)
        
        self._center = list(center)
        self.create_boundaries()


class Line:
    def __init__(self, coordinates: list):
        """
        Creates a Polygon object
        Arguments:
            coordinates: a list of coordinates
        """
        self.reorder_coords(coordinates)
        self.create_center()
        self.create_boundary()

    def reorder_coords(self, coordinates):
        """Re-organise the coordinates and define the midpoint of the Polygon"""
        self._coordinates = [coordinates[0], coordinates[1], coordinates[0]]

        x, y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)

    def create_center(self):
        self.center = [sum([i[0] for i in self._coordinates[1:]]) / len(self._coordinates[1:]), 
                    sum([i[1] for i in self._coordinates[1:]]) / len(self._coordinates[1:])
        ]

    def create_boundary(self):
        """Generate the line's boundaries for collision testing"""

        if self.coordinates[0][0] == self.coordinates[1][0]:
            gradient = "x"
            y_intercept = self.coordinates[0][0]

        elif self.coordinates[0][1] == self.coordinates[1][1]:
            gradient = "y"
            y_intercept = self.coordinates[0][1]

        else:
            gradient = (self.coordinates[0][1]-self.coordinates[1][1]) / (self.coordinates[0][0]-self.coordinates[1][0])
            y_intercept = self.coordinates[0][1] - (gradient*self.coordinates[0][0])

        x, y = zip(*self._coordinates[0:2])

        self.boundary = [gradient, y_intercept, "", (min(x), max(x)), (min(y), max(y))]

    def collidelines(self, lines):
        """
        Test if a line is colliding with the line.
        Arguments:
            lines: a list of values used.
        Returns:
            True if intersection detected and False if not
        """

        for line in lines:
            if (self.boundary[0] == line[0]) and (self.boundary[1] == line[1]): 
                return True
            elif (self.boundary[0] == "x") and (line[0] == "y") and (self.boundary[4][0] <= line[1] <= self.boundary[4][1]) and (line[3][0] <= self.boundary[1] <= line[3][1]): 
                return True
            elif (self.boundary[0] == "y") and (line[0] == "x") and (self.boundary[3][0] <= line[1] <= self.boundary[3][1]) and (line[4][0] <= self.boundary[1] <= line[4][1]): 
                return True

            elif self.boundary[0] not in ["x", "y"]:
                if (line[0] == "x") and (self.boundary[3][0] <= line[1] <= self.boundary[3][1]) and (line[4][0] <= (line[1]*self.boundary[0])+self.boundary[1] <= line[4][1]): 
                    return True
                elif (line[0] == "y") and (self.boundary[4][0] <= line[1] <= self.boundary[4][1]) and (line[3][0] <= (line[1]-self.boundary[1])/self.boundary[0] <= line[3][1]): 
                    return True
                elif line[0] not in ["x", "y"]:
                    if self.boundary[0] == line[0]: 
                        continue
                    elif (self.boundary[3][0] <= (line[1]-self.boundary[1])/(self.boundary[0]-line[0]) <= self.boundary[3][1]) and (line[3][0] <= (line[1]-self.boundary[1])/(self.boundary[0]-line[0]) <= line[3][1]): 
                        return True

        return False

    def colliderect(self, rect: pygame.Rect):
        """
        Test if a pygame.Rect object is colliding with the polygon.
        Arguments:
            rect: pygame.Rect object
        Returns:
            True if collision detected and False if not
        """

        rect_lines = [["y", rect.top, "", (rect.left, rect.right), (rect.top, rect.top)], 
                    ["x", rect.right, "", (rect.right, rect.right), (rect.top, rect.bottom)], 
                    ["y", rect.bottom, "", (rect.left, rect.right), (rect.bottom, rect.bottom)], 
                    ["x", rect.left, "", (rect.left, rect.left), (rect.top, rect.bottom)]
        ]

        if self.rect.colliderect(rect):
            for coord in self._coordinates:
                if rect.collidepoint(coord):
                    return True

            if self.collidelines(rect_lines):
                return True
        
        return False

    def collidecircle(self, circle):
        if self.rect.colliderect(circle.rect):
            for coord in self._coordinates:
                if circle.collidepoint(coord):
                    return True

            if circle.collideline(self.boundary):
                return True
        
        return False

    def collidepolygon(self, polygon):
        if self.rect.colliderect(polygon.rect):
            for coord in self._coordinates:
                if polygon.collidepoint(coord):
                    return True
        
            if self.collidelines(polygon.boundaries):
                return True

        return False
    
    def draw(self, surface, color):
        """Draw an outline of the polygon"""

        pygame.draw.line(surface, color, self._coordinates[0], self._coordinates[1])

    def aadraw(self, surface, color):
        """Draw an anti-aliased outline of the polygon"""

        pygame.draw.aaline(surface, color, self._coordinates[0], self._coordinates[1])

    def move(self, x: float=0, y: float=0):
        """
        Move the polygon by a vector.
        Arguments:
            x: magnitude of horizontal movement
            y: magnitude of verticle movement
        """

        self._coordinates = [[coord[0]+x, coord[1]+y] for coord in self._coordinates]

        _x, _y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(_x), min(_y), max(_x)-min(_x)+1, max(_y)-min(_y)+1)

        self.center[0] += x
        self.center[1] += y
        self.create_boundary()

        return self

    def move_by(self, x: float=0, y: float=0):
        """
        Move the polygon by a vector.
        Arguments:
            x: magnitude of horizontal movement
            y: magnitude of verticle movement
        """

        self._coordinates = [[coord[0]+x, coord[1]+y] for coord in self._coordinates]
        self.rect.x += x
        self.rect.y += y
        self.center[0] += x
        self.center[1] += y
        self.create_boundary()

        return self

    def move_to(self, position: tuple):
        """
        Move the polygon's center to a specified coordinate.
        Arguments:
            position: new coordinate to move to
        """

        self.move_by(position[0]-self.center[0], position[1]-self.center[1])
        return self

    def rotate(self, angle, center: tuple=None):
        """
        Roate the line around a point
        Arguments:
            angle: in degrees
            center: point of rotation (x, y)
        """

        if not center:
            center = self.center
        
        angle = radians(angle)
        for i in range(len(self._coordinates)):
            self._coordinates[i] = [cos(angle) * (self._coordinates[i][0] - center[0]) - sin(angle) * (self._coordinates[i][1] - center[1]) + center[0], 
                                    sin(angle) * (self._coordinates[i][0] - center[0]) + cos(angle) * (self._coordinates[i][1] - center[1]) + center[1]
            ]

        self.reorder_coords(self._coordinates)
        self.create_center()
        self.create_boundary()
        
        return self

    def enlarge(self, scale_factor=1, center=None):
        if center == None: 
            center = self.center
        for i in range(len(self._coordinates)):
            self._coordinates[i] = [scale_factor*(self._coordinates[i][0]-center[0]) + center[0], 
                                    scale_factor*(self._coordinates[i][1]-center[1]) + center[1]
            ]

        x, y = zip(*self._coordinates)
        self.rect = pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)
        self.create_center()
        self.create_boundary()

        return self

    @property
    def coordinates(self):
        return self._coordinates
    @coordinates.setter
    def coordinates(self, coordinates):
        self.reorder_coords(coordinates)
        self.create_center()

def rotate_coord(coord, angle, center: tuple=None):
    """
    Roate the coordinate around a point.
    Arguments:
        coord: coordinate to rotate, (x, y)
        angle: in degrees
        center: point of rotation, (x, y)
    Returns:
        Rotated coordinate
    """

    if not center:
        center = (0, 0)
    angle = radians(angle)
    coord = [cos(angle) * (coord[0] - center[0]) - sin(angle) * (coord[1] - center[1]) + center[0], 
            sin(angle) * (coord[0] - center[0]) + cos(angle) * (coord[1] - center[1]) + center[1]
    ]

    return coord

def rect_to_polygon(rect: pygame.Rect):
    """
    Convert a pygameRect object to a Polygon object
    """
    return Polygon([rect.topleft, rect.topright, rect.bottomright, rect.bottomleft])

def polygon_to_rect(polygon: Polygon):
    """
    Returns the rect attribute of a polygon
    """
    return polygon.rect

def coord_center(coordinates: list):
    """
    Returns the center coordinate of a list of points
    """
    return [sum([i[0] for i in coordinates]) / len(coordinates), sum([i[1] for i in coordinates]) / len(coordinates)]

def coords_to_rect(coordinates: list):
    """
    Returns a pygame.Rect object of a list of coordinates
    """
    x, y = zip(*coordinates)
    return pygame.Rect(min(x), min(y), max(x)-min(x)+1, max(y)-min(y)+1)

def enlarge_coord(coord: list, scale_factor: float=1, center=(0, 0)):
    """
    Perform an enlargement function to a coordinate
    """
    return [scale_factor*(coord[0]-center[0]) + center[0], scale_factor*(coord[1]-center[1]) + center[1]]