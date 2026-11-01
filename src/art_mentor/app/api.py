import json
from fastapi import Form, Response
from art_mentor.processing.perspective import correct_perspective

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title="Art Mentor AI")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/images/inspect")
async def inspect_image(file: UploadFile = File(...)):
    # 최대 10MB까지 허용
    max_bytes = 10 * 1024 * 1024
    contents = await file.read(max_bytes + 1)

    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail="사진 크기는 10MB 이하여야 합니다.",
        )

    if not contents:
        raise HTTPException(
            status_code=400,
            detail="빈 파일입니다.",
        )

    # 업로드된 파일의 바이트를 이미지 배열로 변환
    encoded = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="이미지로 읽을 수 없는 파일입니다.",
        )

    height, width = image.shape[:2]

    return {
        "filename": file.filename,
        "width": width,
        "height": height,
        "channels": image.shape[2],
    }

@app.post("/images/correct")
async def correct_image(
    file: UploadFile = File(...),
    corners: str = Form(...),
    width: int | None = Form(default=None, ge=2, le=4000),
    height: int | None = Form(default=None, ge=2, le=4000),
):
    # 업로드 파일 읽기: 최대 10MB
    max_bytes = 10 * 1024 * 1024
    contents = await file.read(max_bytes + 1)

    if len(contents) > max_bytes:
        raise HTTPException(status_code=413, detail="사진은 10MB 이하여야 합니다.")

    if not contents:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    encoded = np.frombuffer(contents, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=400, detail="이미지를 읽지 못했습니다.")

    # 출력 너비와 높이는 함께 입력하거나 함께 생략
    if (width is None) != (height is None):
        raise HTTPException(
            status_code=400,
            detail="출력 너비와 높이는 둘 다 입력하거나 둘 다 생략해 주세요.",
        )

    try:
        # JSON 문자열을 네 좌표가 들어 있는 배열로 변환
        points = np.array(json.loads(corners), dtype=np.float32)

        if points.shape != (4, 2) or not np.isfinite(points).all():
            raise ValueError("좌표는 유한한 숫자로 된 [x, y] 네 쌍이어야 합니다.")

        image_height, image_width = image.shape[:2]

        if (
            (points[:, 0] < 0).any()
            or (points[:, 0] >= image_width).any()
            or (points[:, 1] < 0).any()
            or (points[:, 1] >= image_height).any()
        ):
            raise ValueError("좌표가 이미지 범위를 벗어났습니다.")

        # 크기를 생략했다면 기존 함수와 같은 기준으로 추정
        if width is None:
            top_left, top_right, bottom_right, bottom_left = points

            width = int(round(max(
                np.linalg.norm(top_right - top_left),
                np.linalg.norm(bottom_right - bottom_left),
            )))
            height = int(round(max(
                np.linalg.norm(bottom_left - top_left),
                np.linalg.norm(bottom_right - top_right),
            )))

        # 지나치게 큰 출력 이미지 방지
        if width > 4000 or height > 4000:
            raise ValueError("출력 너비와 높이는 각각 4000픽셀 이하여야 합니다.")

        corrected = correct_perspective(
            image, points, width=width, height=height
        )

    except (ValueError, TypeError, OverflowError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    # 보정 결과를 PNG 파일 내용으로 변환
    success, result = cv2.imencode(".png", corrected)

    if not success:
        raise HTTPException(status_code=500, detail="결과 이미지 변환에 실패했습니다.")

    return Response(
        content=result.tobytes(),
        media_type="image/png",
        headers={
            "Content-Disposition": 'attachment; filename="corrected.png"'
        },
    )