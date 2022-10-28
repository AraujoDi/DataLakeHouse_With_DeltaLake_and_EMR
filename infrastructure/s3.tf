resource "aws_s3_bucket" "dl" {
    bucket = "dtlk-diego-edc-tf"
    acl = "private"

    tags = {
      IES   = "IGTI",
      CURSO = "EDC"
    }
    
    server_side_encryption_configuration{
        rule {
            apply_server_side_encription_by_default {
                sse_algorithm = "AES256"
            }
        }
    }
}