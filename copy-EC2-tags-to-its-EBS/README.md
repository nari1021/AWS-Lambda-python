# copy EC2 tags to its EBS

다른 사람이 작성한 코드를 가져와서 주석만 한글로 달았습니다.
다른 분의 코드여서 제가 함부로 수정하기가 죄송해서 수정한 것은....
한 줄 지웠습니다.. 불필요한 코드 딱 한줄..!

# Error

## 1. when calling the CreateTags operation: Value ( empty ) for parameter tagSet is invalid. You must specify one or more tags to create

위와 같은 에러가 난다면, `copy_ec2_tags`에서 비교하는 4가지 if문의 태그 값이 없기 때문입니다. 

해결 방법은 2가지 입니다.
1. 자신이 EC2에 넣어둔 태그의 키 값으로 if문을 수정한다.
2. EC2에 현재 if 문 4개에 들어있는 키 값을 가진 태그를 추가한다.

저의 경우... if 문의 값(Env, Tier, DataClass, JiraTicket) 중에 하나를 Name으로 수정했습니다.
