module "ebs_snapshot_delete" {
  source = "./modules/ebs_snapshot_delete"
  prefix = "tf-ebs-snapshot-delete"
  cron_delete_schedule="cron(0 22 1 * ? *)"
}
