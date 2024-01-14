import cv2
import imutils


def convert_point_to_point_to_xyhw(box):
    return box[0][0], box[0][1], box[1][0] - box[0][0], box[1][1] - box[0][1]


def convert_xyhw_to_point_to_point(box):
    return [box[0], box[1]], [box[0] + box[2], box[1] + box[3]]


def overlap(source, target):
    """returns true if the two boxes overlap"""

    # TODO: Maybe add margin

    # unpack points
    ret = True
    tl1, br1 = source
    tl2, br2 = target

    # checks
    if tl1[0] >= br2[0] or tl2[0] >= br1[0]:
        ret = False

    if tl1[1] >= br2[1] or tl2[1] >= br1[1]:
        ret = False

    return ret


def merge_boxes(source, target):
    ret = []
    tl1, br1 = source
    tl2, br2 = target

    ret.append([min(tl1[0], tl2[0]), min(tl1[1], tl1[1])])
    ret.append([max(br1[0], br2[0]), max(br1[1], br2[1])])

    return ret


def transform_points_list_to_boxes_tuple(blist):

    ret = []

    for box in blist:
        ret.append(convert_point_to_point_to_xyhw(box))

    return tuple(ret)


def transform_boxes_tuple_to_points_list(tuple):

    ret = []

    for box in tuple:
        ret.append(convert_xyhw_to_point_to_point(box))

    return ret


def group_overlapped_boxes(input_list):

    ret = []
    boxes = transform_boxes_tuple_to_points_list(input_list)
    prev_box = [[0, 0], [0, 0]]

    for box in boxes:
        if overlap(prev_box, box):
            prev_box = merge_boxes(prev_box, box)

            if box == boxes[-1]:
                ret.append(prev_box)
        else:
            ret.append(prev_box)
            prev_box = box

            # If we are at the end and the two boxes are not overlapped
            if box == boxes[-1]:
                ret.append(box)

    # Remove the first element that we added for the comparison
    ret.remove([[0, 0], [0, 0]])

    return transform_points_list_to_boxes_tuple(ret)


def remove_small_boxes(b_list, min_w=15, min_h=15):

    ret = []

    for box in b_list:
        if box[2] >= min_w or box[3] >= min_h:
            ret.append(box)

    return ret


def adjust_padding(distance):

    ret = (0, 0)
    padding_side = distance / 2

    if (padding_side - math.trunc(padding_side)) == 0:
        new_dis = distance / 2
        ret = (int(new_dis), int(new_dis))
    else:
        new_dis = distance / 2
        ret = (int(new_dis), int(new_dis+1))

    return ret


def trim_character_rois(blist, image):

    ret = []

    for box in blist:
        (x, y, w, h) = box

        roi = image[y:y + h, x:x + w]
        roi_binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        (height, width) = roi_binary.shape

        if height > width:
            roi_binary = imutils.resize(roi_binary, height=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(int(45 - roi_binary.shape[1]))
            print(f"{roi_binary.shape} | {padding} | {width} | {height}")
            roi_binary = cv2.copyMakeBorder(roi_binary, top=0, bottom=0, left=padding[0], right=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
        else:
            roi_binary = imutils.resize(roi_binary, width=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(45 - roi_binary.shape[0])
            print(f"{roi_binary.shape} | {padding}")
            roi_binary = cv2.copyMakeBorder(roi_binary, left=0, right=0, top=padding[0], bottom=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))

        ret.append(roi_binary)

    return ret

