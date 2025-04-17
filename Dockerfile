# Dockerfile — 프로젝트 최상단에 위치해야 합니다
FROM python:3.9-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 먼저 복사/설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 전체 복사
COPY . .

# Gunicorn으로 Flask 앱 실행
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
