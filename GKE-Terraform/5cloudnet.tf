resource "google_compute_router_nat" "nat" {
  name = "nat"
  router = google_compute_router.router.name
  region = "us-central1"
  nat_ip_allocate_option = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

resource "google_compute_address" "nat" {
  name = "nat"
  region = "us-central1"
  address_type = "EXTERNAL"
  network_tier = "STANDARD"
  depends_on = [ google_project_service.compute, google_project_service.container ]
}
