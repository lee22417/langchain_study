## 20231229

- 20231229_diary_pic_png 참고

```python
# new_ai.py
def translate_msg(self, ask):
        try:
            result = []

            # ai가 실행할 행동 정의 (영어번역하기)
            translate = """
            Translate incoming Question to English as accurate as possible.
            Question: {question}
            """

            # 정의한 행동 요청 (영어번역 행동 요청)
            translate_prompt = ChatPromptTemplate.from_template(translate)
            translate_response = (
                translate_prompt
                | self.llm
            )

            # 위에 정의한 행동 실행 (영어번역 실행)
            result = translate_response.invoke({"question": ask})
            print(f'convert to eng : ${result}')
            return result.content
```

```bash
위 코드 참고,
> print(f'convert to eng : ${result}')'
로 찍은 결과가 대부분 이런 포맷으로 들어오는데
> convert to eng : $content='Translation: Hello'
간혈적으로 아래처럼 들어온다.
> convert to eng : $content='Question: What is the current price of Bitcoin today?'
> convert to eng : $content='Translate incoming Question to English as accurate as possible.\nQuestion: Please provide a list of stores with a rating of 4 or higher in different areas.'
처리가 필요함.
```
