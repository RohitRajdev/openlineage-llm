#!/usr/bin/env bash
set -euo pipefail

API_URL="${OPENLINEAGE_URL:-http://localhost:3000}"
ADMIN_URL="${OPENLINEAGE_ADMIN_URL:-http://localhost:3001}"
NS="${OPENLINEAGE_NAMESPACE:-ai-apps}"

echo "Waiting for Marquez admin at $ADMIN_URL/healthcheck ..."
for i in {1..60}; do
  if curl -fsS "$ADMIN_URL/healthcheck" >/dev/null; then
    echo "Admin is healthy ✅"
    break
  fi
  echo "  still starting... ($i/60)"; sleep 1
  if [[ "$i" == "60" ]]; then
    echo "Admin health did not become ready in time"; exit 1
  fi
done

echo "== Admin health =="
curl -sS "$ADMIN_URL/healthcheck" || true
echo -e "\n== Namespaces =="
curl -sS "$API_URL/api/v1/namespaces" || true
echo -e "\n== Jobs in $NS =="
curl -sS "$API_URL/api/v1/namespaces/$NS/jobs" || true
echo
