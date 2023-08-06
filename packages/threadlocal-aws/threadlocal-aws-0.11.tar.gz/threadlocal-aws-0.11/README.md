# Threadlocal AWS clients and resources

Convinient access to threadlocal boto3 clients and resources.

## Why

Suppose you have non-trivial serverless project with several lambdas and
some shared common code. Normally you would want to create used resources
outside of the lambda handler so that they don't need to be recreated
during a warm start of the lambda. Also you might want to share the created
resources in different parts of the code. This might lead to you creating
lots of resources that end up not being needed on the actual code path
that gets taken by the lambda function.

With threadlocal-aws the resources are created as a side effect of the first
call on the code path and subsequent calls use the same resources from a
threadlocal cache. The arguments to the functions are used as cache keys
so you can trivially use clients that interact with different regions for example
just by passing the region to the threadlocal function you use and a matching
session will be found.

Different accounts can be used by creating sessions towards the accounts and
passing them to the threadlocal function.

## Where not to use

All of the created resources are stored for the lifetime of the program so it is
only a good idea to use in places where the lifetime of the program is limited.
Also an environment with lots of threads combined with a long lifetime like some web
development frameworks is not a good idea.

## Usage

### Resource

Lots of boto3 aws modules have resources. For example easy to iterate all instances:
```python
from threadlocal_aws.resources import ec2

for instance in ec2().instances.all():
     print(instance.id)
```

You can get an item from dynamo with just two lines of code:
```python
from threadlocal_aws.resources import dynamodb_Table as table

dynamo_resp = table("my-table", region="eu-central-1").get_item(Key="foo#bar#123")
```

Or iterate all objects in a bucket:
```python
from threadlocal_aws.resources import s3_Bucket as bucket

for s3_obj in bucket("my-unique-bucket").objects.all():
     print(s3_obj.key)
```

### Client

```python
from threadlocal_aws.clients import ec2

instance = ec2().describe_instances(InstanceIds=["i-0fd31cg97d77ddfff"])
```
