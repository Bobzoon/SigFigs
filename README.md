# SigFigs
## Implementation of a Sigfig class and an Exact class that allow simple math operations to be done while keeping the correct number of significant digits.

### Determining the correct number of sigfigs
Keeping track of the number of significant figures, AKA significant digits or sigfigs, in a measurement is crucial to retaining the correct amount of precision. The rules for determining the correct number of significant figures in a number are as follows:
1. All non-zero numbers are significant
2. All zeroes between non-zero numbers are significant
3. All leading zeroes, whether before or after a decimal point, are not significant
4. Trailing zeroes, whether before or after a decimal point, are significant.

Trailing zeroes before an implied decimal point, e.g. the zeroes in 1000, are ambiguous and assumed not significant. To write 1000 with more than one sigfig, use scientific notation

### Maintaining the correct number of sigfigs during an operation.
Maintaining the correct precision during operations is equally as crucial.

When two numbers are multiplied or divided, the result has the same number of significant figures as the quantity with fewer significant figures. Reported to the correct significance, 1.2 * 3.45 = 4.1

When two numbers are added or subtracted, the result has enough significant digits such that it has the same number of decimal places as the quantity with fewer decimal places. Reported to the correct significance, 1.2 + 34.56 = 35.8. Notice that all digits before the decimal place are added. Also notice that the result has 3 sigfigs, despite neither of the inputs having 3. *The result of addition or subtraction can change the number of sigfigs independent of the number of the operands.* Notice also that the result is rounded based on the first *non-significant* digit.

Because the number of sigfigs can change due to addition or subtraction, when addition/subtraction are mixed with multiplication/division sigfigs must be kept track of at each step. Also, although the final result of a series of operations should be rounded to the correct number of significant digits, rounding after each step in a series of operations results in a loss of precision. For example (1.23+4.5)/6.000 = 0.955, which to the correct precision is reported as 0.96, not 0.95, as rounding after the addition and after the division would suggest.

### Exact numbers
Exact quantities such as those in defined quantities or resulting from the counting of discrete objects, are treated as having infinite significant figures.

## Use
```Sigfig(value, sigfigs=None)``` produces a Sigfig object of value ```value``` and with ```sigfigs``` sigfigs. If ```sigfigs``` is None or 0, it is inferred from ```value```.
```value``` can be of types, ```int```,```float```, ```str```, or ```Sigfig```. If a ```float``` is used as the value, any trailing zeroes will be dropped. This can be avoided by either explicitly declaring sigfigs or using a ```str``` type for ```value```. ```Sigfig``` supports addition, subtraction, multiplication, and division with any of the types appropriate for ```value``` and with ```Exact```.

```Exact(value)``` produces an Exact object of value ```value```
