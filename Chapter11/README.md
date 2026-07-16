# Chapter Eleven

## Code samples

- `kong/kong.yml` — declarative Kong config: JWT auth, rate limiting, IP restriction and CORS
- `docker-compose.yml` — Kong in DB-less mode in front of the backend
- `hardening/Dockerfile` — a minimal, non-root, hardened container image
- `monitoring_alerting.py` — log-based detection of brute-force and BOLA-style abuse

> **Note:** these are compact, illustrative placeholder samples (AI-assisted, author-reviewed) meant as a starting point for the concepts in this chapter, not production code. See the repository root `CODE_NOTES.md`. Install shared dependencies with `pip install -r ../requirements.txt`.

## Further Reading
* [https://snyk.io/blog/tips-for-hardening-container-image-security-strategy/](https://snyk.io/blog/tips-for-hardening-container-image-security-strategy/)
* [https://www.cisecurity.org/insights/blog/how-to-layer-secure-docker-containers-with-hardened-images](https://www.cisecurity.org/insights/blog/how-to-layer-secure-docker-containers-with-hardened-images)
* [https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
* [https://www.cisecurity.org/cis-hardened-images/amazon](https://www.cisecurity.org/cis-hardened-images/amazon)
* [https://www.chakray.com/how-protect-your-apis-installing-configuring-modsecurity-nginx/](https://www.chakray.com/how-protect-your-apis-installing-configuring-modsecurity-nginx/)
* [https://owasp.org/www-project-modsecurity-core-rule-set/](https://owasp.org/www-project-modsecurity-core-rule-set/)
* [https://www.netnea.com/cms/apache-tutorial-7_including-modsecurity-core-rules/](https://www.netnea.com/cms/apache-tutorial-7_including-modsecurity-core-rules/)
* [https://www.fastly.com/blog/the-waf-efficacy-framework-measuring-the-effectiveness-of-your-waf](https://www.fastly.com/blog/the-waf-efficacy-framework-measuring-the-effectiveness-of-your-waf)
* [https://github.com/coreruleset/coreruleset](https://github.com/coreruleset/coreruleset)
* [https://en.wikipedia.org/wiki/Next-generation_firewall](https://en.wikipedia.org/wiki/Next-generation_firewall)
* [https://learn.microsoft.com/en-us/azure/api-management/mitigate-owasp-api-threats](https://learn.microsoft.com/en-us/azure/api-management/mitigate-owasp-api-threats)
* [https://www.altexsoft.com/blog/api-gateway/](https://www.altexsoft.com/blog/api-gateway/)
* [https://konghq.com/install#kong-community](https://konghq.com/install#kong-community)
* [https://www.moesif.com/blog/technical/api-tools/API-Management-vs-API-Gateway-and-where-does-API-Analytics-and-Monitoring-fit/](https://www.moesif.com/blog/technical/api-tools/API-Management-vs-API-Gateway-and-where-does-API-Analytics-and-Monitoring-fit/)
* [https://beeceptor.com/](https://beeceptor.com/)
* [https://curity.io/resources/learn/phantom-token-pattern/](https://curity.io/resources/learn/phantom-token-pattern/)
* [https://docs.42crunch.com/latest/content/concepts/api_firewall.htm](https://docs.42crunch.com/latest/content/concepts/api_firewall.htm)
* [https://42crunch.com/actively-monitor-and-defend-your-apis-with-42crunch-and-the-azure-sentinel-platform/](https://42crunch.com/actively-monitor-and-defend-your-apis-with-42crunch-and-the-azure-sentinel-platform/)
* [https://azuremarketplace.microsoft.com/en-us/marketplace/apps/42crunch1580391915541.42crunch_sentinel_solution?tab=Overview&OCID=AIDcmm549zy227_aff_7794_1243925](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/42crunch1580391915541.42crunch_sentinel_solution?tab=Overview&OCID=AIDcmm549zy227_aff_7794_1243925)
