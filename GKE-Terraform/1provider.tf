terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
  backend "gcs" {
    bucket         = "stp-7thsem"
    prefix         = "GKE/gke.tfstate"
  }
}


# to set region in the gcp, go to shell and type this command "gcloud config set compute/region us-central1-a"
# to set zone in the gcp, go to shell and type this command "gcloud config set compute/zone us-central1"

provider "google" {
  project     = "stp-7thsem"
  region      = "us-central1"
  zone        = "us-central1-a"
}
