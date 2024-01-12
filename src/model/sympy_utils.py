


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


def get_all_overlaps_for_box(boxes, bounds):
    """returns all overlapping boxes + itself"""

    overlaps = []
    for a in boxes:
        print(overlap(bounds, convert_xyhw_to_point_to_point(a)))
        if overlap(bounds, convert_xyhw_to_point_to_point(a)):
            overlaps.append(a)
            boxes.remove(a)

    if len(overlaps) > 0:
        overlaps.insert(0, bounds)

    return overlaps


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