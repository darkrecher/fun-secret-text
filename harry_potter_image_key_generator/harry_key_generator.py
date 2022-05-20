import numpy as np
import cv2

wing_size = (299, 199)

HARKEY_ELEMENT_INFOS = {
    "left_wing": {
        "size_xy": (299, 199),
        "uplefts_xy": (
            (1, 1),
            (1, 201),
            (1, 401),
        ),
    },
    "extr_down": {
        "size_xy": (162, 134),
        "uplefts_xy": (
            (301, 1),
            (301, 136),
            (301, 271),
            (301, 406),
        ),
    },
    "extr_up": {
        "size_xy": (216, 157),
        "uplefts_xy": (
            (464, 1),
            (464, 159),
            (464, 317),
            (464, 475),
        ),
    },
    "middle": {
        "size_xy": (158, 381),
        "uplefts_xy": (
            (681, 1),
            (840, 1),
            (999, 1),
        ),
    },
}


HARKEY_ELEM_OFFSETS = {
    "left_wing": (0, 110),
    "right_wing": (313, 110),
    "extr_up": (198, 0),
    "middle": (227, 157),
    "extr_down": (208, 538),
}

HARKEY_SIZE_XY = (612, 672)


def prepare_harkey_elements(atlas_img):
    harkey_elements = {}
    for elem_name, elem_infos in HARKEY_ELEMENT_INFOS.items():
        images_and_masks = []
        size_xy = elem_infos["size_xy"]
        for upleft_xy in elem_infos["uplefts_xy"]:
            elem_img = take_image_part(atlas_img, upleft_xy, size_xy)
            byte_mask = cv2.inRange(
                elem_img, np.array([1, 1, 1]), np.array([255, 255, 255])
            )
            images_and_masks.append((elem_img, byte_mask))
        harkey_elements[elem_name] = images_and_masks

    nb_img_per_elem = []
    for elem_name in sorted(list(HARKEY_ELEMENT_INFOS.keys())):
        nb_img = len(harkey_elements[elem_name])
        nb_img_per_elem.append((elem_name, nb_img))

    images_and_masks_right_wing = []
    for img_left_wing, mask in harkey_elements["left_wing"]:
        img_right_wing = img_left_wing[:, ::-1]
        byte_mask = cv2.inRange(
            img_right_wing, np.array([1, 1, 1]), np.array([255, 255, 255])
        )
        images_and_masks_right_wing.append((img_right_wing, byte_mask))
    harkey_elements["right_wing"] = images_and_masks_right_wing

    return harkey_elements, nb_img_per_elem


def take_image_part(source_img, upleft_xy, size_xy):
    upleft_x, upleft_y = upleft_xy
    size_x, size_y = size_xy
    return source_img[upleft_y : upleft_y + size_y, upleft_x : upleft_x + size_x]


def blit_img(source_img, dest_img, dest_upleft_xy, byte_mask=None):
    dest_upleft_x, dest_upleft_y = dest_upleft_xy
    size_y, size_x = source_img.shape[:2]

    if byte_mask is None:

        dest_img[
            dest_upleft_y : dest_upleft_y + size_y,
            dest_upleft_x : dest_upleft_x + size_x,
        ] = source_img

    else:

        dest_img[
            dest_upleft_y : dest_upleft_y + size_y,
            dest_upleft_x : dest_upleft_x + size_x,
        ] = cv2.bitwise_and(
            source_img,
            dest_img[
                dest_upleft_y : dest_upleft_y + size_y,
                dest_upleft_x : dest_upleft_x + size_x,
            ],
            mask=byte_mask,
        )


def build_harkey(harkey_num_id, harkey_elements, nb_img_per_elem):
    HARKEY_SIZE_X, HARKEY_SIZE_Y = HARKEY_SIZE_XY
    harkey_img = np.full((HARKEY_SIZE_Y, HARKEY_SIZE_X, 3), 255, np.uint8)

    for elem_name, nb_img in nb_img_per_elem:
        current_elem_index = harkey_num_id % nb_img
        print(elem_name, current_elem_index)
        elem_img, byte_mask = harkey_elements[elem_name][current_elem_index]
        offset_xy = HARKEY_ELEM_OFFSETS[elem_name]
        blit_img(elem_img, harkey_img, offset_xy, byte_mask)

        if elem_name == "left_wing":
            print("right_wing", current_elem_index)
            elem_name = "right_wing"
            elem_img, byte_mask = harkey_elements[elem_name][current_elem_index]
            offset_xy = HARKEY_ELEM_OFFSETS[elem_name]
            blit_img(elem_img, harkey_img, offset_xy, byte_mask)

        current_elem_index //= nb_img

    return harkey_img


def main():
    import random

    print("coucou")
    atlas_img = cv2.imread("harkeys.png")
    harkey_elements, nb_img_per_elem = prepare_harkey_elements(atlas_img)
    harkey = build_harkey(random.randrange(0, 144), harkey_elements, nb_img_per_elem)
    cv2.imshow("pouet", harkey)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
