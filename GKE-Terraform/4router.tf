resource "google_compute_router" "router" {
  name    = "router"
  network = google_compute_network.vpc_network.id
  region  = "us-central1"
}