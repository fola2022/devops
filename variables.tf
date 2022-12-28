
#==========================================================
#== aws/security_group/variables.tf
#==========================================================


# variable "aws_region" {
#   type        = string
#   description = "AWS region being deployed to"
# }

variable "vpc_id" {
  type        = string
  description = "AWS tenant being deployed to"
}

# variable "region" {
#   type        = string
#   description = "The region where resources will be deployed to"
# }

variable "user" {
  type          = string
  description   = "The username of individual deploying the module"
}


variable "sg_name" {
  type        = string
  description = "Name of the security groups"
}

variable  "create_sg_with_source" {
  type        = bool
  description = "Whether to create security group with a source security group and all rules"
}
#### tags variables ##

variable "created_by" {
  type        = string
  description = "Automation used to create resource"
  default     = "Terraform"
}

variable "program" {
  type        = string
  description = "Program Name"
  default     = "PCS"
}


##########################################################################

variable "create" {
  description = "Whether to create security group and all rules"
  type        = bool
  #default     = true
}


variable "tags" {
  description = "A mapping of tags to assign to security group"
  type        = map(string)
  default     = {}
}

##########
# Ingress
##########
variable "ingress_rules" {
  description = "List of ingress rules to create by name"
  type        = list(string)
  default     = []
}

variable "ingress_with_self" {
  description = "List of ingress rules to create where 'self' is defined"
  type        = list(map(string))
  default     = []
}

variable "ingress_with_cidr_blocks" {
  description = "List of ingress rules to create where 'cidr_blocks' is used"
  type        = list(map(string))
  default     = []
}

variable "ingress_with_source_security_group_id" {
  description = "List of ingress rules to create where 'source_security_group_id' is used"
  type        = list(string)
  default     = []
}

variable "ingress_cidr_blocks" {
  description = "List of IPv4 CIDR ranges to use on all ingress rules"
  type        = list(string)
  default     = []
}

variable "egress_cidr_blocks" {
  description = "List of IPv4 CIDR ranges to use on all ingress rules"
  type        = list(string)
  default     = []
}

#########
# Egress
#########
variable "egress_rules" {
  description = "List of egress rules to create by name"
  type        = list(string)
  default     = []
}

variable "egress_with_self" {
  description = "List of egress rules to create where 'self' is defined"
  type        = list(map(string))
  default     = []
}

variable "egress_with_cidr_blocks" {
  description = "List of egress rules to create where 'cidr_blocks' is used"
  type        = list(map(string))
  default     = []
}

variable "egress_with_source_security_group_id" {
  description = "List of egress rules to create where 'source_security_group_id' is used"
  type        = list(string)
  default     = []
}
