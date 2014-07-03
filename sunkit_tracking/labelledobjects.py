# -*- coding: utf-8 -*-
"""
This file contains the classes to represent labelled objects throughout their
lifetimes and collections of those objects
"""

class LabelledObject(object):
    """
    This represents a labelled object over many different frames.
    """
    
    def __init__(self, label):
        self.label = label
        self._frames = set()
        self._regionprops = []
    
    def __hash__(self):
        return self.label

    def __repr__(self):
        return "<LabelledObject Instance Label:%i>"%self.label
    
    @property
    def frames(self):
        return self._frames
    
    @property
    def regionprops(self):
        return self._regionprops
    
    def add_frame(self, frameind, region_props):
        """
        Add a frame to the object, with it's regionprops instance
        """
        self._frames.add(frameind)
        self._regionprops.append(region_props)


class LabelledObjectCollection(list):
    """
    This holds many labelled objects.
    """
    def __contains__(self, item):
        return item in [a.label for a in self]

    def append(self, item):
        if not isinstance(item, LabelledObject):
            raise TypeError("A LabelledObjectCollection only holds LabelledObject objects")
        elif item.label in [a.label for a in self]:
            raise ValueError("An object with this label already exists in this collection")
        else:
            super(LabelledObjectCollection, self).append(item)
    
    def __setitem__(self, key, value):
        if not isinstance(value, LabelledObject):
            raise TypeError("A LabelledObjectCollection only holds LabelledObject objects")
        elif value.label in [a.label for a in self]:
            raise ValueError("An object with this label already exists in this collection")
        else:
            super(LabelledObjectCollection, self).__setitem__(key, value)

    def __getitem__(self, key):
        return super(LabelledObjectCollection, self).__getitem__([a.label for a in self].index(key))
    
    def add_frame(self, frameind, regionprops):
        """
        Add a frame to the collection. If a object with the label exists, add
        the frame to that object, if there is no object with the correct label
        add a new object with the frame as it's first frame.
        
        Parameters
        ----------
        frameind : int
            The index of the frame
        
        regionprops : list of `~skimage.measure._regionprops._RegionProperties` object
            The region properties for the frame.
        """
        
        for rprop in regionprops:
            if not rprop.label in self:
                self.append(LabelledObject(rprop.label))

            self[rprop.label].add_frame(frameind, rprop)
