#!/bin/bash

# Set the S3 bucket name and file path
BUCKET_NAME="mys3bucket1o1"
files=( "basesuppression/suppression.xml" "specific_vuln/suppression.xml" )
output_file="mergedfile.xml"

# set the AWS credentials
aws_access_key_id='AKIAVZ7NVR76O3QAESQF'
aws_secret_access_key='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'

for i in "${files[@]}"
do
  #aws s3 cp s3://$BUCKET_NAME/$i . --region us-east-1 --profile default &> /dev/null
  export AWS_ACCESS_KEY_ID=$aws_access_key_id ; export AWS_SECRET_ACCESS_KEY=$aws_secret_access_key ; aws s3 cp s3://$BUCKET_NAME/$i .
done

file1=${files[0]}
file2=${files[1]}

# extract all the content from <suppress> upto the end of the file
data=$(cat "$file2" | sed -n -e '/<suppress>/,$p')

# insert the data extracted from $file2 to the $file1
cat "$file1" > $output_file
echo "$data" >> $output_file

# remove all the </suppressions> entries from $file1
sed -i 's|</suppressions>||g' $output_file

# insert </suppressions> to the end of file1
echo "</suppressions>" >> $output_file

# remove all empty lines from output file
sed -i '/^$/d' $output_file
