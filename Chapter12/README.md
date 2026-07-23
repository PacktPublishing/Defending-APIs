# Chapter Twelve

## Code samples

- `services/gateway_service.py` — edge authentication with internal token propagation
- `services/orders_service.py` — a downstream service enforcing east-west scope checks
- `docker-compose.yml` — the two services wired together, orders unpublished to the outside

> **Note:** these are compact, illustrative placeholder samples (AI-assisted, author-reviewed) meant as a starting point for the concepts in this chapter, not production code. See the repository root `CODE_NOTES.md`. Install shared dependencies with `pip install -r ../requirements.txt`.

## The idea

1. A caller hits the **gateway** with an external JWT (`EXTERNAL_JWT_SECRET`,
   audience `edge`).
2. The gateway verifies that token, then mints a short-lived **internal** JWT
   (`INTERNAL_JWT_SECRET`, audience `orders`, scope `orders:read`).
3. The **orders** service only accepts that internal token and checks scope with
   exact membership (so `orders:reader` does not satisfy `orders:read`).

Orders is not published to the host. Only the gateway is reachable from outside
the Compose network.

## Run without Docker

The scope checks are covered by the unit tests:

```bash
# from the repository root
JWT_SECRET=$(python -c "import secrets;print(secrets.token_hex(32))") \
  pytest tests/test_units.py -k scope -v
```

## Run with Docker

Stop the Chapter 11 stack first if it is still using the Docker engine heavily,
then from the **repository root**:

```bash
docker compose -f Chapter11/docker-compose.yml down   # if still running
docker compose -f Chapter12/docker-compose.yml up --build
```

| Service | Host ports | Role |
|---------|------------|------|
| `gateway` | `12001` | Edge auth + token propagation |
| `orders` | not published | Downstream; east-west only |

Without a token:

```bash
curl -i http://localhost:12001/orders
# → 401 authenticate at the edge
```

With a valid external token (demo secrets match the code defaults):

```bash
TOKEN=$(python - <<'PY'
import jwt, time
print(jwt.encode(
    {"sub": "1001", "aud": "edge", "exp": time.time() + 60},
    "external-edge-secret-rotate-me",
    algorithm="HS256",
))
PY
)
curl -i http://localhost:12001/orders -H "Authorization: Bearer $TOKEN"
# → 200 with the orders list
```

Those default secrets are for local demos only. Override with
`EXTERNAL_JWT_SECRET` / `INTERNAL_JWT_SECRET` in real use.

Tear down:

```bash
docker compose -f Chapter12/docker-compose.yml down
```

## Further Reading
* [https://microservices.io/](https://microservices.io/)
* [https://www.openlegacy.com/blog/monolithic-application](https://www.openlegacy.com/blog/monolithic-application)
* [https://falco.org/](https://falco.org/)
* [https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/](https://www.aquasec.com/cloud-native-academy/kubernetes-in-production/kubernetes-security-best-practices-10-steps-to-securing-k8s/)
* [https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html)
* [https://www.practical-devsecops.com/kubernetes-security-best-practices/](https://www.practical-devsecops.com/kubernetes-security-best-practices/)
* [https://arstechnica.com/information-technology/2018/02/tesla-cloud-resources-are-hacked-to-run-cryptocurrency-mining-malware/](https://arstechnica.com/information-technology/2018/02/tesla-cloud-resources-are-hacked-to-run-cryptocurrency-mining-malware/)
* [https://blog.kubesimplify.com/four-pillars-of-observability-in-kubernetes](https://blog.kubesimplify.com/four-pillars-of-observability-in-kubernetes)
* [https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204A.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204A.pdf)
* [https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf)
* [https://www.cloudflare.com/en-gb/learning/access-management/what-is-mutual-tls/](https://www.cloudflare.com/en-gb/learning/access-management/what-is-mutual-tls/)
* [https://approov.io/blog/how-certificate-pinning-helps-thwart-mobile-mitm-attacks](https://approov.io/blog/how-certificate-pinning-helps-thwart-mobile-mitm-attacks)
* [https://docs.konghq.com/hub/kong-inc/acme/](https://docs.konghq.com/hub/kong-inc/acme/)
* [https://medium.com/microservices-in-practice/service-mesh-for-microservices-2953109a3c9a](https://medium.com/microservices-in-practice/service-mesh-for-microservices-2953109a3c9a)
* [https://tetrate.io/blog/mtls-best-practices-for-kubernetes/](https://tetrate.io/blog/mtls-best-practices-for-kubernetes/)
* [https://curity.io/resources/learn/introduction-identity-and-access-management/](https://curity.io/resources/learn/introduction-identity-and-access-management/)
* [https://curity.io/resources/learn/the-api-security-maturity-model/](https://curity.io/resources/learn/the-api-security-maturity-model/)
* [https://www.okta.com/resources/whitepaper/8-ways-to-secure-your-microservices-architecture/](https://www.okta.com/resources/whitepaper/8-ways-to-secure-your-microservices-architecture/)
* [https://identityserver4.readthedocs.io/en/latest/topics/reference_tokens.html](https://identityserver4.readthedocs.io/en/latest/topics/reference_tokens.html)
* [https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf)
* [https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf](https://www.cisa.gov/sites/default/files/2023-04/zero_trust_maturity_model_v2_508.pdf)
* [https://docs.solo.io/gloo-edge/latest/](https://docs.solo.io/gloo-edge/latest/)
* [https://traefik.io/traefik-hub/](https://traefik.io/traefik-hub/)
* [https://docs.nginx.com/nginx/](https://docs.nginx.com/nginx/)
* [https://www.getambassador.io/products/edge-stack/api-gateway](https://www.getambassador.io/products/edge-stack/api-gateway)
* [https://traefik.io/blog/reverse-proxy-vs-ingress-controller-vs-api-gateway/](https://traefik.io/blog/reverse-proxy-vs-ingress-controller-vs-api-gateway/)
* [https://docs.solo.io/gloo-edge/latest/introduction/architecture/deployment_arch/](https://docs.solo.io/gloo-edge/latest/introduction/architecture/deployment_arch/)
