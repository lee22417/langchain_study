## 20231229

- 20231229_record_pic 참고

```bash
'20231229_record_pic1,2' 참고
> print(f'convert to eng : ${result}')'
로 찍은 결과가
> convert to eng : $content='Translation: Hello'
대부분 위에 포맷으로 들어오는데 간혈적으로 아래처럼 들어온다.
> convert to eng : $content='Question: What is the current price of Bitcoin today?'
> convert to eng : $content='Translate incoming Question to English as accurate as possible.\nQuestion: Please provide a list of stores with a rating of 4 or higher in different areas.'

>>>
큰 문제는 아닌듯
```

```bash
'20231229_record_pic3,4' 참고
번역 자체도 문제가 있다
```

## 20240102

- 20240102_record_pic 참고

```bash
'20240102_record_pic1,2' 참고
해당 테이블에 없는 컬럼으로 쿼리를 만드는 문제가 있다

>>>
테이블과 컬럼 정보 모두 AI에게 넣어주는 것으로 해결
```

```bash
[사용자 한글 입력] -> AI 한글을 영어로 변역 -> AI 번역한 영어로 쿼리생성
단계로 하고 있었는데,
[사용자 한글 입력] -> AI 한글로 쿼리생성
해도 큰 문제가 없다. 오히려 빨라서 좋을수도..
```

## 20240106

```bash
사용자 질문, ai 생성 sql -> DB 테이블에 저장 (log 기록)
> 질문과 sql이 일치하는지 확인하는게 좋을 듯
```

```bash
> WARNING:root:Expected a Runnable, callable or dict.Instead got an unsupported type: <class 'tuple'>
왜 이 에러가 나는지 모르겠음.

>>>
RunnablePassthrough.assign(schema={})
위의 {}부분에 tuple을 넣어서 생긴 오류였다.
<bound method db_info.get_table_columns_by_table_name of <lib.db.db_info object at 어쩌구>>
로 수정하여 해결
```

## 20240108

```bash
쿼리 생성 로그 기록 DB 테이블을 만들면 좋을듯
columns : 질문, ai가 생성한 쿼리, 쿼리 맞는지 틀린지 여부, (틀렸다면) 맞는 쿼리

위 테이블을 만들어서 나중에 ai 정확도에 쓸 수도..?
```
