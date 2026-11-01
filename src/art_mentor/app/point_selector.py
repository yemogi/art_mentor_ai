import tkinter as tk
from math import ceil


def select_corners(image_path):
    """PNG 사진에서 클릭한 네 모서리의 원본 좌표를 반환합니다."""
    window = tk.Tk()
    window.title("그림의 네 모서리 선택")

    # PNG 이미지 불러오기
    original = tk.PhotoImage(file=str(image_path))

    # 큰 사진은 창에 들어가도록 정수 배율로 축소
    scale = max(
        1,
        ceil(original.width() / 1000),
        ceil(original.height() / 700),
    )
    display = original.subsample(scale, scale)

    guide = tk.Label(
        window,
        text="왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래 순서로 클릭",
    )
    guide.pack(pady=10)

    canvas = tk.Canvas(
        window,
        width=display.width(),
        height=display.height(),
        highlightthickness=0,
    )
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=display)

    corners = []
    confirmed = False

    # 마우스 왼쪽 버튼을 누를 때 실행되는 함수
    def on_click(event):
        if len(corners) >= 4:
            return

        # 축소 화면의 좌표를 원본 사진의 좌표로 환산
        x = min(event.x * scale, original.width() - 1)
        y = min(event.y * scale, original.height() - 1)
        corners.append((x, y))

        canvas.create_oval(
            event.x - 5, event.y - 5,
            event.x + 5, event.y + 5,
            fill="red", outline="red", tags="marker",
        )
        canvas.create_text(
            event.x + 12, event.y,
            text=str(len(corners)), fill="red", tags="marker",
        )

        guide.config(text=f"{len(corners)}/4개 선택됨")
        if len(corners) == 4:
            guide.config(text="네 점을 확인한 뒤 '선택 완료'를 눌러 주세요.")

    def reset():
        corners.clear()
        canvas.delete("marker")
        guide.config(
            text="왼쪽 위 → 오른쪽 위 → 오른쪽 아래 → 왼쪽 아래 순서로 클릭"
        )

    def finish():
        nonlocal confirmed

        if len(corners) != 4:
            guide.config(text="모서리 네 개를 모두 선택해 주세요.")
            return

        confirmed = True
        window.destroy()

    canvas.bind("<Button-1>", on_click)

    tk.Button(window, text="다시 선택", command=reset).pack(pady=5)
    tk.Button(window, text="선택 완료", command=finish).pack(pady=5)

    window.mainloop()

    if not confirmed:
        raise SystemExit("모서리 선택을 취소했습니다.")

    return corners