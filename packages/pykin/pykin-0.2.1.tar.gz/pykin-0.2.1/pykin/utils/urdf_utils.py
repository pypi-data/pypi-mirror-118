from pykin.utils.kin_utils import convert_string_to_narray, LINK_TYPES

class URDF_Link:
    def __init__(self):
        pass

    @staticmethod
    def set_visual(elem_link, link_frame):   
        for elem_visual in elem_link.findall('visual'):
            URDF_Link.set_visual_origin(elem_visual, link_frame)
            URDF_Link.set_visual_geometry(elem_visual, link_frame)
            URDF_Link.set_visual_color(elem_visual, link_frame)

    @staticmethod
    def set_collision(elem_link, link_frame):
        for elem_collision in elem_link.findall('collision'):
            URDF_Link.set_collision_origin(elem_collision, link_frame)
            URDF_Link.set_collision_geometry(elem_collision, link_frame)

    @staticmethod
    def set_visual_origin(elem_visual, frame):
        elem_origin = elem_visual.find('origin')
        frame.link.visual.offset.pos = convert_string_to_narray(elem_origin.attrib.get('xyz'))
        frame.link.visual.offset.rot = convert_string_to_narray(elem_origin.attrib.get('rpy'))

    @staticmethod
    def set_visual_geometry(elem_visual, frame):
        elem_geometry = elem_visual.find('geometry')
        for shape_type in LINK_TYPES:
            for shapes in elem_geometry.findall(shape_type):
                URDF_Link.convert_visual(shapes, frame)

    @staticmethod
    def set_visual_color(elem_visual, frame):
        for elem_matrial in elem_visual.findall('material'):
            elem_color = elem_matrial.find('color')
            rgba = convert_string_to_narray(elem_color.attrib.get('rgba'))
            frame.link.visual.gparam['color'] = {elem_matrial.get('name') : rgba}
    
    @staticmethod
    def convert_visual(shapes, frame):
        if shapes.tag == "box":
            frame.link.visual.gtype = shapes.tag
            frame.link.visual.gparam = {"size" : convert_string_to_narray(shapes.attrib.get('size', None))}
        elif shapes.tag == "cylinder":
            frame.link.visual.gtype = shapes.tag
            frame.link.visual.gparam = {"length" : shapes.attrib.get('length', 0),
                                        "radius" : shapes.attrib.get('radius', 0)}
        elif shapes.tag == "sphere":
            frame.link.visual.gtype = shapes.tag
            frame.link.visual.gparam = {"radius" : shapes.attrib.get('radius', 0)}
        elif shapes.tag == "mesh":
            frame.link.visual.gtype = shapes.tag
            frame.link.visual.gparam = {"filename" : shapes.attrib.get('filename', None)}
        else:
            frame.link.visual.gtype = None
            frame.link.visual.gparam = None

    @staticmethod
    def set_collision_origin(elem_collision, frame):
        elem_origin = elem_collision.find('origin')
        frame.link.collision.offset.pos = convert_string_to_narray(elem_origin.attrib.get('xyz'))
        frame.link.collision.offset.rot = convert_string_to_narray(elem_origin.attrib.get('rpy'))

    @staticmethod
    def set_collision_geometry(elem_collision, frame):
        elem_geometry = elem_collision.find('geometry')
        for shape_type in LINK_TYPES:
            for shapes in elem_geometry.findall(shape_type):
                URDF_Link.convert_collision(shapes, frame)

    @staticmethod
    def convert_collision(shapes, frame):
        if shapes.tag == "box":
            frame.link.collision.gtype = shapes.tag
            frame.link.collision.gparam = {"size" : convert_string_to_narray(shapes.attrib.get('size', None))}
        elif shapes.tag == "cylinder":
            frame.link.collision.gtype = shapes.tag
            frame.link.collision.gparam = {"length" : shapes.attrib.get('length', 0),
                                        "radius" : shapes.attrib.get('radius', 0)}
        elif shapes.tag == "sphere":
            frame.link.collision.gtype = shapes.tag
            frame.link.collision.gparam = {"radius" : shapes.attrib.get('radius', 0)}
        elif shapes.tag == "mesh":
            frame.link.collision.gtype = shapes.tag
            frame.link.collision.gparam = {"filename" : shapes.attrib.get('filename', None)}
        else:
            frame.link.collision.gtype = None
            frame.link.collision.gparam = None


class URDF_Joint:
    def __init__(self):
        pass
    
    @staticmethod
    def set_origin(elem_joint, frame):
        elem_origin = elem_joint.find('origin')
        if elem_origin is not None:
            frame.joint.offset.pos = convert_string_to_narray(
                elem_origin.attrib.get('xyz'))
            frame.joint.offset.rot = convert_string_to_narray(
                elem_origin.attrib.get('rpy'))
    
    @staticmethod
    def set_axis(elem_joint, frame):
        elem_axis = elem_joint.find('axis')
        if elem_axis is not None:
            frame.joint.axis = convert_string_to_narray(
                elem_axis.attrib.get('xyz'))

    @staticmethod
    def set_limit(elem_joint, frame):
        elem_limit = elem_joint.find('limit')
        if elem_limit is not None:
            if "lower" in elem_limit.attrib:
                frame.joint.limit[0] = float(elem_limit.attrib["lower"])
            if "upper" in elem_limit.attrib:
                frame.joint.limit[1] = float(elem_limit.attrib["upper"])