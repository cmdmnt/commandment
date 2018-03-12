#!/usr/bin/env bash

openssl smime -decrypt -in "${1}" -recip "./dep-public.pem"  -inkey "./dep-key.pem"
