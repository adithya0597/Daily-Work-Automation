"""iac-boilerplate - Generate Terraform modules for cloud infrastructure."""

import argparse
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from typing import Any

from skillpack.utils.output import get_output_dir, write_text


def handler(args: argparse.Namespace) -> int:
    """CLI handler for iac-boilerplate."""
    result = iac_boilerplate_main(
        project_name=args.name,
        cloud=args.cloud,
        resources=args.resources.split(",") if args.resources else None,
        output_dir=args.output_dir,
    )

    if result.get("success"):
        print(f"✅ Generated Terraform modules: {result['output_dir']}")
        for f in result.get("files", []):
            print(f"   - {f}")
        return 0
    print(f"❌ Error: {result.get('error')}")
    return 1


def register_parser(subparsers: Any) -> None:
    """Register the iac-boilerplate subcommand."""
    parser = subparsers.add_parser(
        "iac-boilerplate",
        help="Generate Terraform modules for cloud infrastructure",
    )
    parser.add_argument("--name", required=True, help="Project name")
    parser.add_argument(
        "--cloud",
        choices=["aws", "gcp", "azure"],
        default="aws",
        help="Cloud provider",
    )
    parser.add_argument(
        "--resources",
        default="compute,storage,network",
        help="Comma-separated resources to generate",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./out/iac_boilerplate"),
        help="Output directory",
    )
    parser.set_defaults(handler=handler)


