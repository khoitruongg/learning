variable "project_id" {
  type        = string
  description = "Your GCP project ID"
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "ssh_user" {
  type        = string
  description = "SSH user for VM access"
}

variable "ssh_pub_key_path" {
  type        = string
  description = "Path to your SSH public key"
}
