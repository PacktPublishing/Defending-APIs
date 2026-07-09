# Attacking APIs
In this lesson, you will how to hack a live API using the [vAPI](https://github.com/roottusk/vapi) vulnerable API as an example API to attack. The API emulates all ten of the OWASP API Security Top 10 2019 flaws and you should attempt to complete as many of these in the time available, starting with the number one and working up to number ten.

## Setup
* To install vAPI, use the following commands to clone the repository, and start the Docker services.
    ```
    git clone https://github.com/roottusk/vapi.git
    cd vapi
    sudo docker compose up -d
    ```
* Next install the Postman environment and collection contained within the repository in the 'postman' folder (refer to either of the guides [here](#further-reading))

* Verify vAPI is running by accessing the documentation at [http://localhost/vapi](http://localhost/vapi)

## Instructions
For the exercises, there are two ways to complete the challenges:

### The hard way - on your own
This is the more challenging option and relies on only the prompts provided in the vAPI documentation here: [http://localhost/vapi](http://localhost/vapi)

### The easy way - using one of the guides 
This an alternative option and relies on the guides provided [here](#further-reading). These guides provide step-by-step instructions on how to complete each challenge.

## Further Reading
* [vAPI GitHub repository](https://github.com/roottusk/vapi)
* [OWASP API Security Top 10 2019](https://owasp.org/API-Security/editions/2019/en/0x11-t10/)
* [Guide - OWASP API Top 10 CTF Walk-through](https://securedelivery.io/articles/api-top-ten-walkthrough/)
* [Guide - vAPI walkthrough](https://zerodayhacker.com/vapi-walkthrough/)