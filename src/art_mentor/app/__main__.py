from pathlib import Path

import cv2

from art_mentor.processing.perspective import correct_perspective


def main():
    # 프로젝트 최상위 폴더
    project_root = Path(__file__).resolve().parents[3]

    # 입력 이미지 불러오기
    image_path = project_root / "images" / "input" / "image_01.png"
    image = cv2.imread(str(image_path))

    if image is None:
        raise SystemExit(f"이미지를 읽지 못했습니다: {image_path}")

    print("이미지 불러오기 성공!")
    print("이미지 크기:", image.shape)

    # 이 사진의 모서리 좌표
    # 왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래
    corners = [
        (82, 260),
        (1027, 129),
        (1387, 681),
        (185, 1012),
    ]

    # 별도 파일에 정의한 보정 함수 호출
    # 출력 크기는 아직 연습용 값
    corrected = correct_perspective(
        image, corners, width=1200, height=850
    )

    # 보정 이미지 저장
    output_dir = project_root / "images" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result_path = output_dir / "image_01_corrected.png"

    if not cv2.imwrite(str(result_path), corrected):
        raise RuntimeError("보정 이미지 저장에 실패했습니다.")

    print("원근 보정 결과 저장:", result_path)


if __name__ == "__main__":
    main()