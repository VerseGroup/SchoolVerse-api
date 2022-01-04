# fernet encryptions if necessary, but prioritize RSA for more security

# fernet is symmetric encryption (a key and a ciphertext, where they key allows both encryption and decryption)

# rsa is asymmetric encryption (ciphertext, a public key and a private key) which even uses sha256. The private key
# allows user to encrypt and decrypt, and the public key only allows encryption. In this case, the clientside would receive
# a public key to store data, and would make an api call to a server to do any manipulation that would require decryption.
# this means that if client is hacked, no data can be read and we can prioritize security on the backend instead in regard to the 
# private keys