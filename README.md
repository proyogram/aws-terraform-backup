# aws-terraform-backup

## 前提

本モジュールでは、terraformのtfstateファイルを保管するS3バケットを作成する必要がある。
作成したS3バケット名をprovider.tfの`bucket`に設定する。
当リポジトリでは、`tf-backend-proyogram`という名前のバケットを用いているが、S3バケット名は一意である必要があるため、この名前をそのまま流用することはできない。


## 使い方
1. main.tfの以下の設定を変更する。
```
  prefix                = "<全てのリソースの頭につく値>"
  full_repository_id    = "<ユーザ名>/<レポジトリ名>"
  branch_name           = "<ブランチ名>"
```
2. `terraform plan`を実行。
3. plan結果が問題なければ、`terraform apply`を実行
4. 以上