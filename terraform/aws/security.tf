data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "telegram_youtube_sg" {
  name   = "telegram-youtube-downloader-sg"
  vpc_id = data.aws_vpc.default.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "telegram-youtube-downloader"
  }
}