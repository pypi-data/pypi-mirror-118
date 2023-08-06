# Installing

## From source:
- `pip install git+https://github.com/editid0/IsDigit`

## From pypi:
- `pip install -U IsDigit`

<br />
<br />
<br />

# Examples
```python
import IsDigit as id

digits = id.IsDigit(allow_floats=True, allow_ints=True)

print(digits.is_digit('1')) # returns True
print(digits.is_digit('1.0')) # returns True
print(digits.is_digit('1.0.0')) # returns False
print(digits.is_digit('x')) # returns False
```
Or, alternatively:
```python
import IsDigit as id

digits = id.IsDigit()

print(digits.is_digit('1')) # returns True
print(digits.is_digit('1.0')) # returns False
print(digits.is_digit('1.0.0')) # returns False
print(digits.is_digit('x')) # returns False
```