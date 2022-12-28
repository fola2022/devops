
# # 
# #==========================================================
# #== aws/security-group/sg_rule.tf
# #==========================================================
# #


#################################################
# Main Security Group Rule

###################################
# Ingress 
###################################
# Security group rules with "cidr_blocks" and it uses list of rules names
resource "aws_security_group_rule" "main_ingress_rules" {
  count = var.create ? length(var.ingress_rules) : 0

  security_group_id = "${aws_security_group.xeta_main_sg.id}"
  type              = "ingress"

  cidr_blocks      = var.ingress_cidr_blocks
  description      = var.rules[var.ingress_rules[count.index]][3]

  from_port = var.rules[var.ingress_rules[count.index]][0]
  to_port   = var.rules[var.ingress_rules[count.index]][1]
  protocol  = var.rules[var.ingress_rules[count.index]][2]
}


##################################
# Egress - List of rules (simple)
##################################
# Security group rules with "cidr_blocks" and it uses list of rules names
resource "aws_security_group_rule" "egress_rules" {
  count = var.create ? length(var.egress_rules) : 0

  security_group_id = "${aws_security_group.xeta_main_sg.id}"
  type              = "egress"

  cidr_blocks      = var.egress_cidr_blocks
  description      = var.rules[var.ingress_rules[count.index]][3]

  from_port = var.rules[var.egress_rules[count.index]][0]
  to_port   = var.rules[var.egress_rules[count.index]][1]
  protocol  = var.rules[var.egress_rules[count.index]][2]
}


# ##### AD Rules ################################

# ###################################
# # Ingress 
# ###################################
# # Security group rules with "cidr_blocks" and it uses list of rules names
# resource "aws_security_group_rule" "main_ingress_rules" {
#   count = var.create ? length(var.ingress_rules) : 0

#   security_group_id = "${aws_security_group.xeta_main_sg.id}"
#   type              = "ingress"

#   cidr_blocks      = var.ingress_cidr_blocks
#   description      = var.rules[var.ingress_rules[count.index]][3]

#   from_port = var.rules[var.ingress_rules[count.index]][0]
#   to_port   = var.rules[var.ingress_rules[count.index]][1]
#   protocol  = var.rules[var.ingress_rules[count.index]][2]
# }


# ##################################
# # Egress - List of rules (simple)
# ##################################
# # Security group rules with "cidr_blocks" and it uses list of rules names
# resource "aws_security_group_rule" "egress_rules" {
#   count = var.create ? length(var.egress_rules) : 0

#   security_group_id = "${aws_security_group.xeta_main_sg.id}"
#   type              = "egress"

#   cidr_blocks      = var.egress_cidr_blocks
#   description      = var.rules[var.ingress_rules[count.index]][3]

#   from_port = var.rules[var.egress_rules[count.index]][0]
#   to_port   = var.rules[var.egress_rules[count.index]][1]
#   protocol  = var.rules[var.egress_rules[count.index]][2]
# }




#############################################################
# Security Group Rule with Source Security Group
###################################
# Ingress

resource "aws_security_group_rule" "ingress_rules_with_source" {
  count = var.create && var.create_sg_with_source ? length(var.ingress_with_source_security_group_id) : 0

  security_group_id           = aws_security_group.xeta_sg_with_source.*.id[0]
  type                        = "ingress"

  source_security_group_id    = "${aws_security_group.xeta_main_sg.id}"
  description                 = var.rules[var.ingress_with_source_security_group_id[count.index]][3]

  from_port                   = var.rules[var.ingress_with_source_security_group_id[count.index]][0]
  to_port                     = var.rules[var.ingress_with_source_security_group_id[count.index]][1]
  protocol                    = var.rules[var.ingress_with_source_security_group_id[count.index]][2]
}


##################################
# Egress -
##################################

resource "aws_security_group_rule" "egress_rules_with_source" {
  count = var.create && var.create_sg_with_source ? length(var.egress_with_source_security_group_id) : 0
  
  security_group_id           = aws_security_group.xeta_sg_with_source.*.id[0]
  type                        = "egress"

  source_security_group_id    = "${aws_security_group.xeta_main_sg.id}"
  description                 = var.rules[var.egress_with_source_security_group_id[count.index]][3]

  from_port                   = var.rules[var.egress_with_source_security_group_id[count.index]][0]
  to_port                     = var.rules[var.egress_with_source_security_group_id[count.index]][1]
  protocol                    = var.rules[var.egress_with_source_security_group_id[count.index]][2]

}
