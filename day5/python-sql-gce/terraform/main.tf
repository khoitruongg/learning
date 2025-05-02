
# Define repository URL as a local value
locals {
  repository_url = "gcr.io/${var.project_id}/${var.repository_name}"
}

# Cloud SQL Database Instance
resource "google_sql_database_instance" "default" {
  name             = "day4-database"
  database_version = "POSTGRES_13"
  region           = var.region
  deletion_protection = false 

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      authorized_networks {
        name  = "my-network"
        value = "0.0.0.0/0"  # Allow all IPs for testing
      }
    }
  }

  lifecycle {
    prevent_destroy = false  # Allow Terraform to destroy this resource
  }
}

# Config SQL name
resource "google_sql_database" "postgres_db" {
  name     = var.postgres_db  # This is the actual database name
  instance = google_sql_database_instance.default.name
}

# Create SQL User
resource "google_sql_user" "postgres_user" {
  name     = var.postgres_user
  instance = google_sql_database_instance.default.name
  password_wo = var.postgres_password
}

# Compute Engine VM
resource "google_compute_instance" "vm" {
  name         = "d4-vm"
  machine_type = "e2-micro"
  zone         = "us-central1-a"
  allow_stopping_for_update = true 

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Define external IP address configuration
    }
  }

  metadata = {
    startup-script = <<-EOT
      #!/bin/bash
      apt-get update
      apt-get install -y docker.io

      # Enable and start Docker
      systemctl enable docker
      systemctl start docker

      # Authenticate to GCR (use your service account JSON or setup access manually)
      echo '${file("${var.credentials_file}")}' > /tmp/key.json
      gcloud auth activate-service-account --key-file=/tmp/key.json
      gcloud auth configure-docker gcr.io

      # Pull and run the Docker image
      docker pull gcr.io/${var.project_id}/${var.repository_name}/${var.docker_image_name}:${var.image_tag}
      docker run -d -p 5000:5000 gcr.io/${var.project_id}/${var.repository_name}/${var.docker_image_name}:${var.image_tag}
    EOT
  }

  service_account {
    email  = "${var.service_email}@${var.project_id}.iam.gserviceaccount.com"
    scopes = ["cloud-platform"]
  }

  tags = ["http-server", "https-server"]

  deletion_protection = false  # Allow deletion

  lifecycle {
    prevent_destroy = false  # Allow Terraform to destroy this resource
  }
}

# Cloud Run Service (Dockerized app)
resource "google_cloud_run_service" "app_service" {
  name     = var.docker_image_name
  location = var.region

  template {
    spec {
      containers {
        image = "${local.repository_url}/${var.docker_image_name}:${var.image_tag}"
        env {
          name  = "POSTGRES_PASSWORD"
          value = var.postgres_password
        }
        env {
          name  = "POSTGRES_DB"
          value = var.postgres_db
        }
        env {
          name  = "POSTGRES_USER"
          value = var.postgres_user
        }
        env {
          name  = "POSTGRES_HOST"
          value = var.postgres_host
        }
        env {
          name  = "POSTGRES_PORT"
          value = tostring(var.postgres_port)
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Output the Cloud Run URL
output "cloud_run_url" {
  description = "The URL of the Cloud Run service."
  value       = google_cloud_run_service.app_service.status[0].url
}

# Output the Cloud SQL Database instance name
output "db_instance_name" {
  description = "The name of the Cloud SQL Database instance."
  value       = google_sql_database_instance.default.name
}

# Output the external IP of the VM
output "vm_external_ip" {
  description = "The external IP of the VM instance."
  value       = google_compute_instance.vm.network_interface[0].access_config[0].nat_ip
}
