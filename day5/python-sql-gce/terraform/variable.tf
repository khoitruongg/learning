variable "project_id" {
  description = "The Google Cloud project ID"
  type        = string
}

variable "postgres_db" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "myappdb"  # You can leave this empty to override in .env
}

variable "postgres_user" {
  description = "PostgreSQL user"
  type        = string
  default     = "myuser"  # Same as above
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "postgres_host" {
  description = "Host where PostgreSQL is running"
  type        = string
  default     = "localhost"
}

variable "postgres_port" {
  description = "Port for PostgreSQL"
  type        = string
  default     = "5432"
}

variable "credentials_file" {
  description = "Path to the service account credentials file"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "The GCP region"
  type        = string
  default = "us-central1"
}

variable "docker_image_name" {
  description = "The name of the Docker image"
  type        = string
  default     = "python-postgres-app"
}

variable "repository_name" {
  description = "The Artifact Registry repository name"
  type        = string
  default     = "app-repo"
}

variable "image_tag" {
  description = "The tag for the Docker image"
  type        = string
  default     = "latest"
}

variable "service_email" {
  description = "The email for terraform service"
  type        = string
}