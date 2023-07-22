variable "prefix" {
  type        = string
  description = "全てのリソースの文字前に付与される値"
}

variable "cron_delete_schedule" {
  type        = string
  description = "スケジュールをcronで表現"
}
