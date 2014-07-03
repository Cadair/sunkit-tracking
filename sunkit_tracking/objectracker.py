# -*- coding: utf-8 -*-
"""
This file contains the core code for the object tracker.
"""

import skimage.measure

from .labelledobjects import LabelledObjectCollection

class LabelledObjectTracker(object):
    """
    Track labelled objects through a series of images. Will modify the inputted
    labelled images.
    """
    
    def __init__(self, image_series, labelled_series, **kwargs):
        if image_series.shape != labelled_series.shape:
            raise TypeError("The image series and the labelled series must be the same shape")

        self.image_series = image_series
        self.labelled_series = labelled_series
    
    def pre_tracking(self, i1, i2):
        """
        Run this code before comparing two frames.
        
        Parameters
        ----------
        i1, i2 : int
            The indexes of the frames being compared
        """
    
    def post_tracking(self, i1, i2):
        """
        Run this code after comparing two frames.
        
        Parameters
        ----------
        i1, i2 : int
            The indexes of the frames that have been compared
        """
    
    def compare_images(self, i1, i2):
        """
        The comparison method, modifies the images in place
        """
    
    def track_objects(self):
        """
        Run the tracking code on the series of images.
        
        Returns
        -------
        labelledobjects : `~sunkit_tracking.LabelledObjectCollection`
            A collection of all object found in the image series
        """

        obj_collection = LabelledObjectCollection()
        for k, (im, label_im) in enumerate(zip(self.image_series,
                                               self.labelled_series)):

            self.pre_tracking(k, k+1)

            self.compare_images(k, k+1)

            all_rprops = skimage.measure.regionprops(label_im, im)
            obj_collection.add_frame(k, all_rprops)

            self.post_tracking(k, k+1)
        
        return obj_collection


class OverlapObjectTracker(LabelledObjectTracker):
    """
    Track objects through a series of images via their overlap with the 
    previous frame
    """
        
    def compare_images(self, i1, i2):
        self.labelled_series[i1], self.labelled_series[i2] = \
                        skimage.measure.label_match(self.labelled_series[i1],
                                                    self.labelled_series[i2],
                                                    remove_duplicates=True)