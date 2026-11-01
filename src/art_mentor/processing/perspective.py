import cv2
import numpy as np


def correct_perspective(image, corners, width=None, height=None):
    """네 모서리로 원근 보정합니다.

    corners 순서: 왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래
    width, height를 생략하면 사진 속 변 길이로 출력 크기를 추정합니다.
    """
    source_points = np.array(corners, dtype=np.float32)

    if source_points.shape != (4, 2):
        raise ValueError("모서리 좌표는 (x, y) 네 쌍이어야 합니다.")

    if not np.isfinite(source_points).all():
        raise ValueError("모서리 좌표는 유한한 숫자여야 합니다.")

    # 좌표 네 개를 각각의 변수에 담기
    top_left, top_right, bottom_right, bottom_left = source_points

    # 두 점 사이의 직선거리 계산
    top_width = np.linalg.norm(top_right - top_left)
    bottom_width = np.linalg.norm(bottom_right - bottom_left)

    left_height = np.linalg.norm(bottom_left - top_left)
    right_height = np.linalg.norm(bottom_right - top_right)

    # 크기를 전달받지 않았다면 변 길이로 추정
    if width is None:
        width = int(round(max(top_width, bottom_width)))

    if height is None:
        height = int(round(max(left_height, right_height)))

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