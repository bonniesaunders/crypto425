# README #

This module was written to provide students of cryptography a basic set of objects and functions to get started programming cryptography applications.

There are two classes: 

+ **Message** which sets up strings that use a particular alphabet. 
  An alphabet 'ABCDEFGHIJKLMNOPQRSTUVEWXYZ' can be used for classical ciphers.  The complete 8-bit ascii code 
  can be used for modern ciphers.
+ **Cipher** with sub-classes that have encrypt, decrypt, and sometimes crack methods. 

The module depends on Matmod <https://bitbucket.org/bonnie_saunders/matmod> which provides basic number theory functions and again depends on cypari.

contact Bonnie Saunders <saunders@uic.edu>