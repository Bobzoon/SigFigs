from warnings import warn
class Exact:
    """Exact quantities such as those in defined quantities or resulting from the counting of discrete objects, 
    are treated as having infinite significant figures"""
    def __init__(self,value):
        if type(value)==Exact:
            self.value=value.value
        else:
            self.value=float(value)
    def __add__(self, addition):
        return Exact(self.value+Exact(addition).value)
    __radd__=__add__
    def __sub__(self, subtrahend):
        return Exact(self.value-Exact(subtrahend).value)
    __rsub__=__sub__
    def __mul__(self,multiplicand):
        return Exact(self.value*Exact(multiplicand).value)
    __rmul__=__mul__
    def __truediv__(self,divisor):
        return Exact(self.value/Exact(divisor).value)
    __rtruediv__=__truediv__
    def __str__(self):
        return str(self.value)

class Sigfig:
    """
    Allows math to be done with the returned value having the correct number of significant figures without losing precision during calculation.
    """
    def zerostrip(self, x:str):
        """Remove any characters before significant digits"""
        return x.lstrip('0').lstrip('.').lstrip('0')
        
    def findsigfigs(self):
        """
        Find the number of significant figures in a number
        There are 4 rules in determining the number of significant figures in a number:
        1) All non-zero numbers are significant
        2) All zeroes between non-zero numbers are significant
        3) All leading zeroes, whether before or after a decimal point, are not significant
        4) Trailing zeroes, whether before or after a decimal point, are significant.
        Trailing zeroes before an implied decimal point, e.g. the zeroes in 1000, are ambiguous and assumed not significant
        """
        #Rule 3 and scientific notation handling
        self.remlead0enot=self.zerostrip(self.valuestring).split('e',1)[0]
        #Rule 4
        if '.' not in self.valuestring and self.valuestring[-1]=='0':
            self.sigfigs=len(self.remlead0enot.rstrip('0'))
        #Rules 4, 1, and 3
        else:
            self.sigfigs=len(self.remlead0enot)-1 if '.' in self.remlead0enot else len(self.remlead0enot)
        return self.sigfigs
    
    def findpostdecimal(self):
        """Find the number of places after a decimal point until the number's amount of significant digits has been reached.
        For example, in 1.005, findpostdecimal should return 3, while in 0.00000531, findpostdecimal should return 8.
        When e notation is included, the function is performed on the expanded form of the number."""
        if 'e' in self.valuestring:
            enot=int(self.valuestring.split('e')[1])
            enotpostdecimal=self.valuestring1 if '.' in self.valuestring else None
            positioncorrection=len(enotpostdecimal)-enot
            self.postdecimalsig=positioncorrection if positioncorrection>0 else 0
            return self.postdecimalsig
        elif not (self.valuestring.startswith('0') or self.valuestring.startswith('.')):
            self.postdecimalsig=self.sigfigs-len(self.valuestring0.lstrip('0')) if '.' in self.valuestring else 0
            return self.postdecimalsig
        else:
            postdecimalcount=0
            postdecimalsig=0
            startsigcount=False
            for character in self.valuestring1:
                if not startsigcount and character=='0':
                    postdecimalcount+=1
                else:
                    startsigcount=True
                    postdecimalcount+=1
                    postdecimalsig+=1
                    if postdecimalsig==self.sigfigs:
                        return postdecimalcount

    def __init__(self, value, sigfigs=None):
        """Initializes a Sigfig object with the given value and sigfigs significant figures.
        If not specified, finds the number of significant figures in value."""
        if type(value)==Sigfig:
            self.value=value.value
            self.valuestring=value.valuestring
            self.sigfigs=value.sigfigs
            self.postdecimalsig=value.postdecimalsig
        else:
            try:
                self.value=float(value)
            except ValueError:
                raise TypeError("Sigfig object values must allow float(value)")
            if type(value)==float:
                warn("WARNING: Significant figures that are trailing zeroes right of the decimal point in floats are lost.")
            self.valuestring=f'{value}'.lower()
            self.valuestring0=self.valuestring.split('.')[0]
            self.valuestring1=self.valuestring.split('.')[1] if '.' in self.valuestring else None
            self.sigfigs=sigfigs if sigfigs else self.findsigfigs()
            self.postdecimalsig=self.findpostdecimal()               

    def __add__(self,addition):
        """When two numbers are added, the result has enough significant digits such that 
        it has the same number of decimal places as the quantity with fewer decimal places."""
        if type(addition)==Exact:
            result=Sigfig(f'{self.value+addition.value}')
            result.postdecimalsig=self.postdecimalsig
            predecimal=f"{result.valuestring0}"
            postdecimal=f".{result.valuestring1[:result.postdecimalsig]}"
            sigfigtest=predecimal+postdecimal if result.postdecimalsig else predecimal
            result.sigfigs=Sigfig(sigfigtest).findsigfigs()
            return result
        else:
            sigadd=Sigfig(addition)
            result=Sigfig(f'{self.value+sigadd.value}')
            result.postdecimalsig=min([self.postdecimalsig,sigadd.postdecimalsig])
            predecimal=f"{result.valuestring0}"
            postdecimal=f".{result.valuestring1[:result.postdecimalsig]}"
            sigfigtest=predecimal+postdecimal if result.postdecimalsig else predecimal
            result.sigfigs=Sigfig(sigfigtest).findsigfigs()
            return result
    __radd__=__add__
        
    def __sub__(self,subtrahend):
        """Subtraction follows the same rules as addition"""
        if type(subtrahend)==Exact:
            result=Sigfig(f'{self.value-subtrahend.value}')
            result.postdecimalsig=self.postdecimalsig
            predecimal=f"{result.valuestring0}"
            postdecimal=f".{result.valuestring1[:result.postdecimalsig]}"
            sigfigtest=predecimal+postdecimal if result.postdecimalsig else predecimal
            result.sigfigs=Sigfig(sigfigtest).findsigfigs()
            return result
        else:
            sigsub=Sigfig(subtrahend)
            result=Sigfig(f'{self.value-sigsub.value}')
            result.postdecimalsig=min([self.postdecimalsig,sigsub.postdecimalsig])
            predecimal=f"{result.valuestring0}"
            postdecimal=f".{result.valuestring1[:result.postdecimalsig]}"
            sigfigtest=predecimal+postdecimal if result.postdecimalsig else predecimal
            result.sigfigs=Sigfig(sigfigtest).findsigfigs()
            return result
    __rsub__=__sub__
    
    def __mul__(self,multiplicand):
        """When two numbers are multiplied, the result has the same number of significant figures
        as the quantity with fewer significant figures"""
        if type(multiplicand)==Exact:
            result=Sigfig(f'{self.value*multiplicand.value}')
            result.sigfigs=self.sigfigs
            result.postdecimalsig=result.findpostdecimal() if '.' in result.valuestring else 0
            return result
        else:
            sigmul=Sigfig(multiplicand)
            result=Sigfig(f'{self.value*sigmul.value}')
            result.sigfigs=min([self.sigfigs,sigmul.sigfigs])
            result.postdecimalsig=result.findpostdecimal() if '.' in result.valuestring else 0
            return result
    __rmul__=__mul__
    
    def __truediv__(self,divisor):
        """Division follows the same rules as multiplication"""
        if type(divisor)==Exact:
            result=Sigfig(f'{self.value/divisor.value}')
            result.sigfigs=self.sigfigs
            result.postdecimalsig=result.findpostdecimal() if '.' in result.valuestring else 0
            return result
        else:
            sigdiv=Sigfig(divisor)
            result=Sigfig(f'{self.value/sigdiv.value}')
            result.sigfigs=min([self.sigfigs,sigdiv.sigfigs])
            result.postdecimalsig=result.findpostdecimal() if '.' in result.valuestring else 0
            return result
    __rtruediv__=__truediv__

    def __repr__(self):
        return f"Sigfig('{self.value}', sigfigs={self.sigfigs})"
    
    def __str__(self):
        return f"{self.value:.{self.sigfigs-1}e}"
