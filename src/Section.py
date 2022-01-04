# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:47:50 2017

@author: lfoul
"""
import OpenGL.GL as gl
from Opening import Opening


class Section:
    # Constructor
    def __init__(self, parameters=None):
        # Parameters
        # position: position of the wall 
        # width: width of the wall - mandatory
        # height: height of the wall - mandatory
        # thickness: thickness of the wall
        # color: color of the wall        

        # Sets the parameters
        if parameters is None:
            parameters = {}
        self.parameters = parameters

        # Sets the default parameters
        if 'position' not in self.parameters:
            self.parameters['position'] = [0, 0, 0]
        if 'width' not in self.parameters:
            raise Exception('Parameter "width" required.')
        if 'height' not in self.parameters:
            raise Exception('Parameter "height" required.')
        if 'orientation' not in self.parameters:
            self.parameters['orientation'] = 0
        if 'thickness' not in self.parameters:
            self.parameters['thickness'] = 0.2
        if 'color' not in self.parameters:
            self.parameters['color'] = [0.5, 0.5, 0.5]
        if 'edges' not in self.parameters:
            self.parameters['edges'] = False

            # Objects list
        self.objects = []

        # Generates the wall from parameters
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
            [0, 1, 2, 3],  # Front
            [1, 5, 6, 2],  # Top
            [5, 6, 7, 4],  # Back
            [4, 7, 3, 0],  # Bottom
            [0, 1, 5, 4],  # Left
            [2, 6, 7, 3]  # Right
        ]

        # Checks if the opening can be created for the object x

    def canCreateOpening(self, x: Opening):
        # A compléter en remplaçant pass par votre code
        x_pos = x.getParameter("position")
        x_width = x.getParameter("width")
        x_height = x.getParameter("height")
        self_pos = self.getParameter("position")
        self_height = self.getParameter("height")
        self_width = self.getParameter("width")

        if self_pos[0] > x_pos[0] or self_pos[0] + self_width < x_pos[0] + x_width:
            return False
        if self_pos[2] > x_pos[2] or self_pos[2] + self_height < x_pos[2] + x_height:
            return False
        return True
        # Creates the new sections for the object x

    def createNewSections(self, x: Opening):
        # A compléter en remplaçant pass par votre code
        if not self.canCreateOpening(x):
            raise Exception("Can't create this opening")
        sec1 = Section({'position': self.parameters['position'],
                        'width': x.getParameter('position')[0] - self.parameters['position'][0],
                        'height': self.parameters['height'],
                        'thickness': self.parameters['thickness']
                        })
        sec2 = Section({'position': [x.getParameter('position')[0],
                                     self.parameters['position'][1],
                                     x.getParameter('position')[2] + x.getParameter('height')],
                        'height': self.parameters['height'] - (
                                x.getParameter('position')[2] + x.getParameter('height')),
                        'width': x.getParameter('width'),
                        'thickness': self.parameters['thickness']
                        })

        sec3 = Section({'position': [
            sec2.getParameter('position')[0],
            self.parameters['position'][1],
            self.parameters['position'][2]],
            'height': x.getParameter('position')[2] - self.parameters['position'][2],
            'width': x.getParameter('width'),
            'thickness': self.parameters['thickness']
        })
        sec4 = Section(
            {'position': [sec2.parameters['position'][0] + sec2.parameters['width'],
                          self.parameters['position'][1],
                          self.parameters['position'][2]],
             'height': self.parameters['height'],
             'width': self.parameters['width'] - (sec1.parameters['width'] + sec2.parameters['width']),
             'thickness': self.parameters['thickness']
             })
        sections = [sec1, sec2, sec3, sec4]

        if sec3.parameters['height'] == 0:
            sections.remove(sec3)
        if sec2.parameters['height'] == 0:
            sections.remove(sec2)
        if sec1.parameters['width'] == 0:
            sections.remove(sec1)
        if sec4.parameters['width'] == 0:
            sections.remove(sec4)

        return sections

    # Draws the edges
    def drawEdges(self):
        # A compléter en remplaçant pass par votre code
        gl.glPushMatrix()

        if self.parameters['orientation'] != 0:
            gl.glRotate(self.parameters['orientation'], 0.0, 0.0, 1.0)

        gl.glBegin(gl.GL_LINES)  # Tracé d’un quadrilatère

        for face in self.faces:
            for i, point in enumerate(face):
                gl.glColor3fv([0.0, 0.0, 0.0])
                gl.glVertex3fv(self.vertices[point])

        gl.glEnd()

        gl.glPopMatrix()

    # Draws the faces
    def draw(self):
        if self.parameters['edges']:
            self.drawEdges()

        gl.glPushMatrix()

        gl.glTranslatef(
            self.parameters['position'][0],
            self.parameters['position'][1],
            self.parameters['position'][2],
        )

        if self.parameters['orientation'] != 0:
            gl.glRotate(self.parameters['orientation'], 0.0, 0.0, 1.0)

        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)  # on trace les faces : GL_FILL
        gl.glBegin(gl.GL_QUADS)  # Tracé d’un quadrilatère

        for face in self.faces:
            for i, point in enumerate(face):
                gl.glColor3fv([self.parameters['color'][0] / (i + 1 * 15),
                               self.parameters['color'][1],
                               self.parameters['color'][2] * i * 5])
                gl.glVertex3fv(self.vertices[point])

        gl.glEnd()

        gl.glPopMatrix()
