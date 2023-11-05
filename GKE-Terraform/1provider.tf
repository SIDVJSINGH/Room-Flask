terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
  backend "gcs" {
    bucket         = "stp-application"
    prefix         = "GKE/gke.tfstate"
  }
}

# to set region in the gcp, go to shell and type this command "gcloud config set compute/region us-cental1-a"
# to set zone in the gcp, go to shell and type this command "gcloud config set compute/zone us-cental1"

provider "google" {
  # credentials = file("${path.module}/key/all.json")
  project     = "stp-application"
  region      = "us-central1"
  zone        = "us-central1-a"
}
