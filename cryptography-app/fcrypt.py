##import the packages required for background,assymmetric encryption,symmetric encryption,
##System IO operations,padding,cipher,hash,pickle and serialization

import os,sys,getopt
import pickle
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

##=====================================================================================================================
##The encrypt function 

def encrypt(pub_key,priv_key,inputfilename,outputfilename):
##Obtain the destination public key and the sender private key from the file where it is stored in pem format.
##Do the serialization in order to get it in the proper format
    try:
        with open(priv_key, 'rb') as f:
            sendprivkey = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    except:
        print("The file specified does not exist")
        sys.exit(2)

    try:
        with open(pub_key, 'rb') as f1:
            destpubkey = serialization.load_pem_public_key(f1.read(), backend=default_backend())
    except:
        print("The destination public key file is not present")
        sys.exit(2)

##Sign the file to be encrypted using the sender private key which will be verified later by the receiver using the sende's public key
    signer = sendprivkey.signer(padding.PSS( mgf=padding.MGF1(hashes.SHA1()), salt_length=padding.PSS.MAX_LENGTH),hashes.SHA1())

    try:
        f=open(inputfilename,'rb').read()
    except:
        print("The input file you have specified is not present")
        sys.exit(2)
    else:
        signer.update(f)
        signature=signer.finalize()
                        
##Use the pickle to store the object as it is in a file.        
    try:
        p=open('cipher.txt','wb')
    except:
        print("The encrypted file is not present in the speccified location")
        sys.exit(2)
    else:
        pickle.dump(signature,p)
        
##Calculate the chunksize based on which the contents of the input file has to be processed for encryption
    chunksize = 64*1024
    
##Compute the size of the entire file
    filesize = '{:016d}'.format(os.path.getsize(inputfilename)).encode('utf-8')
    
##Set the default backend for the AES encryption of the data
    backend = default_backend()
    
##Generate the AES key used for symmetric encryption
    aeskey = os.urandom(32)
    
## Generate the random IV
    iv = os.urandom(16)
    
##Store the IV so that the decryption part uses the same generated IV
    pickle.dump(iv,p)

##Encrypting the content of the file with AES key , CBC mode and the default backend
##Encrypt the data chunk by chunk by padding extra bits if its necessary
##Store the encrypted data using the pickle object.
    try:
        cipher = Cipher(algorithms.AES(aeskey), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
    except:
        print("The requested algorithm is not supported for encryption") 

    with open(inputfilename, 'rb') as infile:
        with open(outputfilename, 'wb') as outfile:
             while True:
                   chunk = infile.read(chunksize)
                   if len(chunk) == 0:
                       break
                   elif len(chunk) % 16 != 0:
                       chunk += b' ' * (16 - (len(chunk) % 16))
                       try:
                           pickle.dump(encryptor.update(chunk) + encryptor.finalize(),p)
                       except Exception as TypeError:
                           print("The data specified is not in bytes for update()")
                           print("Or the data is used after its finalized")
                           sys.exit(2)
                            
                  
##Encrypting the AES key and storing it in a file which can be later used by the receiver to decrypt the message
##Use RSA to encrypt the AES key
    message1 = aeskey
    ciphertext1 = destpubkey.encrypt(message1, padding.OAEP( mgf=padding.MGF1(algorithm=hashes.SHA1()),algorithm=hashes.SHA1(),label=None))  
    pickle.dump(ciphertext1,p)
    p.close()

##===============================================================================================================
##decrypt function invoked when the use compiles and runs the decryption part
##It takes in the destination private key,senderpublickey,the file which contains the encrypted data and the output file where the final outcome has to be written to
                                  
def decrypt(destprivkey,senderpublickey,cipherfile,outputfile):
    try:                              
        p =open(cipherfile,'rb')
    except:
        print("The encrypted file is not present")
        sys.exit(2)

##Load the objects stored in the encryption method to separate variables
##First fetch gives the signature,Second gives the IV generated ,Third gives the encrypted data of the file and the last gives the encrypted AESkey                                
    signature=pickle.load(p)
    IV=pickle.load(p)
    encrypted_data=pickle.load(p)
    encrypted_aes=pickle.load(p)
    p.close()

    try:
        f1=open(destprivkey,'rb')
    except:
        print("The file containing the destination private key is not present")
        sys.exit(2)
        
##Serialize the destination private key which will be stored in the pem format in the file                                  
    destprivkey = serialization.load_pem_private_key(f1.read(), password=None, backend=default_backend())

##Decrypt the AES key using the SHA1 protocol for hashing and destination private key
    decrypted_aes = destprivkey.decrypt( encrypted_aes, padding.OAEP( mgf=padding.MGF1(algorithm=hashes.SHA1()), algorithm=hashes.SHA1(), label=None ))

    try:
        f=open(senderpublickey,'rb')
    except:
        print("the file for sender public key is not present")
        sys.exit(2)
                                  
##Serialize and obtain the public key of the sender
    sendpublic_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

##Verify the signature sentusing the sender's public key and using SHA1 hashing protocol                                  
    verifier = sendpublic_key.verifier(signature, padding.PSS( mgf=padding.MGF1(hashes.SHA1()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA1())
                                  
    try:
        q=open('text.txt','rb').read()
    except:
        print("The text file you are looking for is not present")
        sys.exit(2)
                                  
##Update the verifier with the content of the text file.And call the verify() method to verify  
    verifier.update(q)
                                  
##Raises an exception if the signature is invalid
    try:                                  
        verifier.verify()
    except:
        print("Invalid Signature")
        sys.exit(2)

##Decrypt the data by employing AES decryption mechanism,using the decrypted AES key and Initialization vector
##Set the default backend    
    backend = default_backend()
    with open(outputfile, 'wb') as o:
         cipher = Cipher(algorithms.AES(decrypted_aes), modes.CBC(IV), backend=backend)
         decryptor = cipher.decryptor()
         o.write(decryptor.update(encrypted_data) + decryptor.finalize())

    
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def main(argv):
    
##Check if there are enough command line arguments,if not prompt the user to enter all the arguments    
    if len(argv) < 5:
       print("fcrypt.py -e <destination_public_key_file_name> <sender_private_key_file_name> <input_plaintext_file> <ciphertextfile>")
       print("or")
       print("fcrypt.py -d <destination_private_key_file_name> <sender_public_key_file_name> <ciphertextfile> <output_plaintext_file")
       sys.exit(2) 
    try:
       opts, args = getopt.getopt(argv,"e:d:")
    except getopt.GetoptError:
       sys.exit(2)
       
##Call the encrypt function if the option specified by the user is -e or else call the decrypt function       
    for opt, arg in opts:
       if opt =="-e":
          des_pub_key = argv[1]
          sen_priv_key = argv[2]
          infile = argv[3]
          cipher = argv[4]
          encrypt(des_pub_key,sen_priv_key,infile,cipher)
          print("done")
          sys.exit(2)
       if opt =="-d":
          des_priv_key = argv[1]
          sen_pub_key = argv[2]
          cipher = argv[3]
          outfile = argv[4]
          decrypt(des_priv_key,sen_pub_key,cipher,outfile)
          print("done")
          sys.exit(2)
  
##invoke the main method for execution   
if __name__ == "__main__":
    main(sys.argv[1:])

    




