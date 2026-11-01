# Art Mentor AI

Art Mentor의 이미지 처리 및 AI 기능을 담당하는 Python 프로젝트입니다.

비스듬하게 촬영된 그림 사진에서 사용자가 종이의 네 모서리를 선택하면, OpenCV로 원근 보정하여 결과를 저장합니다.

## 개발 환경

- Python 3.12
- Anaconda
- OpenCV / NumPy
- Tkinter: 파일 선택 및 모서리 선택 화면
- FastAPI: 향후 웹 API 연동에 사용

프로젝트의 Python 패키지 목록과 버전은 requirements.txt에 기록되어 있습니다.

## 구현된 기능

- 파일 선택 창에서 PNG 이미지 선택
- 마우스로 종이의 네 모서리 지정
- 모서리를 잘못 선택했을 때 다시 선택
- 실제 종이의 가로:세로 비율 입력
- 비율을 모를 때 사진 속 변 길이로 출력 크기 추정
- 원근 보정 결과를 PNG 이미지로 저장

## 주요 파일과 폴더

| 경로 | 역할 |
|---|---|
| src/art_mentor/app/__main__.py | 파일 선택, 비율 입력, 보정 함수 호출 및 결과 저장 |
| src/art_mentor/app/point_selector.py | 사진 표시 및 마우스로 네 모서리 선택 |
| src/art_mentor/processing/perspective.py | 출력 크기 추정 및 원근 보정 |
| images/input/ | 샘플 원본 이미지 |
| images/output/ | 보정 결과 이미지. 실행 시 자동 생성 |
| environment.yml | Conda 가상환경 설정 |
| requirements.txt | Python 패키지 목록 |
| .gitignore | 캐시와 실행 결과를 Git 관리 대상에서 제외 |

## 환경 설정

저장소를 내려받은 뒤 프로젝트 최상위 폴더에서 실행합니다.
최상위 폴더는 README.md와 requirements.txt가 있는 폴더입니다.

### 가상환경 생성

```powershell
conda env create -f environment.yml
conda activate art_mentor_ai
```

이미 환경을 만들었다면 활성화 명령어만 실행합니다.

```powershell
conda activate art_mentor_ai
```

### 패키지 설치

```powershell
python -m pip install -r requirements.txt
```

### 의존성 확인

```powershell
python -m pip check
```

## 실행 방법

Windows PowerShell 기준입니다.
프로젝트 최상위 폴더에서 실행합니다.

```powershell
conda activate art_mentor_ai
$env:PYTHONPATH = "$PWD\src"
python -m art_mentor.app
```

PYTHONPATH 설정은 현재 터미널에 적용됩니다.
새 터미널을 열면 다시 설정합니다.

## 사용 순서

1. 파일 선택 창에서 보정할 PNG 사진을 선택합니다.
2. 흰 종이의 바깥 모서리를 다음 순서로 클릭합니다.
   - 왼쪽 위
   - 오른쪽 위
   - 오른쪽 아래
   - 왼쪽 아래
3. 잘못 클릭했다면 ‘다시 선택’을 누릅니다.
4. 네 점을 확인하고 ‘선택 완료’를 누릅니다.
5. 터미널로 돌아와 종이의 가로:세로 비율을 입력합니다.
   - 비율을 알면 `4:3`, `297:210` 등의 형식으로 입력합니다.
   - 실제 가로·세로 길이를 입력할 때는 같은 단위를 사용합니다.
   - 비율을 모르면 아무것도 입력하지 않고 Enter를 누릅니다.
6. images/output/ 폴더에서 결과를 확인합니다.

## 결과 저장

선택한 사진의 이름 뒤에 _corrected를 붙여 저장합니다.

예시:

- image_01.png → images/output/image_01_corrected.png
- image_02.png → images/output/image_02_corrected.png

원본 사진은 수정하지 않습니다.
동일한 결과 이름의 파일이 이미 있으면 덮어씁니다.
서로 다른 폴더에서 이름이 같은 사진을 선택해도 결과 이름이 같으므로 주의해야 합니다.

## 비율 및 보정의 한계

- 비율을 입력하면 출력 너비는 1200픽셀로 정하고, 높이는 입력 비율에 맞춰 계산합니다.
- 비율을 생략하면 위·아래 변 중 긴 길이를 너비로, 왼쪽·오른쪽 변 중 긴 길이를 높이로 사용합니다.
- 변 길이로 추정한 출력 크기는 실제 종이 비율을 보장하지 않습니다.
- 비율이 맞지 않으면 그림이 늘어나거나 눌릴 수 있습니다. 형태 평가에 사용할 때는 실제 종이 비율을 입력하는 것이 좋습니다.
- 현재는 평평한 직사각형 종이의 네 모서리가 모두 보이는 사진을 대상으로 합니다.
- 종이의 휘어짐, 렌즈 왜곡, 그림자와 반사광은 별도로 보정하지 않습니다.
- 현재 파일 선택 화면은 PNG 이미지만 지원합니다.
- 실행 결과 이미지와 Python 캐시는 Git 관리 대상에서 제외됩니다.

## 향후 개발 계획

- 모서리 좌표의 유효성 검사 강화
- 모서리 자동 검출
- JPG 등 입력 이미지 형식 확대
- FastAPI를 통한 이미지 및 모서리 좌표 수신
- Next.js / React 및 Spring Boot와 연동

현재 구현은 로컬 컴퓨터에서 실행하는 수동 모서리 선택 프로그램입니다.
웹 API는 아직 구현하지 않았습니다.