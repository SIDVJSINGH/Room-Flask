terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
    }
  }
  backend "gcs" {
    bucket         = "stp-7thsem"
    prefix         = "GKE/gke.tfstate"
  }
}

# to set region in the gcp, go to shell and type this command "gcloud config set compute/region us-cental1-a"
# to set zone in the gcp, go to shell and type this command "gcloud config set compute/zone us-cental1"

provider "google" {
  credentials = file("${path.module}/key/all.json")
  project     = "stp-7thsem"
  region      = "us-central1"
  zone        = "us-central1-a"
}
