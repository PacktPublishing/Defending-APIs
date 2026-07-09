# API Firewalls
In this lesson, you will learn about the 42Crunch API firewall and how to integrate this with your API to provide very granular security controls at your API endpoints.

## Setup
For the 42Crunch API firewall installation, you need two components:
* A demo application with a corresponding OAS definition. I suggest to use Pixi as a Docker installation [here](../../Sample%20APIs/Pixi/docker-compose.yaml) and the OAS definition [here](../../OAS%20Files/PhotoManager.json)
* You will also need to install the firewall and log forwarder to collect logs and forward them to Azure Sentinel. You can find the installation instructions [here](https://github.com/42Crunch/azure-sentinel-integration).

## Instructions
There is no specific lesson for this topic, but you can find more information about the 42Crunch API firewall in the [42Crunch API Firewall Documentation](https://help.42crunch.com/docs/api-firewall). If you register for a community account on 42Crunch then you will have access to a limited version of the API firewall that you can use to test out the functionality.

## Further Reading
* [42Crunch API Firewall](https://42crunch.com/api-firewall/)
* [42Crunch API Firewall Documentation](https://help.42crunch.com/docs/api-firewall)
* [42Crunch Microsoft Sentinel Connector](https://azuremarketplace.microsoft.com/en-gb/marketplace/apps/42crunch1580391915541.42crunch_sentinel_solution?tab=Overview)
* [Azure Sentinel Integration on GitHub](https://github.com/42Crunch/azure-sentinel-integration)
* [Protect Your APIs with Microsoft Azure Sentinel and 42Crunch Platforms](https://42crunch.com/protect-your-apis-with-microsoft-azure-sentinel-and-42crunch-platforms/)
* [Actively Monitor and Defend Your APIs with 42Crunch and the Azure Sentinel Platform](https://42crunch.com/actively-monitor-and-defend-your-apis-with-42crunch-and-the-azure-sentinel-platform/)
* [Recommendations to mitigate OWASP API Security Top 10 threats using API Management](https://learn.microsoft.com/en-us/azure/api-management/mitigate-owasp-api-threats)
