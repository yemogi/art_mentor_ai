# /ai/images/input/images_01.png, images_02.png 파일 불러와서.
# 정면으로 보정하기.

# 보정된 파일은 output 폴더에 저장하기.
import cv2
import numpy as np


def correct_perspective(image, corners, width, height):
    """네 모서리 좌표를 이용해 이미지를 직사각형으로 보정합니다.

    corners 순서: 왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래
    width, height: 결과 이미지의 가로·세로 픽셀 수
    """
    source_points = np.array(corners, dtype=np.float32)

    if source_points.shape != (4, 2):
        raise ValueError("모서리 좌표는 (x, y) 네 쌍이어야 합니다.")

    if width < 2 or height < 2:
        raise ValueError("결과 이미지의 가로와 세로는 2 이상이어야 합니다.")

    destination_points = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1],
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(
        source_points, destination_points
    )

    corrected = cv2.warpPerspective(
        image, matrix, (width, height)
    )

    return corrected