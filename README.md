# Art Mentor AI

Art Mentor의 이미지 처리 및 AI 기능을 담당하는 Python 프로젝트입니다.

## 개발 환경

- Python 3.12
- Anaconda
- FastAPI
- OpenCV
- NumPy / pandas

## 첫 번째 개발 목표

비스듬하게 촬영된 그림의 이미지를 정면에서 본 형태로 원근 보정합니다.

1. 원본 이미지 불러오기
2. 그림 영역의 네 모서리 좌표 지정
3. OpenCV로 원근 보정
4. 결과 이미지 저장

추후 모서리 자동 검출 및 Spring Boot와의 API 연동을 추가할 예정입니다.

## 디렉토리 구조

```text
ai/
├── src/
│   └── art_mentor/
│       ├── __init__.py
│       ├── app/
│       │   ├── __init__.py
│       │   └── main.py
│       └── processing/
│           ├── __init__.py
│           └── perspective.py
├── images/
│   ├── input/
│   └── output/
├── environment.yml
├── requirements.txt
└── README.md
```

- `app/main.py`: 프로그램 실행 시작점
- `processing/perspective.py`: 원근 보정 처리
- `images/input/`: 원본 이미지
- `images/output/`: 보정 결과 이미지

## 환경 설정

아래 명령어는 `ai` 폴더에서 실행합니다.

### 가상환경 생성

```bash
conda env create -f environment.yml
conda activate art_mentor_ai
```

이미 가상환경이 있다면 활성화 명령어만 실행합니다.

### 라이브러리 설치

```bash
python -m pip install -r requirements.txt
```

### 의존성 확인

```bash
python -m pip check
```

## 실행 방법

현재 계획한 실행 방식입니다. 기능 구현 후 사용할 수 있습니다.

Windows Anaconda Prompt 기준:

```bat
conda activate art_mentor_ai
set PYTHONPATH=%CD%\src
python -m art_mentor.app.main
```

## 웹 연동 계획

- Next.js / React: 이미지 업로드 및 결과 표시
- Spring Boot: 웹 요청 관리 및 Python API 호출
- Python / FastAPI: 이미지 처리 및 분석 결과 반환