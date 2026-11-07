variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "agentplatform"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # nunca aparece en logs
}