# tags
Evaluates tags associated with AWS resources for compliance.

## Description
This script takes as standard input the output from the AWS CLI command [resourcegroupstaggingapi](https://docs.aws.amazon.com/cli/latest/reference/resourcegroupstaggingapi/index.html). It checks each resource for the presence of tags defined by the tuple REQUIRED_TAGS.

## Usage

1. Update the REQUIRED_TAGS tuple to include the tags you want to search for.
2. Ensure you have installed and configured the [AWS Command Line Interface](https://aws.amazon.com/cli/).
3. Run the following command to generate the report:

`aws resourcegroupstaggingapi get-resources --region REGION | python tags.py`

## Output

Resources that have no tags are listed in the section named "RESOURCES WITH NO TAGS".

Resources that have tags but do not contain all the tags listed in the REQUIRED_TAGS tuple are listed in the section named "RESOURCES WITH NON-COMPLIANT TAGS".

Resources that have all the tags listed in the REQUIRED_TAGS tuple are listed in the section named "RESOURCES WITH COMPLIANT TAGS".
