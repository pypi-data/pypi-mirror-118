## Ottr ACME Client

`otter-acme` is a Python wrapper around `acme.sh` that handles the certificate
signing process for Certificate Authorities that support the ACME protocol. This
package is utilized when building a container on top of the Airbnb Ottr Core
Platform.

```py
import acme

# Query Subject Alternative Names
subject_alternative_names = acme.query_subject_alternative_names(hostname=hostname, table=table)

# ACME Client
le_client = acme.LetsEncrypt(hostname=hostname, subdelegate=dns,
subject_alternative_names=subject_alternative_names, region=region_name)

# Local Development
le_client.acme_local(csr={csr_path})
# Container Development
le_client.acme_development(csr={csr_path})
# Container Production
le_client.acme_production(csr={csr_path})

# Query Certificate from Device
expiration = acme.query_certificate_expiration(hostname=hostname)
# Update Expiration
acme.update_certificate_expiration(expiration)
```
