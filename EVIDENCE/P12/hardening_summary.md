# P12 Hardening summary (template)

## Already applied
- Dockerfile uses a pinned base image (`python:3.12-slim`) and multi-stage build.
- Container runs as non-root user (`USER app`).
- `docker-compose.yaml` uses hardening options: `read_only: true`, `cap_drop: [ALL]`, `no-new-privileges:true`, `seccomp`/`apparmor` profiles (where supported).

## Planned improvements (based on P12 scanners)
- Review Hadolint findings (if any) and fix the highest-impact ones.
- Review Checkov findings for Docker Compose and tighten configuration where reasonable.
- Review Trivy HIGH/CRITICAL vulnerabilities:
  - update base image / Python dependencies;
  - confirm whether findings are exploitable in runtime image (dev-only vs prod).
