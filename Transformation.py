import numpy as np
import pygame
from math import *
class Rotation:
    def __init__(self, angle, axis):
        self.angle = angle
        self.axis = axis
def identity_matrix():
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)

def translation_matrix(x, y, z):
    return np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]], np.float32)

def scale_matrix(s):
    return np.array([[s, 0, 0, 0],
                     [0, s, 0, 0],
                     [0, 0, s, 0],
                     [0, 0, 0, 1]], np.float32)

def scale_matrix3(sx, sy ,sz):
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]], np.float32)

def rotation_x_matrix(angle):
    cos_value = cos(radians(angle))
    sine_value = sin(radians(angle))
    return np.array([[1, 0, 0, 0],
                     [0, cos_value, -sine_value, 0],
                     [0, sine_value, cos_value, 0],
                     [0, 0, 0, 1]], np.float32)

def rotation_y_matrix(angle):
    cos_value = cos(radians(angle))
    sine_value = sin(radians(angle))
    return np.array([[cos_value, 0, sine_value, 0],
                     [0, 1, 0, 0],
                     [-sine_value, 0, cos_value, 0],
                     [0, 0, 0, 1]], np.float32)

def rotation_z_matrix(angle):
    cos_value = cos(radians(angle))
    sine_value = sin(radians(angle))
    return np.array([[cos_value, -sine_value, 0, 0],
                     [sine_value, cos_value, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]], np.float32)

def rotation_around_axis(angle, axis):
    cos_value = cos(radians(angle))
    sine_value = sin(radians(angle))
    axis = axis.normalize()
    ux2 = axis.x * axis.x
    uy2 = axis.y * axis.y
    uz2 = axis.z * axis.z
    return np.array(
        [[cos_value + (1 - cos_value) * ux2, (1 - cos_value) * axis.y * axis.x - sine_value * axis.z, (1 - cos_value) * axis.z * axis.x + sine_value * axis.y, 0],
         [(1 - cos_value) * axis.y * axis.x + sine_value * axis.z, cos_value + (1 - cos_value) * uy2, (1 - cos_value) * axis.z * axis.y - sine_value * axis.x, 0],
         [(1 - cos_value) * axis.x * axis.z - sine_value * axis.y, (1 - cos_value) * axis.y * axis.z + sine_value * axis.x, cos_value + (1 - cos_value) * uz2, 0],
         [0, 0, 0, 1]], np.float32)

def translate(matrix, x, y, z):
    trans = translation_matrix(x, y, z)
    return matrix @ trans

def scale(matrix, s):
    scale1D = scale_matrix(s)
    return matrix @ scale1D

def scale3(matrix, sx, sy, sz):
    scale3D = scale_matrix3(sx, sy, sz)
    return matrix @ scale3D

def rotate(matrix, angle, axis, local=True):
    rot = identity_matrix()
    if axis == "X":
        rot = rotation_x_matrix(angle)
    elif axis == "Y":
        rot = rotation_y_matrix(angle)
    elif axis == "Z":
        rot = rotation_z_matrix(angle)

    if local:
        return matrix @ rot
    else:
        return rot @ matrix

def rotate_mesh(matrix, angle, axis, local=True):
    rot = rotation_around_axis(angle, axis)
    if local:
        return matrix @ rot
    else:
        return rot @ matrix