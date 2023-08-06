import boto3
from typing import Any, List, Dict


class DatabaseClient:
    instance_id: str
    region_name: str
    Instance: Any

    def __init__(self, instance_id: str, region_name: str = "us-east-1") -> None:
        self.instance_id = instance_id
        self.region_name = region_name

        ec2 = boto3.resource('ec2', region_name=self.region_name)
        Instance = ec2.Instance(self.instance_id)
        self.Instance = Instance

    def getAllKeys(self) -> List[str]:
        keys1: List[str] = []

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.reload
        self.Instance.tags.reload()

        tags: List[Dict[str, str]] = self.Instance.tags

        for tag in tags:
            key: str = tag["Key"]
            keys1.append(key)

        return keys1

    def getAllKeyPairs(self) -> Dict[str, str]:
        tagDictonary: Dict[str, str] = {}

        tags: List[Dict[str, str]] = self.Instance.tags

        for tag in tags:
            key: str = tag["Key"]
            value: str = tag["Value"]
            tagDictonary[key] = value

        return tagDictonary

    # Add/Update Key Value pair
    def updateKeyValue(self, key: str, value: str) -> None:
        self.Instance.create_tags(
            Tags=[{'Key': key, 'Value': value}, ])

    def deleteKeyValue(self, key: str) -> None:
        self.Instance.delete_tags(Tags=[{'Key': key, }, ])
