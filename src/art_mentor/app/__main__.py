from pathlib import Path

import cv2
import math
import tkinter as tk
from tkinter import filedialog

from art_mentor.app.point_selector import select_corners
from art_mentor.processing.perspective import correct_perspective


def main():
    # 프로젝트 최상위 폴더
    project_root = Path(__file__).resolve().parents[3]

    # 입력 이미지 불러오기
    # 파일 선택 창을 위한 기본 창은 숨기기
    picker = tk.Tk()
    picker.withdraw()

    try:
        selected_file = filedialog.askopenfilename(
            parent=picker,
            title="보정할 PNG 사진을 선택해 주세요",
            initialdir=str(project_root / "images" / "input"),
            filetypes=[("PNG 이미지", "*.png")],
        )
    finally:
        picker.destroy()

    # 취소를 누르면 종료
    if not selected_file:
        print("사진 선택을 취소했습니다.")
        return

    image_path = Path(selected_file)
    image = cv2.imread(str(image_path))

    if image is None:
        raise SystemExit(f"이미지를 읽지 못했습니다: {image_path}")

    print("이미지 불러오기 성공!")
    print("이미지 크기:", image.shape)

    # 이 사진의 모서리 좌표
    # 왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래
    # 사진에서 클릭한 네 모서리 좌표 받기
    corners = select_corners(image_path)

    # 별도 파일에 정의한 보정 함수 호출
    # 실제 종이의 가로:세로 비율 입력
    while True:
        ratio_text = input(
            "종이의 가로:세로 비율을 입력하세요. 모르면 Enter: "
        ).strip()

        # 아무것도 입력하지 않으면 변 길이로 추정
        if ratio_text == "":
            corrected = correct_perspective(image, corners)
            print("실제 종이 비율을 모르는 상태의 추정 결과입니다.")
            break

        try:
            paper_width, paper_height = map(float, ratio_text.split(":"))

            # 두 값 모두 유한한 양수인지 확인
            if not all(
                math.isfinite(value) and value > 0
                for value in (paper_width, paper_height)
            ):
                raise ValueError

            # 출력 너비를 1200픽셀로 정하고 비율에 맞춰 높이 계산
            width = 1200
            height_value = width * (paper_height / paper_width)

            if not math.isfinite(height_value):
                raise ValueError

            height = round(height_value)

            # 지나치게 크거나 작은 결과 방지
            if not 2 <= height <= 12000:
                raise ValueError

        except (ValueError, OverflowError):
            print("비율을 확인해 주세요. 예: 4:3 또는 297:210")
            continue

        corrected = correct_perspective(
            image, corners, width=width, height=height
        )
        print("입력한 종이 비율 적용:", ratio_text)
        break

    print("출력 크기 (높이, 너비):", corrected.shape[:2])

    # 보정 이미지 저장
    output_dir = project_root / "images" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result_path = output_dir / f"{image_path.stem}_corrected.png"

    if not cv2.imwrite(str(result_path), corrected):
        raise RuntimeError("보정 이미지 저장에 실패했습니다.")

    print("원근 보정 결과 저장:", result_path)


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print("보정을 중단했습니다:", error)