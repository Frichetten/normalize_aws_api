# normalize_aws_api
A quick script to normalize the AWS API into a single json file.

To use, download [botocore](https://github.com/boto/botocore) and run with the following command.

```
./normalize_aws_api.py <botocore data dir>
```

This will create an aws-api-definition.json in the current directory. I have one in this git repo, although I don't recommend relying on it as there is no guarantee it's up to date.
