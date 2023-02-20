1. [ArgumentParser - 명령행 옵션, 인자와 부속 명령을 위한 파서](https://docs.python.org/ko/3/library/argparse.html#module-argparse)

- 프로그램 실행 시 커맨드 라인에 인수를 받아서 처리하는 것을 간단히 할 수 있도록 하는 표준 라이브러리

```python
from argparse import ArgumentParser

parser = ArgumentParser(
  prog = "The name of the prodram (default: os.path.basename(sys.argv[0])",
  description = "Text to display before the argument help(by default, no text)"
)
```

## 1.1. add_argument() 메서드
