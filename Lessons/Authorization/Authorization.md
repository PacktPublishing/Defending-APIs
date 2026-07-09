# Authorization
In this lesson, you will learn the basics of authorization of API endpoints using firstly a simple approach and then using a more advanced approach using Casbin.

## Setup
You will need a modern Python environment (> 3.6) and the following packages installed from the [requirements](../requirements.txt) file. We will be working with the Python file [casbin_demo.py](./casbin_demo.py) and its dependences in this lesson.

## Instructions
### Step 1: Play with the Casbin tool on their website
Go to the [Casbin editor](https://casbin.org/editor/) and play with the tool. You can use the example provided or create your own. Understand both how the model and policy work together and try this with test data.

### Step 2: Use the example provided to evaluate the Casbin tool in practice
Use the [casbin_demo.py](./casbin_demo.py) provided and the [guide](https://dev.to/teresafds/authorization-on-fastapi-with-casbin-41og) to work through Casbin in practice. You should be able to verify that the user `johndoe` can delete items but that user `alice` is able to delete items.

## Further Reading
* [Authorization on FastAPI with Casbin](https://dev.to/teresafds/authorization-on-fastapi-with-casbin-41og)
* [Casbin](https://casbin.org/)
* [Casbin editor](https://casbin.org/editor/)