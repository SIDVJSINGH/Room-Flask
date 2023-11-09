resource "google_container_cluster" "primary" {
  name                     = "primary"
  location                 = "us-central1"
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
    enable_private_nodes    = false
    enable_private_endpoint = false
  }

  master_authorized_networks_config {
    cidr_blocks {
      display_name = "all-ip"
      cidr_block   = "0.0.0.0/0"
    }
  }
    node_config {
    machine_type = "e2-medium"
    disk_size_gb = 50      
  }
  # lifecycle {
  #   prevent_destroy = true
  # }
}
