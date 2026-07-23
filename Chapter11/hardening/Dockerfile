# Chapter 11 - Securing and hardening environments: a minimal, non-root image.
FROM python:3.12-slim AS base
# Drop privileges -- never run the API as root.
RUN useradd --create-home --uid 10001 apiuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER apiuser
EXPOSE 8000
# Read-only rootfs and no new privileges are enforced at runtime, e.g.:
#   docker run --read-only --security-opt no-new-privileges ...
CMD ["uvicorn", "common.demo_vulnerable_api.app:app", "--host", "0.0.0.0"]
