resource "google_container_cluster" "primary" {
  name                     = "primary"
  location                 = "us-central1-a"
  initial_node_count       = 1
  network                  = google_compute_network.vpc_network.self_link
  subnetwork               = google_compute_subnetwork.private-subnet.self_link
  remove_default_node_pool = true
  depends_on               = [google_compute_network.vpc_network, google_compute_subnetwork.private-subnet]
  logging_service          = "logging.googleapis.com/kubernetes"
  monitoring_service       = "monitoring.googleapis.com/kubernetes"
  networking_mode          = "VPC_NATIVE"
  node_locations           = ["us-central1-b", "us-central1-c"]
  
  addons_config {
    http_load_balancing {
      disabled = true
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
  
  release_channel {
    channel = "REGULAR"
  }
  
  workload_identity_config {
    workload_pool = "stp-7thsem.svc.id.goog"
  }
  
  ip_allocation_policy {
  cluster_ipv4_cidr_block = "10.100.0.0/14"
  }
  
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = true
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  master_authorized_networks_config {
    cidr_blocks {
      display_name = "my-ip"
      cidr_block   = "203.0.113.4/32"
    }
  }
  deletion_protection = false
}
