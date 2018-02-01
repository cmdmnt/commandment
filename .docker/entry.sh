#!/usr/bin/env bash

echo "Starting commandment..."

SSL_HOSTNAME=${SSL_HOSTNAME:-"commandment.test"}

PYTHONPATH=/commandment
export PYTHONPATH

echo "Initialising database..."
touch /commandment/commandment.db
/usr/local/bin/alembic --config /commandment/alembic.ini -x data=true upgrade head

if [[ ! -f /etc/nginx/ssl/ssl.crt || ! -f /etc/nginx/ssl.key ]]; then
    echo "Did not find any SSL certificate to use. SSL is required for MDM."
    echo "Creating new certificate using environment with DNSName: ${SSL_HOSTNAME}"

    cat <<- EOF > /tmp/openssl.cnf

        [req]
        distinguished_name = req_distinguished_name
        req_extensions = v3_req
        prompt = no
        [req_distinguished_name]
        C = AU
        ST = New South Wales
        L = Sydney
        O = Commandment
        OU = MDM
        CN = ${SSL_HOSTNAME}
        [v3_req]
        # Extensions to add to a certificate request
        basicConstraints = CA:FALSE
        keyUsage = nonRepudiation, digitalSignature, keyEncipherment
        subjectAltName = @alt_names
        [alt_names]
        DNS.1 = ${SSL_HOSTNAME}
        DNS.2 = localhost
EOF

    openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout /etc/nginx/ssl.key -out /etc/nginx/ssl.crt -config /tmp/openssl.cnf -extensions 'v3_req'

fi


echo "Starting uWSGI and nginx"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

