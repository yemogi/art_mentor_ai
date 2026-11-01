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
        # 서로 다른 점 네 개인지 검사
    if len(np.unique(source_points, axis=0)) != 4:
        raise ValueError("같은 모서리를 중복 선택했습니다.")

    # 모든 좌표가 원본 이미지 안에 있는지 검사
    image_height, image_width = image.shape[:2]
    x_values = source_points[:, 0]
    y_values = source_points[:, 1]

    if (
        (x_values < 0).any()
        or (x_values >= image_width).any()
        or (y_values < 0).any()
        or (y_values >= image_height).any()
    ):
        raise ValueError("모서리 좌표가 이미지 범위를 벗어났습니다.")

    # OpenCV의 윤곽선 형식으로 변환
    contour = source_points.reshape(4, 1, 2)

    # 선이 교차하거나 한 점이 안쪽으로 들어간 경우 거부
    if not cv2.isContourConvex(contour):
        raise ValueError(
            "네 모서리를 왼쪽 위 → 오른쪽 위 → "
            "오른쪽 아래 → 왼쪽 아래 순서로 선택해 주세요."
        )

    # 네 점이 만드는 영역이 지나치게 작은 경우 거부
    if cv2.contourArea(contour) < 4:
        raise ValueError("선택한 영역이 너무 작습니다.")

    # 이미지 좌표계에서 시계 방향인지 검사
    if cv2.contourArea(contour, oriented=True) <= 0:
        raise ValueError("모서리를 시계 방향으로 선택해 주세요.")

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