def iac_boilerplate_main(
    project_name: str,
    cloud: str = "aws",
    resources: list[str] | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """Generate Terraform infrastructure code."""
    if output_dir is None:
        output_dir = get_output_dir("iac_boilerplate")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)

    if resources is None:
        resources = ["compute", "storage", "network"]

    try:
        files = []

        # Generate main.tf
        main_tf = generate_main_tf(project_name, cloud)
        write_text(content=main_tf, filename="main.tf", skill_name="iac_boilerplate", output_dir=output_dir)
        files.append("main.tf")

        # Generate variables.tf
        variables = generate_variables(project_name, cloud)
        write_text(content=variables, filename="variables.tf", skill_name="iac_boilerplate", output_dir=output_dir)
        files.append("variables.tf")

        # Generate outputs.tf
        outputs = generate_outputs(cloud, resources)
        write_text(content=outputs, filename="outputs.tf", skill_name="iac_boilerplate", output_dir=output_dir)
        files.append("outputs.tf")

        # Generate resource modules
        for resource in resources:
            module_content = generate_module(project_name, cloud, resource)
            write_text(
                content=module_content,
                filename="main.tf",
                skill_name="iac_boilerplate",
                subdir=f"modules/{resource}",
                output_dir=output_dir,
            )
            files.append(f"modules/{resource}/main.tf")

        # Generate terraform.tfvars.example
        tfvars = generate_tfvars_example(project_name, cloud)
        write_text(content=tfvars, filename="terraform.tfvars.example", skill_name="iac_boilerplate", output_dir=output_dir)
        files.append("terraform.tfvars.example")

        # Generate README
        readme = generate_readme(project_name, cloud, resources)
        write_text(content=readme, filename="README.md", skill_name="iac_boilerplate", output_dir=output_dir)
        files.append("README.md")

        return {
            "success": True,
            "output_dir": str(output_dir),
            "files": files,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def generate_main_tf(project_name: str, cloud: str) -> str:
    """Generate main.tf with provider config."""
    
    providers = {
        "aws": dedent('''\
            terraform {
              required_version = ">= 1.0"
              
              required_providers {
                aws = {
                  source  = "hashicorp/aws"
                  version = "~> 5.0"
                }
              }
              
              backend "s3" {
                # Configure in backend.hcl
              }
            }

            provider "aws" {
              region = var.aws_region
              
              default_tags {
                tags = {
                  Project     = var.project_name
                  Environment = var.environment
                  ManagedBy   = "terraform"
                }
              }
            }
        '''),
        "gcp": dedent('''\
            terraform {
              required_version = ">= 1.0"
              
              required_providers {
                google = {
                  source  = "hashicorp/google"
                  version = "~> 5.0"
                }
              }
              
              backend "gcs" {
                # Configure in backend.hcl
              }
            }

            provider "google" {
              project = var.gcp_project
              region  = var.gcp_region
            }
        '''),
        "azure": dedent('''\
            terraform {
              required_version = ">= 1.0"
              
              required_providers {
                azurerm = {
                  source  = "hashicorp/azurerm"
                  version = "~> 3.0"
                }
              }
              
              backend "azurerm" {
                # Configure in backend.hcl
              }
            }

            provider "azurerm" {
              features {}
            }
        '''),
    }
    
    return dedent(f'''\
        # {project_name} Infrastructure
        # Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}

{providers.get(cloud, providers["aws"])}

        # Module references
        module "network" {{
          source = "./modules/network"
          
          project_name = var.project_name
          environment  = var.environment
        }}

        module "compute" {{
          source = "./modules/compute"
          
          project_name = var.project_name
          environment  = var.environment
          
          depends_on = [module.network]
        }}

        module "storage" {{
          source = "./modules/storage"
          
          project_name = var.project_name
          environment  = var.environment
        }}
    ''')


def generate_variables(project_name: str, cloud: str) -> str:
    """Generate variables.tf."""
    
    cloud_vars = {
        "aws": """\
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}
""",
        "gcp": """\
variable "gcp_project" {
  description = "GCP project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}
""",
        "azure": """\
variable "azure_location" {
  description = "Azure location"
  type        = string
  default     = "West US 2"
}
""",
    }
    
    return dedent(f'''\
        # Variables for {project_name}
        # Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        variable "project_name" {{
          description = "Project name for resource naming"
          type        = string
          default     = "{project_name}"
        }}

        variable "environment" {{
          description = "Environment (dev, staging, prod)"
          type        = string
          default     = "dev"
          
          validation {{
            condition     = contains(["dev", "staging", "prod"], var.environment)
            error_message = "Environment must be dev, staging, or prod."
          }}
        }}

{cloud_vars.get(cloud, cloud_vars["aws"])}

        variable "tags" {{
          description = "Additional tags"
          type        = map(string)
          default     = {{}}
        }}
    ''')


def generate_outputs(cloud: str, resources: list) -> str:
    """Generate outputs.tf."""
    return dedent(f'''\
        # Outputs
        # Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        output "project_name" {{
          description = "Project name"
          value       = var.project_name
        }}

        output "environment" {{
          description = "Environment"
          value       = var.environment
        }}

        {"output \"vpc_id\" { value = module.network.vpc_id }" if "network" in resources else ""}
        {"output \"compute_instance_ids\" { value = module.compute.instance_ids }" if "compute" in resources else ""}
        {"output \"storage_bucket_name\" { value = module.storage.bucket_name }" if "storage" in resources else ""}
    ''')


def generate_module(project_name: str, cloud: str, resource: str) -> str:
    """Generate module main.tf for a specific resource."""
    
    modules = {
        ("aws", "compute"): dedent('''\
            # AWS Compute Module

            variable "project_name" { type = string }
            variable "environment" { type = string }

            resource "aws_instance" "main" {
              ami           = data.aws_ami.amazon_linux.id
              instance_type = var.environment == "prod" ? "t3.medium" : "t3.micro"
              
              tags = {
                Name = "${var.project_name}-${var.environment}"
              }
            }

            data "aws_ami" "amazon_linux" {
              most_recent = true
              owners      = ["amazon"]
              
              filter {
                name   = "name"
                values = ["amzn2-ami-hvm-*-x86_64-gp2"]
              }
            }

            output "instance_ids" {
              value = [aws_instance.main.id]
            }
        '''),
        ("aws", "storage"): dedent('''\
            # AWS Storage Module

            variable "project_name" { type = string }
            variable "environment" { type = string }

            resource "aws_s3_bucket" "main" {
              bucket = "${var.project_name}-${var.environment}-data"
            }

            resource "aws_s3_bucket_versioning" "main" {
              bucket = aws_s3_bucket.main.id
              versioning_configuration {
                status = "Enabled"
              }
            }

            resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
              bucket = aws_s3_bucket.main.id
              rule {
                apply_server_side_encryption_by_default {
                  sse_algorithm = "AES256"
                }
              }
            }

            output "bucket_name" {
              value = aws_s3_bucket.main.id
            }
        '''),
        ("aws", "network"): dedent('''\
            # AWS Network Module

            variable "project_name" { type = string }
            variable "environment" { type = string }

            resource "aws_vpc" "main" {
              cidr_block           = "10.0.0.0/16"
              enable_dns_hostnames = true
              enable_dns_support   = true
              
              tags = {
                Name = "${var.project_name}-${var.environment}-vpc"
              }
            }

            resource "aws_subnet" "public" {
              count             = 2
              vpc_id            = aws_vpc.main.id
              cidr_block        = "10.0.${count.index + 1}.0/24"
              availability_zone = data.aws_availability_zones.available.names[count.index]
              
              tags = {
                Name = "${var.project_name}-${var.environment}-public-${count.index + 1}"
              }
            }

            data "aws_availability_zones" "available" {
              state = "available"
            }

            output "vpc_id" {
              value = aws_vpc.main.id
            }
        '''),
    }
    
    # Return cloud-specific module or generic fallback
    key = (cloud, resource)
    if key in modules:
        return modules[key]
    
    # Generic fallback
    return dedent(f'''\
        # {cloud.upper()} {resource.title()} Module
        # Generated by skillpack on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        variable "project_name" {{ type = string }}
        variable "environment" {{ type = string }}

        # TODO: Add {cloud} {resource} resources

        output "{resource}_id" {{
          value = null
        }}
    ''')


def generate_tfvars_example(project_name: str, cloud: str) -> str:
    """Generate terraform.tfvars.example."""
    return dedent(f'''\
        # Example terraform.tfvars
        # Copy to terraform.tfvars and customize

        project_name = "{project_name}"
        environment  = "dev"

        {"aws_region = \"us-west-2\"" if cloud == "aws" else ""}
        {"gcp_project = \"my-project-id\"" if cloud == "gcp" else ""}
        {"gcp_region = \"us-central1\"" if cloud == "gcp" else ""}
        {"azure_location = \"West US 2\"" if cloud == "azure" else ""}

        tags = {{
          Team = "platform"
        }}
    ''')


def generate_readme(project_name: str, cloud: str, resources: list) -> str:
    """Generate README.md."""
    return dedent(f'''\
        # {project_name} Infrastructure

        Generated by skillpack iac-boilerplate on {datetime.now().strftime("%Y-%m-%d %H:%M")}

        ## Cloud: {cloud.upper()}

        ## Resources
        {chr(10).join([f"- {r}" for r in resources])}

        ## Usage

        ```bash
        # Initialize
        terraform init

        # Plan
        terraform plan -var-file=terraform.tfvars

        # Apply
        terraform apply -var-file=terraform.tfvars

        # Destroy
        terraform destroy -var-file=terraform.tfvars
        ```

        ## Structure
        ```
        .
        ├── main.tf              # Provider and module config
        ├── variables.tf         # Input variables
        ├── outputs.tf           # Output values
        ├── terraform.tfvars     # Variable values (git-ignored)
        └── modules/
            ├── compute/
            ├── storage/
            └── network/
        ```

        ## Best Practices
        - Use workspaces for environments: `terraform workspace new prod`
        - Store state remotely (S3, GCS, Azure Blob)
        - Use `terraform fmt` before commits
    ''')
