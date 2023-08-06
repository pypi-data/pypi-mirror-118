# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 13:09:10 2017

@author: Yongguang Gong
"""

from __future__ import absolute_import

__name__ = "optprc"
__version__ = "0.2.0"

from .IRS import IRSPricer_class as IRSPricer
from .Vanilla import VanillaPricer_Class as VanillaPricer
from .Asian import AsianPricer_class as AsianPricer
from .iData import save_json, read_json
from .iDate import timefn
from .cdspricing import discountCurve, spreadCurve
from .cdspricing import CDS as jpmcds

__all__ = ["IRSPricer","VanillaPricer","AsianPricer","timefn","save_json","read_json", 
           "discountCurve", "spreadCurve", "jpmcds"]