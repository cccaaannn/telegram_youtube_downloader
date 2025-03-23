output "ec2_public_ip" {
  value       = aws_instance.server.public_ip
  description = "The public IP address of the EC2 instance"
}

output "ssh_connection_string" {
  value       = "ssh -i ${path.module}/aws-tyd-key.pem ec2-user@${aws_instance.server.public_ip}"
  description = "SSH connection string to connect to the EC2 instance"
}
