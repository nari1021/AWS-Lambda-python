# how to use this folder

1. Login AWS console by your account.

2. Create IAM Policy using `aws-lambda-ec2-policy.json` file.
    - Region
    - Account Number
    - You should change 2 of things on the json file.

3. Create IAM Role having a create policy.

4. Make 2 AWS Lambda funtion.
    - ec2-auto-start function
    - ec2-auto-stop function

5. Copy and Paste python file on Each function

6. If you want to use different tag name, you might change tag name in each file.

</br>

# 이 폴더의 사용법

1. AWS 콘솔에 자신의 계정으로 로그인을 합니다.

2. `aws-lambda-ec2-policy.json` 파일을 이용하여 IAM Policy를 생성합니다.
    - Region
    - Account number
    - json 파일에 위의 두 가지를 자신의 것으로 변경해야합니다.

3. 생성한 Policy를 갖는 Role을 생성합니다.

4. AWS Lambda 함수를 2개 생성합니다.
    - ec2-auto-start 함수 1개
    - ec2-auto-stop 함수 1개

5. 각각의 함수에 python 파일을 복사해서 붙여넣습니다.

6. 각자 auto start/stop 을 위한 태그가 다르다면, 코드안의 태그를 수정하여 사용하면 됩니다.