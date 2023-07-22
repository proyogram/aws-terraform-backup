import json
import boto3

ec2 = boto3.client("ec2")
account_id = boto3.client("sts").get_caller_identity()["Account"]
snapshot_list =[]
active_snapshot_list =[]

def fetch_unnessesary_snapshot():
    response = ec2.describe_snapshots(
            Filters=[
                {
                    'Name': 'owner-id',
                    'Values': [account_id]
                }
            ]
            
        )
    for snapshot in response['Snapshots']:
        snapshot_list.append(snapshot['SnapshotId'])
        
    return snapshot_list
    
def fetch_active_snapshot():
    response = ec2.describe_images(
        Filters=[
                {
                    'Name': 'owner-id',
                    'Values': [account_id]
                }
            ]
    )
    
    for image in response['Images']:
        for bdm in image['BlockDeviceMappings']:
            active_snapshot_list.append(bdm['Ebs']['SnapshotId'])
            
    return active_snapshot_list

def lambda_handler(event, context):
    all_snapshot_list = fetch_unnessesary_snapshot()
    active_snapshot_list = fetch_active_snapshot()
    # 「全スナップショット」-「現在使用しているスナップショット」を取得
    unnesessary_snapshots = set(all_snapshot_list)-set(active_snapshot_list)
    
    # 不要なスナップショットの削除処理を以下に記載
    for snapshot_id in unnesessary_snapshots:
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        print(snapshot_id + "を削除しました。")
