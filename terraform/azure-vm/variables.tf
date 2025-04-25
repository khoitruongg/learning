variable "location" {
  default     = "East US"
  description = "Azure region"
}

variable "admin_username" {
  type        = string
  description = "Admin username for SSH"
}

variable "ssh_pub_key_path" {
  type        = string
  description = "Path to your SSH public key"
}
