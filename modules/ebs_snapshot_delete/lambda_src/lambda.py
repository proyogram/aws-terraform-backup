import boto3

ec2 = boto3.client("ec2")
account_id = boto3.client("sts").get_caller_identity()["Account"]
exceptions = []

def fetch_snapshot_ids():
    snapshot_id_list =[]
    response = ec2.describe_snapshots(
            Filters=[
                {
                    'Name': 'owner-id',
                    'Values': [account_id]
                }
            ]
            
        )
    for snapshot in response['Snapshots']:
        snapshot_id_list.append(snapshot['SnapshotId'])
        
    return snapshot_id_list
    
def fetch_active_snapshot_ids():
    active_snapshot_list =[]
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
    # スナップショットID一覧を取得
    snapshot_ids = fetch_snapshot_ids()
    # AMIと紐づくスナップショットID一覧を取得
    active_snapshot_ids = fetch_active_snapshot_ids()
    # 「全スナップショット」-「現在使用しているスナップショット」を取得
    unnesessary_snapshots = set(snapshot_ids)-set(active_snapshot_ids)
    
    # 不要なスナップショットを削除する
    for snapshot_id in unnesessary_snapshots:
        try:
            # スナップショットを削除する
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(f'Succeeded to delete {snapshot_id}.')
        except Exception as e:
            # スナップショットにAMIに紐づいている場合、処理をスキップする
            if e.response["Error"]["Code"] == "InvalidSnapshot.InUse":
                pass
            else:
                exceptions.append(e)
                print(f'Error occured in deleting {snapshot_id}:{e}')

    if len(exceptions) > 0:
        raise Exception("Error occured in deleting snapshots.")
