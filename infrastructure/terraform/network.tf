# VPC — red privada aislada
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "${var.app_name}-vpc"
    Environment = var.environment
  }
}

# Subnet pública — para el agente (FastAPI)
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "${var.app_name}-public"
    Environment = var.environment
  }
}

# Subnet privada — para PostgreSQL y Redis (no expuestos a internet)
resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name        = "${var.app_name}-private"
    Environment = var.environment
  }
}

# Security group para el agente
resource "aws_security_group" "agent" {
  name   = "${var.app_name}-agent-sg"
  vpc_id = aws_vpc.main.id

  # Permite tráfico entrante en el puerto 8000
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Permite todo el tráfico saliente
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "${var.app_name}-agent-sg"
    Environment = var.environment
  }
}

# Security group para la DB — solo acepta tráfico del agente
resource "aws_security_group" "db" {
  name   = "${var.app_name}-db-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.agent.id]
  }

  tags = {
    Name        = "${var.app_name}-db-sg"
    Environment = var.environment
  }
}