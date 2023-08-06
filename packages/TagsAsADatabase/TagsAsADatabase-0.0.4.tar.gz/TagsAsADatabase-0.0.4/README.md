# AWS Tags As A DataBase (AWS TaaDB) 🚀🚀

[![PyPI version](https://badge.fury.io/py/das2.svg)](https://badge.fury.io/py/TagsAsADatabase)
![GitHub issues](https://img.shields.io/github/issues/OrenLeung/AWSTagsAsADatabase)
![GitHub contributors](https://img.shields.io/github/contributors/OrenLeung/AWSTagsAsADatabase)
![GitHub last commit](https://img.shields.io/github/last-commit/OrenLeung/AWSTagsAsADatabase)


**NOTE: Please Don't Acutally Use this as a Database!** 
**Please Reference [An AWS Database Safari By Corey Quinn](https://www.lastweekinaws.com/blog/an-aws-database-safari/) for acutally databases**

## About 🏎️🏎️
Corey Quinn describes how to use AWS Managed DNS Offering (Route 53) as a DataBase in [Route 53, Amazon Premier Database By Corey Quinn](https://www.lastweekinaws.com/blog/route-53-amazons-premier-database/) & [Twitter Thread](https://twitter.com/quinnypig/status/1120653859561459712?lang=en).

To continue to trend to misuse random AWS resources as, AWS Tags As A Database (**AWS TaaDb**) Python🐍🐍 library was created to use AWS Tags feature as a Key-Value database.

It uses AWS EC2 instance Tags as the database in its current configuration but nothing is stopping it from using any AWS resource that allows the use of Tags

## Installation 🚀🚀

```bash
pip install TagsAsADatabase
```

## Examples 🚀🚀
```python
# imports AWS Tags As A Database Library
from TagsAsADatabase import DatabaseClient

# create a database client (using AWS EC2 instance Tags as backend)
# pass in the resource id of an ec2 instance
# region_name defaults to us-east-1
dbClient = DatabaseClient(INSTANCE_ID, region_name=REGION_NAME)

# gets all the current Keys of the key-value database
# returns type List[str]
print(dbClient.getAllKeys())

# gets all the key-value pairs
# returns as type Dict[str, str]
print(dbClient.getAllKeyPairs())

# adds or updates the VALUE at KEY 
dbClient.updateKeyValue(KEY, VALUE)

# deletes the key-value pair at KEY
dbClient.deleteKeyValue(KEY)
```

## Resources 🚀🚀
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#instance
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.tags
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.create_tags
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance.delete_tags
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Tag.reload