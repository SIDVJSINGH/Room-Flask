resource "google_compute_subnetwork" "private-subnet" {
  name          = "private-subnet"
  ip_cidr_range = "10.0.0.0/18"
  network       = google_compute_network.vpc_network.id
  region        = "us-central1"
  private_ip_google_access = true
  secondary_ip_range {
    range_name    = "k8s-pods-range"
    ip_cidr_range = "10.48.0.0/14"
}
  secondary_ip_range {
    range_name    = "k8s-services-range"
    ip_cidr_range = "10.52.0.0/18"
}
}