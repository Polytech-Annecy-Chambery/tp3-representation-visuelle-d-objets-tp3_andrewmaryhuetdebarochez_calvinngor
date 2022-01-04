# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""

import OpenGL.GL as gl


class Opening:
    # Constructor
    def __init__(self, parameters={}):
        # Parameters
        # position: mandatory
        # width: mandatory
        # height: mandatory
        # thickness: mandatory
        # color: mandatory        

        # Sets the parameters
        self.parameters = parameters

        # Sets the default parameters 
        if 'position' not in self.parameters:
            raise Exception('Parameter "position" required.')
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')
        if 'thickness' not in self.parameters:
            raise Exception('Parameter "thickness" required.')
        if 'color' not in self.parameters:
            raise Exception('Parameter "color" required.')

            # Generates the opening from parameters
        self.generate()

        # Getter

    def getParameter(self, parameterKey):
        return self.parameters[parameterKey]

    # Setter
    def setParameter(self, parameterKey, parameterValue):
        self.parameters[parameterKey] = parameterValue
        return self

        # Defines the vertices and faces

    def generate(self):
        self.vertices = [
            [0, 0, 0],  # 0
            [0, 0, self.parameters['height']],  # 1
            [self.parameters['width'], 0, self.parameters['height']],  # 2
            [self.parameters['width'], 0, 0],  # 3
            [0, self.parameters['thickness'], 0],  # 4
            [0, self.parameters['thickness'], self.parameters['height']],  # 5
            [self.parameters['width'], self.parameters['thickness'], self.parameters['height']],  # 6
            [self.parameters['width'], self.parameters['thickness'], 0],  # 7
        ]

        self.faces = [
            [1, 5, 6, 2],  # Top
            [4, 7, 3, 0],  # Bottom
            [0, 1, 5, 4],  # Left
            [2, 6, 7, 3]  # Right
        ]

        # Draws the faces

    def draw(self):
        # A compléter en remplaçant pass par votre code

        gl.glPushMatrix()

        gl.glTranslatef(
            self.parameters['position'][0],
            self.parameters['position'][1],
            self.parameters['position'][2],
        )

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)  # on trace les faces : GL_FILL
        gl.glBegin(gl.GL_QUADS)  # Tracé d’un quadrilatère

        for face in self.faces:
            for i, point in enumerate(face):
                gl.glColor3fv([10 / (i + 1 * 15), 0.0, 1 * i * 5])
                gl.glVertex3fv(self.vertices[point])

        gl.glEnd()

        gl.glPopMatrix()

