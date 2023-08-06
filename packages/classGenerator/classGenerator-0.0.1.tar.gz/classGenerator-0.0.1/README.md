
# classGenerator

This is a package that helps to generate classes in an easy and fast way



## Installation

Install the package with pip

```bash
  pip install classGenerator
```
    
## Variables Reference

|     Parameter       | Type     | Description                |
| :--------------     | :------- | :------------------------- |
| `nombreArchivo`     | `string` | **Required**. It is the name of the file where the class will be added. If the file does not exist, it will be generated with that name |
| `nombreClase  `     | `string` | **Required**. It is the name with which the class will be generated|
| `variables`         | `string` | **Required**. They are the variables that the class will have |
| `GettersAndSetters` | `bool`   | If this parameter is not specified, the default will be **False**. Set **True** to generate the getters and setters in case you don't want them to set **False** |
| `direccion`         | `string` | If this parameter is not specified, the file will be generated on the **desktop**. Put the address where you want to generate the file |




  
## Usage/Examples

Estructure

```Python
from classGenerator.generateClass import createClass

createClass(nombreArchivo, nombreClase, variables, False, direccion)
```

**Example 1** 

It will create a class on the desktop without getters and setters

```Python
from classGenerator.generateClass import createClass

createClass("People", "Person", "first_name, last_name, email, address")
```
**Example 2** 

It will create a class on the desktop with getters and setters

```Python
from classGenerator.generateClass import createClass

createClass("People", "Person", "first_name, last_name, email, address", True)
```

**Example 3** 

It will create a class at a specific address without getters and setters

```Python
from classGenerator.generateClass import createClass

createClass("People", "Person", "first_name, last_name, email, address", False, "c:\\Users\user\Desktop")
```
  
## Screenshots
![carbon](https://user-images.githubusercontent.com/63989923/131467005-0ec7362d-06f9-48ca-8d41-4ab71875bdce.png)
