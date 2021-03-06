#!python3

# %%
import os
proposal_scripts_dir = os.listdir()
# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Proposal_Scripts')

# %%
# import the necessary packages
import cv2

# load the image_1 and convert it to grayscale
template_name = 'Bottle_Template2.jpg'
file_path = '/root/base/development/MASINT_Proposal_Work'\
            '/Media_Files/Initial/Bottle/'
jpg_files = os.listdir(file_path)
images = []
template_image = []
ImageNumber = 0
for ImageFile in jpg_files:
    TemporaryImage = []
    if ImageFile == template_name:
        TemporaryImage = cv2.imread('{0}{1}'.format(file_path, ImageFile))
        # Can read directly to grayscale if you never need the color by doing below
        # but then it throws and error when trying to convert and you dont have
        # the original so just skip in the future
        # TemporaryImage = cv2.imread('{0}{1}'.format(file_path, ImageFile), cv2.IMREAD_GRAYSCALE)
        # Equivalently
        # TemporaryImage = cv2.imread('{0}{1}'.format(file_path, ImageFile), 0)
        template_image.append(
                          [TemporaryImage,
                           cv2.cvtColor(TemporaryImage, cv2.COLOR_BGR2GRAY)]
                             )
    else:
        TemporaryImage = cv2.imread('{0}{1}'.format(file_path, ImageFile))
        images.append(
                  [ImageNumber,
                   TemporaryImage,
                   cv2.cvtColor(TemporaryImage, cv2.COLOR_BGR2GRAY)]
                     )
        ImageNumber = ImageNumber + 1

# %%
template_image_width, template_image_height = template_image[0][0].shape[-2::-1]
# %%
for ImageNumber, RGBImage, GrayImage in images:
    # print(ImageNumber)
    result = cv2.matchTemplate(images[ImageNumber][2],
                               template_image[0][1],
                               cv2.TM_CCOEFF_NORMED)
    threshold = 0.3
    row_locations = []
    column_locations = []
    points = []
    for Row, RowValue in enumerate(result):
        for Column, Value in enumerate(RowValue):
            if Value >= threshold:
                row_locations.extend([Row])
                column_locations.extend([Column])
                points.append([Column, Row])
    locations = (row_locations, column_locations)
    #locations = np.where(result >= threshold)
    #points = zip(*locations[::-1])
    for point in points:
        cv2.rectangle(images[ImageNumber][1],
                      tuple(point),
                      (point[0]+int(template_image_width/2),
                       point[1]+int(template_image_height/2)),
                       (0, 0, 255),
                       1)

    cv2.imshow(str(ImageNumber), images[ImageNumber][1])
# %%
image_1 = cv2.imread("0020.jpg")
image_2 = cv2.imread("0021.jpg")
image_3 = cv2.imread("0018.jpg")
gray_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)
gray_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
gray_3 = cv2.cvtColor(image_3, cv2.COLOR_BGR2GRAY)
cv2.imshow("Original", image_1)

# %%

# initialize the AKAZE descriptor, then detect keypoints and extract
# local invariant descriptors from the image_1
detector = cv2.AKAZE_create()
(kps_1, descs_1) = detector.detectAndCompute(image_1, None)
(kps_2, descs_2) = detector.detectAndCompute(image_2, None)
(kps_3, descs_3) = detector.detectAndCompute(image_3, None)
print("keypoints: {}, descriptors: {}".format(len(kps_1), descs_1.shape))
print("keypoints: {}, descriptors: {}".format(len(kps_2), descs_2.shape))
print("keypoints: {}, descriptors: {}".format(len(kps_3), descs_3.shape))

# %%
# Match the features
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# matches = bf.knnMatch(descs_1, descs_2, k=2)
matches = bf.knnMatch(descs_1, descs_2, k=1)

# %%
good_matches = matches
# %%
# Test the Ratio
good_matches = []
Ratio = 0.9
for m, n in matches:
    if m.distance < n.distance*Ratio:
        good_matches.append([m])

# %%
number_of_matches_to_draw = 10 # len(good_matches)
good_matches_drawn = good_matches[0:number_of_matches_to_draw]
image_with_matches = cv2.drawMatchesKnn(image_1, kps_1, image_2, kps_2, good_matches_drawn, None, flags=2)
cv2.imshow('Matches', image_with_matches)

# %%
number_of_keypoints_to_draw = 10
kps_drawn = kps[0:number_of_keypoints_to_draw]
# draw the keypoints and show the output image_1
cv2.drawKeypoints(image_1, kps_drawn, image_2, (0, 255, 0))
cv2.imshow("Output", image_1)
cv2.waitKey(0)
