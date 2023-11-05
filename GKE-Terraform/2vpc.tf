resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  disable_on_destroy = true
  disable_dependent_services = true
}

resource "google_project_service" "container" {
  service = "container.googleapis.com"
  disable_on_destroy = true
  disable_dependent_services = true
}

data "google_client_config" "default" {}

resource "google_compute_network" "vpc_network" {
  name                    = lower("network")
  auto_create_subnetworks = false
  routing_mode = "REGIONAL"
  mtu = 1460
  delete_default_routes_on_create = false

  depends_on = [ data.google_client_config.default, google_project_service.compute, google_project_service.container ]
}