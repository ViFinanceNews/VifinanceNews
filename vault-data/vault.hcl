# Enable the file storage backend
storage "file" {
  path = "/vault/file"
}

listener "tcp" {
  address = "0.0.0.0:9210"
  cluster_address = "0.0.0.0:9202"
  tls_cert_file = "/vault/certs/cert.pem"
  tls_key_file  = "/vault/certs/key.pem"
}

api_addr = "https://127.0.0.1:9210"
cluster_addr = "https://127.0.0.1:9202"

# Enable telemetry (optional)
telemetry {
  disable_hostname = true
}