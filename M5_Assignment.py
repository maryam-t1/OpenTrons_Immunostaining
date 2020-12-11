# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:52:40 2020

@author: 91948
"""

from opentrons import simulate
import math
import time


metadata = {'apiLevel': '2.8'}
protocol = simulate.get_protocol_api('2.8')
tempdeck = protocol.load_module('temperature module gen2', 4)

#Labware
plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 1)
tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 5)
reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 3)

cool_reagents = tempdeck.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap')
tempdeck.set_temperature(4) # set block to 4°C
tempdeck.await_temperature(4)
print("Cooling block temperature =",tempdeck.temperature,"°C")

#pipettes
p300_1 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[tiprack_1])
p300_2 = protocol.load_instrument('p300_multi', 'left', tip_racks=[tiprack_2])
protocol.max_speeds['Z'] = 10


samples = int(input("Enter number of samples "))
#assuming samples are filled column-wise
#A12 of reservoir is used to dispense

final_row,final_col = str((plate.wells(samples)[0]))[0],int(str((plate.wells(samples)[0]))[1])

def add_reagent(x,vol):
    tic = time.perf_counter()
    for i in plate.rows_by_name().keys():
        if(i==final_row):
            p300_1.distribute(vol, reservoir.wells_by_name()[x], plate.rows_by_name()[i][0:final_col])
            break
        else:
            p300_1.distribute(vol, reservoir.wells_by_name()[x], plate.rows_by_name()[i][0:12])
    toc = time.perf_counter()
    return toc-tic
def rem_reagent(x,vol):
    tic = time.perf_counter()
    for i in plate.rows_by_name().keys():
        if(i==final_row):
            p300_1.consolidate(vol, plate.rows_by_name()[i][0:final_col], reservoir.wells_by_name()[x])
            break
        else:
            p300_1.consolidate(vol, plate.rows_by_name()[i][0:12], reservoir.wells_by_name()[x])
    toc = time.perf_counter()
    return toc-tic

def add_ab(x,vol):
    tic = time.perf_counter()
    for i in plate.wells():
        if(i==plate.wells(samples)):
            break
        else:
            p300_1.transfer(vol,reservoir[x], i, touch_tip=True, blow_out=True, blowout_location='destination well', new_tip='always') 
    
    toc = time.perf_counter()
    return toc-tic   

def add_reagent_m(x,vol):
    tic = time.perf_counter()
    p300_2.distribute(vol, reservoir.wells_by_name()[x], plate.rows_by_name()['A'][:final_col],new_tip='once')
    toc = time.perf_counter()
    return toc-tic

def rem_reagent_m(x,vol):
    tic = time.perf_counter()
    p300_2.consolidate(vol, plate.rows_by_name()['A'][:final_col], reservoir.wells_by_name()[x])
    toc = time.perf_counter()
    return toc-tic
                
    
#Each function takes reagent location and volume as parameters            
#Each function does the particular task for all of the samples and returns the time taken as output

#Aspirate medial
rem_reagent_m('A1',200)

#Rinse with PBST(From reservoir 3)
add_reagent_m('A3',200)
rem_reagent_m('A1',200)

# #Add/Remove PFA(From reservoir 4)
# t = add_reagent_m('A4',200)
# protocol.delay(10*60-t)
# rem_reagent_m('A1',200)

# #Wash with PBS(From reservoir 2)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)

# #Add/Remove PBS PBS/0.1% Triton X-100(From reservoir 5)
# t = add_reagent_m('A5', 200)
# protocol.delay(10*60-t)
# rem_reagent_m('A1',200)

# #Wash with PBS(From reservoir 2)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)
# add_reagent_m('A2',200)
# rem_reagent_m('A1',200)

# #Add/Remove Blocking solution (From reservoir 6)
# t = add_reagent_m('A6', 200)
# protocol.delay(30*60-t)
# rem_reagent_m('A6',200)

# #Add/Remove A.B solution (From reservoir 6)



for line in protocol.commands(): 
        print(line)

            