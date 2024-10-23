#!/usr/bin/env sh

# The certificate must be an identity document certificate
# i.e. ID card, digi-ID, ..., but not mID, Smart-ID.
# For mID, Smart-ID, the intermediate and root are different.
CERT_NAME=...

# Problem: issuer not known
# openssl verify $CERT_NAME

# Get the ESTEID2018 intermediate certificate
curl -O https://c.sk.ee/esteid2018.der.crt

# Problem: issuer not known
# openssl verify esteid2018.der.crt

# Problem: no root known (intermediate issuer not known)
# openssl verify -CAfile esteid2018.der.crt $CERT_NAME

# Get the EE-GovCA2018 root certificate
curl -O https://c.sk.ee/EE-GovCA2018.der.crt

# Problem: self-signed and not trusted
# openssl verify EE-GovCA2018.der.crt

openssl verify -trusted EE-GovCA2018.der.crt EE-GovCA2018.der.crt
openssl verify -CAfile EE-GovCA2018.der.crt esteid2018.der.crt

# DER to PEM
openssl x509 -in EE-GovCA2018.der.crt -outform PEM -out EE-GovCA2018.pem.crt
openssl x509 -in esteid2018.der.crt -outform PEM -out esteid2018.pem.crt

# Create certificate bundle
cat EE-GovCA2018.pem.crt > SK.bundle
cat esteid2018.pem.crt >> SK.bundle

# This will work
openssl verify -CAfile SK.bundle $CERT_NAME

# Get OCSP endpoint
OCSP_URI=$(openssl x509 -in $CERT_NAME -noout -ocsp_uri)

# Get the OCSP response and validate it
openssl ocsp -issuer esteid2018.pem.crt -cert $CERT_NAME \
  -url "$OCSP_URI" -CAfile SK.bundle -text
