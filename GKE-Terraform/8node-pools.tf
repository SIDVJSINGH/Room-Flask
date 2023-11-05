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
    machine_type = "e2-small"
    disk_size_gb = 10
    labels = {
      role = "general"
    }
    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# resource "google_container_node_pool" "spot" {
#   name = "spot"
#   location = "us-central1-b"
#   cluster = google_container_cluster.primary.id
#   node_count = 1
#   management {
#     auto_repair = true
#     auto_upgrade = true
#   }
#   autoscaling {
#     min_node_count = 1
#     max_node_count = 4
#   }
#   node_config {
#     preemptible = true
#     machine_type = "e2-small"
#     labels = {
#       role = "spot"
#       team = "devops"
#     }
#     service_account = google_service_account.kubernetes.email
#     oauth_scopes = [
#       "https://www.googleapis.com/auth/cloud-platform"
#     ]
#   }
# }
