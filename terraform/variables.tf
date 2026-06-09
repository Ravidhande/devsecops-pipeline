variable "region" {
  default = "ap-south-1"
}

variable "cluster_name" {
  default = "devsecops-cluster"
}

variable "ecr_repo_name" {
  default = "devsecops-app"
}

variable "eks_version" {
  default = "1.31"
}