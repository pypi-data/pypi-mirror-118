# Operator Information Library

The library to get information about various operators in 
Python.

Install through pip:

```sh
pip install o
```

Start off my importing the module:

```py
import o
```

Use the `get` method to get the Operator object for a specific
operator, provided as a string.

```py
operator = o.get("+=")
print(operator)
>>> "<class 'Operator(operator='+=', name='addition assignment', type=AssignmentOperatorType, methods=['__iadd__'], function=operator.iadd)'>"
```

Use the various attributes to retrieve information for the operator.

```py
operator.methods
>>> ['__iadd__']

str(operator.type)
>>> "assignment"

isinstance(operator.type, o.AssignmentOperatorType)
>>> True
```

Or, you can use the Operator object directly.
Be careful, an unknown operator raises an UnknownOperator exception.

## License

This repo is under the MIT license.