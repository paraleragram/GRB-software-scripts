#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math


# In[7]:


def rebin(new_delta_t: float, start_bin: list, end_bin: list, cnt: list):
    """
    This function returns three lists: bin's new beginning, bin's new ending and new counts according to the new timescale
    
    Parameters: new_delta_t: float
                        New timescale in seconds.
                start_bin: list, array, etc
                        An array of data. Each element of the array is the beginning of a new bin. 
                        Usually corresponds to the first column of the time history.
                end_bin: list, array, etc
                        An array of data. Each element of the array is the of the bin. 
                        Usually corresponds to the second column of the time history.
                cnt: list, array, etc
                        An array of data. Each element corresponds to the counts in the i-th bin.
               
    Returns:    new_start_bin, new_end_bin, new_cnt
                        In fact, the time history is returned with a new resolution. 
                        Important: Only the part of the time history that can be made for this timescale is returned. 
                        If you want to get a time history with timescale = 4ms, then there will be no rebinning on the site
                        with timescale = 8ms and more, because from a physical point of view this operation does not make 
                        sense. The time history is returned for one energy channel. If you need to get time histories for 
                        all energy windows, use the function in the loop.
    Examples: 
    
    >>> T1 = [-0.512    T2 = [-0.510     G3 = [1.00
              -0.510          -0.508           0.00
              -0.508          -0.506           0.00
              -0.506          -0.504           0.00
              -0.504          -0.502           0.00
              -0.502          -0.500           2.01
              -0.500          -0.498           0.00
              -0.498]         -0.496]          3.02]
    >>>new_start_bin, new_end_bin, new_cnt = rebin(0.004, T1, T2, G3)
    T1 = [-0.512    T2 = [-0.518     G3 = [1.00
          -0.508          -0.504           0.00
          -0.504          -0.500           2.01
          -0.500]         -0.496]          3.02]
          
    """
    rest_delta_t = 0; rest_cnt = 0; current_cnt = 0; current_delta_t = 0; i = 0
#     start_bin = start_bin.tolist(); end_bin = end_bin.tolist(); cnt = cnt.tolist()
    new_start_bin = []; new_end_bin = []; new_cnt = []
    
#     f = open(str(grb_id) + '_' + str(int(new_delta_t*1000)) + '_' + str(channel) + '.thc','w')  #creating and opening a file for
    #writing
     
    while start_bin[i] < start_bin[-1]: #while loop runs through the values from the first row to the last row of the time
          #history
        delta_t = end_bin[i] - start_bin[i] #During the time history, the width of the bin can change, so it is necessary 
        #to count the new width of the bin for each next iteration
        if delta_t > new_delta_t: #If the width of the bin exceeds the new timescale, the cycle ends
            break
          
        new_start_bin.append(start_bin[i])
        new_end_bin.append(start_bin[i]+ new_delta_t)
#         f.write('%7.3f %8.3f' % (start_bin[i], start_bin[i]+ new_delta_t)) #Writing the start and end time of the bin to 
        #the file

        while round(current_delta_t + delta_t, 3) <= new_delta_t: #in this while, the addition of an integer number of 
            #counts is implemented (how many integer counts will "fit" into the selected timescale
            current_delta_t += delta_t
            current_cnt += cnt[i]
            i += 1
        if  round(new_delta_t - current_delta_t, 3) > 0: #This if implements the addition of a fractional number of counts
            current_cnt += (new_delta_t - current_delta_t)/delta_t*cnt[i]
            rest_delta_t = delta_t - (new_delta_t-current_delta_t)
            rest_cnt = (rest_delta_t)/delta_t*cnt[i] #the remainder of the recorded "fractional" count. it should be 
            #added to the "whole" counts in the next bin
            i += 1
        else: #else is important so that we add the remainder of the bin only when there is one
            rest_delta_t = 0
            rest_cnt = 0 
        
        new_cnt.append(round(current_cnt, 3))
#         f.write('%8.2f' %(current_cnt)) # write the number of counts in the bin to the file
#         f.write('\n') #switching to a new line
        current_cnt = rest_cnt #if "if" is True, then we remember the remainder of the bin. 
        #If False, we proceed to the next iteration without remainder
        current_delta_t = rest_delta_t
                   
#     f.close()
    return new_start_bin, new_end_bin, new_cnt

