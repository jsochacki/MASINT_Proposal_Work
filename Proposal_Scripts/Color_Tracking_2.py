#!/root/base/anaconda4p2/bin/python3
# %%
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

# %%
%%bash
cp /mnt/hgfs/BHD/L64/Source_Files/Video/* ./
# %%
input_video_file_name = 'Final_In'
temporary_file_extension = '_Temporary_File.avi'
output_video_file_name = 'Final_Out'
script_name = 'Color_Tracking_2.py'
# %%
%%bash -s $input_video_file_name $temporary_file_extension
#echo ${1::-4}
ffmpeg -i ./$1.mp4 -c:v mjpeg -q:v 3 -an ./$1$2
# Take video recorded in windows in mp4 format and make it a mjpeg format for
# OpenCV processing
# %%
def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
# %%

os.chdir('/root/base/development/MASINT_Proposal_Work/Media_Files/Initial/Video')

camera = cv2.VideoCapture('./{0}{1}'.format(input_video_file_name,temporary_file_extension))
fourcctext = decode_fourcc(camera.get(cv2.CAP_PROP_FOURCC))
fourccCode = cv2.VideoWriter_fourcc(*fourcctext)
out = cv2.VideoWriter(
                      './{0}{1}'.format(output_video_file_name,
                                        temporary_file_extension),
                      fourccCode,
                      30.0,
                      (640,480),
                      isColor=True)
print(out.isOpened())
# %%
# Use this to help find the hsv you want to bracket
# cv2.imshow('', cv2.inRange(cv2.cvtColor(cv2.imread('./cup2.jpg'), cv2.COLOR_BGR2HSV), (90, 40, 60), (115, 85, 90)))
lowrange = (100, 60, 180)
highrange = (255, 255, 255)
while(camera.isOpened()): # and success):
    ret, inframe = camera.read()
    if ret==True:
        image = inframe.copy()
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lowrange, highrange)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None        
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(image, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
                cv2.circle(image, center, 5, (0, 0, 255), -1)
                cv2.putText(image, '(X={0}, Y={1})'.format(int(x), int(y)),
                            (int(x), int(y)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0,
                            (0, 0, 255),
                            1)
          
        out.write(image)
        cv2.imshow('tracking', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# %%
camera.release()
out.release()
del camera
del out
cv2.destroyAllWindows()

# %%
%%bash -s $output_video_file_name $temporary_file_extension
ffmpeg -i ./$1$2 -r 25 -pix_fmt yuv420p -strict -2 -acodec aac -b:a 128k -vcodec libx264 -crf 21 -rc-lookahead 250 ./$1.mp4
# %%
%%bash
cp * /mnt/hgfs/BHD/L64/Source_Files/Video/

# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Proposal_Scripts')
# %%
%%bash -s $script_name
cp ./$1 /mnt/hgfs/BHD/L64/Source_Files/Video/
# Convert to mp4 for viewing on other computer like windows