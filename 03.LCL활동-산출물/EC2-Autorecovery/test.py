from pprint import pprint

Name = "sksh-argos-p-eks-ui-ng-worker-1"
InstanceId = "i-0ee1068391e87f588"
is_autorecovery = False
print(True if "eks" in Name else False)

instance_info = {
    "name" : Name,
    "instance_id": InstanceId,
    "autorecovery": is_autorecovery,
    "eks_node": True if "eks" in Name else False
}

pprint(instance_info)