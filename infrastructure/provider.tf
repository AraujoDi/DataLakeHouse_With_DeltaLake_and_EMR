provider "aws" {
    region = var.aws_region
}

# Centralizar o arquivo de controle de estado do terraform
terrform{
    backend "s3"{
        bucket = "terraform-state-diego"
        key = "state/igti/edc/mod1/terraform.tfstate"
        region = "us-east-2"
    }
}