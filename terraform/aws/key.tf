# Generate a new RSA private key for the instance
resource "tls_private_key" "instance" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create an AWS key pair using the generated public key
resource "aws_key_pair" "generated_key" {
  key_name   = "tyd-key"
  public_key = tls_private_key.instance.public_key_openssh
}

# Save the generated private key to a local file
resource "local_file" "private_key" {
  content         = tls_private_key.instance.private_key_pem
  filename        = "${path.module}/aws-tyd-key.pem"
  file_permission = "0400"
}