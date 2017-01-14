Cryptography Application

An application to implement cryptography to encrypt and sign a file to be sent by email using RSA public-private key mechanism.

This is the readme file for fcrypt.py file

text.txt is the file which contains plaintext and is used for the encryption and decryption process.
This name will remain the same since in the decryption part, while verifying the data, it reads input from the plaintext file.
And this filename is not passed as an argument to the command line.

import pickle- used to serialize /de-serialize a python object structure. It helps to convert the object into a byte stream 
during the process of "pickling".And during "unpickling",the inverse opearation takes place.
In this program, pickle is used to dump and load the values of signature,cipher text,aes encrypted key and the IV.

default_backend-gives the defauly supporting algorithms and the supporting platform specific implementations.
rsa-provides packages to generate the rsa public key
serialization-provides modules to serialize the keys generated
load_pem_private_key, load_pem_public_key- functions to load the private key and public key in the pem format
Cipher, algorithms, modes-provides the algorithms,codes and the backend for the encryption and the decryption process.
padding and hashes- gives the modules needed for the hashing and the padding process during encryption/decryption


USAGE:
For encryption:
fcrypt.py -e <destination_public_key_file_name> <sender_private_key_file_name> <input_plaintext_file> <ciphertextfile>

where :
<destination_public_key_file_name>- The file name which contains the public key of the destination
<sender_private_key_file_name> - The file containing the sender's private key for signing
<input_plaintext_file>- The file containing the text which needs to be encrypted
<ciphertextfile>-The file to which the encrypted data has to be written to 

For Decryption:
fcrypt.py -d <destination_private_key_file_name> <sender_public_key_file_name> <ciphertextfile> <output_plaintext_file

where :
<destination_private_key_file_name>- The file name which contains the public key of the destination
<sender_public_key_file_name> - The file containing the sender's public key used for verification
<ciphertextfile>-The file from which the enrypted data is obtained for decryption
<output_plaintext_file>-The file to which the final decrypted data will be wriiten to 


The public-private key pairs for both the sender and destination are store in separate files.
destprivkey.pem- The destination public key
destpubkey.pem- the destination private key in pem format
sendprivkey.pem-the sender’s private key
sendpubkey.pem-the sender’s public key


To generate the keys:
A file key_creation.py is used.
pwd:
C:\Users\BHPriyanka\Documents\First Sem\NetworkSecurity\Class\PS2>

py key_creation.py

Once the keys are generated, executed for encryption/decryption.
No need to run the above command every time.
Example executin of the file fcrypt.py:

fcrypt.py -e destpubkey.pem sendprivkey.pem text.txt cipher.txt

fcrypt.py -d destprivkey.pem sendpubkey.pem cipher.txt final.txt

