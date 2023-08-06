# Decrypt256
Decrypts SHA-256.
# How to download
To download it do:
```py
pip install decrypt256
```
# How to use it
To include the python file use:
```py
from decrypt256 import decrypt256
```
And to use it do:
```py
from decrypt256 import decrypt256

hash = input("Enter a hash: ")
value_hash = decrypt256.decrypt256(hash)

if value_hash != None:
	print("The value of that hash is: " + value_hash)
else:
	print("Hash invalid or not found")
```