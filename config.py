voms_config = {
    "vomses": [
        {
            "hostname": "voms.example.org",
            "port": "443",
            "vo_name": "example-vo"
        }
    ],
    "cert_path": "/var/www/.globus/usercert.pem",
    "key_path": "/var/www/.globus/userkey.pem",
    "trusted_ca_path": "/etc/grid-security/certificates/"
}

comanage_config = {
    "dbname": "example_db",
    "user": "example_user",
    "host": "example_address",
    "password": "secret"
}