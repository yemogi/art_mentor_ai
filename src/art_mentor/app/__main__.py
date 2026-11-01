from pathlib import Path

import cv2

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
    # 출력 크기는 아직 연습용 값
        # 사진 속 변 길이로 출력 크기를 추정해서 보정
    corrected = correct_perspective(image, corners)

    print("출력 크기 추정값 (높이, 너비):", corrected.shape[:2])
    print("주의: 실제 종이 비율을 확인하지 않은 추정 결과입니다.")

    # 보정 이미지 저장
    output_dir = project_root / "images" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result_path = output_dir / f"{image_path.stem}_corrected.png"

    if not cv2.imwrite(str(result_path), corrected):
        raise RuntimeError("보정 이미지 저장에 실패했습니다.")

    print("원근 보정 결과 저장:", result_path)


if __name__ == "__main__":
    main()