## Overview

In cavag, the core functions are provided by `Object` and `PropertySet` in file *_utils.py*. The UML diagram of this file is shown below

<div style="text-align: center"><img src="_assets/pics/uml/_utils_uml.png" alt="UML of _utils"></div>

In other modules, all abstract classes related to physical objects are subclasses of `PrintableObject`. A mature subclass needs to define the **modifiable_properties** class property, which can be used in class method `cls.filter_properties(kwargs)` to filter modifiable physical properties in the dict, <font color="red">kwargs</font>. In general, **modifiable_properties** contains the names of all input parameters other than the <font color="red">name</font> defined in the constructor of the subclass. A **property_set** is created #TO DO


## Module Content

- [fiber](fiber.md)

  **Class[es]**

  - `FiberEnd`
  - `StepIndexFiberEnd`


- [fpcavity](fpcavity)


- [gaussbeam](gaussbeam.md)


- [mirror](mirror.md)

  **Class[es]**

  - `MirrorSurface`
  - `RTLConverter`
  - `ThickLens`
  - `ThinLens`


- [misc](misc.md) 


- [utils](utils.md)