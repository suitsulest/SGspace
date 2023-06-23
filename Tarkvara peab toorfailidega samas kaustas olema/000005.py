import cv2
import numpy as np
import glob
import os

# v3.00

# correction values, set to 0 to disable
gamma       = 1     # 0 = OFF, 1 = ON
brightness  = 10    # 0 to 255
blur        = 0     # 1 = none, 2 = 2x2 averaging
contrast    = 2     # 0 to 10

# setup directories
Home_Files  = []
Home_Files.append(os.getlogin())

for i in range(176):
    files = glob.glob(f"image{i}")
    files.sort()
    valid = 0

    rows = 2160
    cols = 3840

    gamma_table = [0,1,3,6,9,10,12,15,17,19,21,24,26,28,30,33,35,37,39,42,44,46,48,51,53,55,57,60,62,64,66,68,70,
             72,74,76,78,80,82,84,87,89,91,93,95,97,99,101,103,106,108,110,111,112,114,116,118,119,121,123,125,127,
             128,130,132,134,135,137,139,141,143,144,146,148,150,152,153,154,156,157,159,160,162,163,165,166,168,169,
             171,172,174,175,177,178,180,181,183,184,186,187,189,190,191,192,193,194,195,196,197,198,199,201,202,
             203,204,205,206,207,208,209,210,212,213,214,215,216,216,217,218,218,219,220,221,221,222,223,224,224,
             225,226,227,227,228,229,230,230,231,232,233,233,234,234,234,235,235,236,236,237,237,238,238,239,239,
             240,240,241,241,242,242,243,243,244,244,245,245,246,246,246,246,246,247,247,247,247,248,248,248,248,
             248,249,249,249,249,250,250,250,250,251,251,251,252,252,252,252,252,252,252,252,252,252,252,252,252,
             252,252,252,252,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,254,254,254,254,
             254,254,254,254,254,254,254,254,254,254,254,254,255,255,255,255,255,255,255]


    if len(files) > 0:
        for x in range(0,len(files)):
            # Open raw file
            f = open(files[x],'rb')
            image = np.fromfile(f, np.uint8, cols * rows)
            f.close()
            # check size
            
            valid = 2
            
       
            # process if a valid size
            if valid > 0:
                # trim off 
                
                # extract data
                if valid == 2:
                    A = image.reshape(cols,rows)
                    #A = image.reshape(int(image.size/3),3)
                    #A  = np.delete(A, 2, 1)

                F  = A.reshape(rows,cols)
                C  = A.reshape(int(rows/2),int(cols*2))
                D  = np.split(C, 2, axis=1)
                H  = D[0].reshape(int(D[0].size/2),2)
                I  = np.split(H, 2, axis=1)
                b  = I[0].reshape(int(rows/2),int(cols/2))
                g0 = I[1].reshape(int(rows/2),int(cols/2))
                L  = D[1].reshape(int(D[0].size/2),2)
                M  = np.split(L, 2, axis=1)
                g1 = M[0].reshape(int(rows/2),int(cols/2))
                r  = M[1].reshape(int(rows/2),int(cols/2))

                # some basic colour correction
                Red   = r * 1
                Blue  = b * 1
                Green = ((g0/2) + (g1/2)) * 0.7
                Green = Green.astype(np.uint8)

                # combine B,G,R
                BGR=np.dstack((Blue,Green,Red)).astype(np.uint8)
                res = cv2.resize(BGR, dsize=(cols,rows), interpolation=cv2.INTER_CUBIC)

                # split res into Y,Cr,Cb
                res_rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                res_ycbcr = cv2.cvtColor(res_rgb, cv2.COLOR_RGB2YCrCb)
                Y, Cr, Cb = cv2.split(res_ycbcr)

                # apply blurring
                if blur > 1:
                    F = cv2.blur(F,(blur,blur))

                # split rgb into Y,Cr,Cb
                rgb = cv2.cvtColor(F, cv2.COLOR_BGR2RGB)
                ycbcr = cv2.cvtColor(rgb, cv2.COLOR_RGB2YCrCb)
                Y1, Cr1, Cb1 = cv2.split(ycbcr)

                # combine Y1 from rgb and Cr an Cb from res
                image_merge = cv2.merge([Y1,Cr,Cb])
                image2 = cv2.cvtColor(image_merge, cv2.COLOR_YCrCb2BGR)

                # save output uncorrected
                fname = files[x].split('.')
                cv2.imwrite(fname[0] + "U.tif", image2)
                result = cv2.resize(image2, dsize=(int(cols/6),int(rows/6)), interpolation=cv2.INTER_CUBIC)
                cv2.imshow('Uncorrected Output',result)
               
                # adjust gamma
                if gamma != 0:
                    lookUpTable = np.empty((1,256), np.uint8)
                    for i in range(256):
                       lookUpTable[0,i] = gamma_table[i]
                    image2 = cv2.LUT(image2, lookUpTable)
                
                # adjust contrast
                if contrast != 0:
                    lab= cv2.cvtColor(image2, cv2.COLOR_BGR2LAB)
                    l_channel, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=contrast, tileGridSize=(8,8))
                    cl = clahe.apply(l_channel)
                    limg = cv2.merge((cl,a,b))
                    image2 = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                # adjust brightness
                if brightness != 0:
                    image2 = cv2.convertScaleAbs(image2, alpha=1, beta=brightness)
                
                # save output
                fname = files[x].split('.')
                cv2.imwrite(fname[0] + "C.tif", image2)

                # show corrected result
                result = cv2.resize(image2, dsize=(int(cols/6),int(rows/6)), interpolation=cv2.INTER_CUBIC)
                cv2.imshow('Corrected Output',result)
                
        
        
            # wait for a key press
            #cv2.waitKey()
        cv2.destroyAllWindows()
