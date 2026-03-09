<p align="center">
  <a href="https://github.com/Anti-Forensics/tuckerlsb">
    <img src="assets/images/tuckerlsb.png" alt="TuckerLSB banner" width="900">
  </a>
</p>

Usage:

This script will embed a hidden message into a specified output PNG file.  

```
$ python tuckerlsb.py --input demo.png --output out.png --message "TEST"  
```

This script will also extract the hidden message and print it.  

```
$ python tuckerlsb.py --input out.png --getmessage
```
