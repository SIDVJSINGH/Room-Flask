resource "google_service_account" "kubernetes" {
  account_id = "kubernetes"
}

resource "google_container_node_pool" "general" {
  name = "general"
  location = "us-central1-a"
  cluster = google_container_cluster.primary.id
  node_count = 1
  management {
    auto_repair = true
    auto_upgrade = true
  }
  node_config {
    preemptible = false
    machine_type = "e2-medium"
    disk_size_gb = 20 
    labels = {
      role = "general"
    }
    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

