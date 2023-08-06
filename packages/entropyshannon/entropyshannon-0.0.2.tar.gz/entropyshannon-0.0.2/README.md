
<div id="headline" align="center">
  <h1>Entropy-Calucalator</h1>
  <p>Conations a python package for various  type of entropy calculations</p>
</div> 





### Requirements
- None
### Installation
```
pip install entropyshannon
```
	
### Basic example

```py
from entropyshannon import *

string_entropy=shannon_entropy("12311331")
print(string_entropy)


probability_list=[1/2,1/3,1/10,7/10]
print(shannon_entropy_probability_list(probability_list))


```


    
