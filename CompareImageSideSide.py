#!/usr/bin/env python
# coding: utf-8
#coded by P C Tiwari


import os, sys, optparse
import numpy as np
import PIL.Image,PIL.ImageDraw,PIL.ImageFont

##to run
## python CompareImageSideSide.py -f firstDir -s secondDir --f_txt firstDirTxt --s_txt secondDirTxt

usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)
parser.add_option("-f", "--first_dir", dest="FirstDir", default="firstDir")
parser.add_option("-s", "--second_dir", dest="SecondDir", default="secondDir")
parser.add_option("-t", "--third_dir", dest="ThirdDir", default="thirdDir")

parser.add_option("-x", "--f_txt", dest="FirstDirTxt", default="firstDirTxt")
parser.add_option("-y", "--s_txt", dest="SecondDirTxt", default="secondDirTxt")
parser.add_option("-z", "--t_txt", dest="ThirdDirTxt", default="thirdDirTxt")

(options, args) = parser.parse_args()

regions = ['SR_1b','SR_2b','ZmumuCR_1b','ZmumuCR_2b','ZeeCR_1b','ZeeCR_2b','TopmunuCR_1b','TopmunuCR_2b','WmunuCR_1b','WmunuCR_2b','WenuCR_1b','WenuCR_2b']
list_comp=[]
for reg in regions:
    listfiles_1 = [f for f in os.listdir(options.FirstDir+'/bbDMPng/'+reg)]
    listfiles_2 = [f for f in os.listdir(options.SecondDir+'/bbDMPng/'+reg)]
    list_temp =[]
    for i in listfiles_1:
        for j in listfiles_2:
            if ('_MET_' in i and '_MET_' in j) or ('_Recoil_' in i and '_Recoil_' in j):
                im_list=[options.FirstDir+'/bbDMPng/'+reg+'/'+i,options.SecondDir+'/bbDMPng/'+reg+'/'+j]
                list_temp.append(im_list)
        list_comp+=list_temp

for reg in regions:
    if not os.path.exists('compared_files/bbDMPng/'+reg): os.makedirs('compared_files/bbDMPng/'+reg)
    if not os.path.exists('compared_files/bbDMPdf/'+reg): os.makedirs('compared_files/bbDMPdf/'+reg)

for im in list_comp:
    imgs = [ PIL.Image.open(i) for i in im ]
    draw = [PIL.ImageDraw.Draw(i) for i in imgs]
    fonts = PIL.ImageFont.truetype('/Library/Fonts/Arial.ttf', 30)
    draw[0].text((175,100), options.FirstDirTxt, font=fonts, fill=(0, 0, 0))
    draw[1].text((175,100), options.SecondDirTxt, font=fonts, fill=(0, 0, 0))

    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    # save that beautiful picture
    imgs_comb = PIL.Image.fromarray(imgs_comb)
    reg_name = im[1].split('/')[-2]
    image_name=(im[1].split('/')[-1]).split('.')[0]
    print (reg_name,image_name )
    imgs_comb.save( 'compared_files/bbDMPng/'+reg_name+'/'+image_name+'.png')
    imgs_comb.save( 'compared_files/bbDMPdf/'+reg_name+'/'+image_name+'.pdf')
