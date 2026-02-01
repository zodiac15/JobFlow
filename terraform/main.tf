terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

resource "google_compute_instance" "vm" {
    name = "jobflow-vm"
    machine_type = "e2-micro"
    zone = var.zone
    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-11"
            size = 10
        }
    }
    network_interface {
        network = "default"
        access_config {}
    }
    metadata = {
        enable_oslogin = true
        startup-script = <<EOF
echo '${base64encode(file("${path.module}/startup.sh"))}' | base64 -d > /tmp/startup.sh
chmod +x /tmp/startup.sh
/tmp/startup.sh
EOF
    }
    tags = ["http-server", "https-server"]
}

resource "google_compute_firewall" "allow-http" {
    name = "allow-http"
    network = "default"
    allow {
        protocol = "tcp"
        ports = ["80","8080","5000"]
    }
    source_ranges = ["0.0.0.0/0"]
}
