from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")
print(password)
print(password2)

# Returns true
print(sha256_crypt.verify("password", password))

# Returns always failure
# if password == password2:
#     print("Right Guess")
# else:
#     print(" Guess")
