locals {
  user_name = "ec2-user"
  remote_root_path = "/telegram_youtube_downloader"


  base_docker_command = "sudo docker run -d --name telegram_youtube_downloader --restart unless-stopped -e TELEGRAM_BOT_KEY=${var._1_telegram_bot_key}"
  logs_volume = "-v ${local.remote_root_path}/logs:/telegram_youtube_downloader/logs"

  # Only add cookies settings if the cookie file provided and exists
  cookies_settings = length(var._2_cookie_file_path) == 0 ? "" : (
    fileexists(var._2_cookie_file_path) ? "-e youtube_downloader_options__audio_options__cookiefile=/app/cookies/cookies.txt -v ${local.remote_root_path}/cookies:/app/cookies" : ""
  )

  docker_command = "${local.base_docker_command} ${local.logs_volume} ${local.cookies_settings} ${var._3_extra_args} cccaaannn/telegram_youtube_downloader:latest"
}

data "aws_ami" "instance_ami" {
  owners      = ["amazon"]
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-2.*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "server" {
  ami                    = data.aws_ami.instance_ami.id
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.telegram_youtube_sg.id]
  key_name               = aws_key_pair.generated_key.key_name

  tags = {
    Name = "telegram-youtube-downloader"
  }

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    systemctl enable docker
    mkdir -p ${local.remote_root_path}/logs
    mkdir -p ${local.remote_root_path}/cookies
    sudo chmod -R 777 ${local.remote_root_path}
    ${local.docker_command}
  EOF

  # Add connection block for SSH
  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = local.user_name
    private_key = tls_private_key.instance.private_key_pem
  }
}

# Upload the cookie file to the instance if it exists
resource "null_resource" "upload_cookie_file" {
  count = length(var._2_cookie_file_path) > 0 ? 1 : 0

  triggers = {
    instance_id = aws_instance.server.id
  }

  connection {
    type        = "ssh"
    host        = aws_instance.server.public_ip
    user        = local.user_name
    private_key = tls_private_key.instance.private_key_pem
  }

  # Ensure the cookies directory exists and has permissions before copying the file
  provisioner "remote-exec" {
    inline = [
      "sudo mkdir -p ${local.remote_root_path}/cookies",
      "sudo chmod 777 ${local.remote_root_path}/cookies"
    ]
  }

  # Upload the file
  provisioner "file" {
    source      = var._2_cookie_file_path
    destination = "${local.remote_root_path}/cookies/cookies.txt"
  }
}
