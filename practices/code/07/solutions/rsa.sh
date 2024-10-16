#!/usr/bin/env sh

KEYFILE=key.pem
PUBFILE=pub.pem

DATAFILE=data.bin
HASHFILE=data.sha256

PSSSIG1=pss1.sig
PSSSIG2=pss2.sig

PKCSSIG1=det1.sig
PKCSSIG2=det2.sig

# Generate random data to sign
openssl rand -hex 3072 > $DATAFILE

# Generate unprotected RSA private key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out $KEYFILE -quiet

# Extract public key from private key
openssl pkey -in $KEYFILE -pubout -out $PUBFILE

# Sign in PSS mode using 'dgst' util
echo "dgst: generating PSS signatures '$PSSSIG1' and '$PSSSIG2'"
openssl dgst -sha256 -sign $KEYFILE \
  -sigopt rsa_padding_mode:pss -sigopt rsa_mgf1_md:sha256 -out $PSSSIG1 $DATAFILE
openssl dgst -sha256 -sign $KEYFILE \
  -sigopt rsa_padding_mode:pss -sigopt rsa_mgf1_md:sha256 -out $PSSSIG2 $DATAFILE
echo "Generated OK"

echo

# Sign in PKCS1_v1.5 mode using 'dgst' util
echo "dgst: generating PKCS1_v1.5 signatures '$PKCSSIG1' and '$PKCSSIG2'"
openssl dgst -sha256 -sign $KEYFILE -out $PKCSSIG1 $DATAFILE
openssl dgst -sha256 -sign $KEYFILE -out $PKCSSIG2 $DATAFILE
echo "Generated OK"

echo

# Showcase signature differences
echo "SHA256sums of signature files"
sha256sum ./*.sig

echo

# Verify signatures using 'dgst' util
echo "dgst: verifying RSA-PSS signature '$PSSSIG1'"
openssl dgst -sha256 -verify $PUBFILE -sigopt rsa_padding_mode:pss \
  -signature $PSSSIG1 $DATAFILE

echo "dgst: verifying RSA-PSS signature '$PSSSIG2'"
openssl dgst -sha256 -verify $PUBFILE -sigopt rsa_padding_mode:pss \
  -signature $PSSSIG2 $DATAFILE

echo

# Verify signature using 'dgst' util
echo "dgst: verifying PKCS1_v1.5 signature '$PKCSSIG1'"
openssl dgst -sha256 -verify $PUBFILE -signature $PKCSSIG1 $DATAFILE

echo

# Output SHA256 hashes for signature verification with 'pkeyutl'
openssl dgst -sha256 -binary -out $HASHFILE $DATAFILE

# Verify signatures using 'pkeyutl' util for pre-hashed data
echo "pkeyutl: verifying RSA-PSS signature '$PSSSIG1' with pre-hashed data"
openssl pkeyutl -verify -in $HASHFILE -pubin -inkey $PUBFILE -sigfile $PSSSIG1 \
  -pkeyopt rsa_padding_mode:pss -pkeyopt digest:sha256

echo "pkeyutl: verifying RSA-PSS signature '$PSSSIG2' with pre-hashed data"
openssl pkeyutl -verify -in $HASHFILE -pubin -inkey $PUBFILE -sigfile $PSSSIG2 \
  -pkeyopt rsa_padding_mode:pss -pkeyopt digest:sha256

echo

# Verify signatures using 'pkeyutl' for raw data
echo "pkeyutl: verifying RSA-PSS signature '$PSSSIG1' with original data"
openssl pkeyutl -verify -in $DATAFILE -pubin -inkey $PUBFILE -sigfile $PSSSIG1 \
  -rawin -digest sha256 -pkeyopt rsa_padding_mode:pss

echo "pkeyutl: verifying RSA-PSS signature '$PSSSIG2' with original data"
openssl pkeyutl -verify -in $DATAFILE -pubin -inkey $PUBFILE -sigfile $PSSSIG2 \
  -rawin -digest sha256 -pkeyopt rsa_padding_mode:pss

echo

# Sanity check functions ====================================
check_pss () {
  openssl dgst -sha256 -verify $PUBFILE \
    -sigopt rsa_padding_mode:pss -sigopt rsa_mgf1_md:sha256 \
    -signature $PSSSIG1 $DATAFILE > /dev/null
  openssl dgst -sha256 -verify $PUBFILE \
    -sigopt rsa_padding_mode:pss -sigopt rsa_mgf1_md:sha256 \
    -signature $PSSSIG2 $DATAFILE > /dev/null
}

check_pkcs () {
  openssl dgst -sha256 -verify \
    $PUBFILE -signature $PKCSSIG1 $DATAFILE > /dev/null
}
# ===========================================================

# Sign in PSS mode using 'pkeyutl' util with raw data
echo "pkeyutl: generating PSS signatures '$PSSSIG1' and '$PSSSIG2' with original data"
openssl pkeyutl -sign -in $DATAFILE -inkey $KEYFILE -out $PSSSIG1 \
  -rawin -digest sha256 -pkeyopt rsa_padding_mode:pss
openssl pkeyutl -sign -in $DATAFILE -inkey $KEYFILE -out $PSSSIG2 \
  -rawin -digest sha256 -pkeyopt rsa_padding_mode:pss
check_pss
echo "Generated OK"

echo

# Sign in PKCS1_v1.5 mode using 'pkeyutl' util with raw data
echo "pkeyutl: generating PKCS1_v1.5 signature '$PKCSSIG1' with original data"
openssl pkeyutl -sign -in $DATAFILE -inkey $KEYFILE -out $PKCSSIG1 \
  -rawin -digest sha256
check_pkcs
echo "Generated OK"

echo

# Sign in PSS mode using 'pkeyutl' util with pre-hashed data
echo "pkeyutl: generating PSS signatures '$PSSSIG1' and '$PSSSIG2' with pre-hashed data"
openssl pkeyutl -sign -in $HASHFILE -inkey $KEYFILE -out $PSSSIG1 \
  -pkeyopt rsa_padding_mode:pss -pkeyopt digest:sha256
openssl pkeyutl -sign -in $HASHFILE -inkey $KEYFILE -out $PSSSIG2 \
  -pkeyopt rsa_padding_mode:pss -pkeyopt digest:sha256
check_pss
echo "Generated OK"

echo

# Sign in PKCS1_v1.5 mode using 'pkeyutl' util with raw data
echo "pkeyutl: generating PKCS1_v1.5 signature '$PKCSSIG1' with original data"
openssl pkeyutl -sign -in $HASHFILE -inkey $KEYFILE -out $PKCSSIG1 \
  -pkeyopt digest:sha256
check_pkcs
echo "Generated OK"
