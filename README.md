# sangho-llm-bot
LLM chat bot to use CrewAI

## 1. 프로젝트 세팅

- VSC
- Github 연동

## 2. 프로젝트 구성
- 가상환경을 설정 => Docker Container 개념 (공간을 분리해서 따로 관리하겠다.)
- python 3.8 열심히 개발을 했어요. 근데 우리가 배포할 서버가 3.3 버전의 파이썬이야.
  => 3.8함수를 썼다면 3.3에는 없는 함수야. => 오류. => 배포하고 나서 알겠죠.
  => 로컬에서 작업하는 환경과 호스트에서 작업하는 환경을 일치시켜 주기 위함.
  => Docker(Virtural Machine) // venv 모듈을 사용해서 환경 설정을 해주도록 하겠습니다.

> python3.10 -m venv .venv
> source .venv/bin/activate (MAC)
> .venv/Scripts/activate (Win)

## 3. 프로젝트

### 3-1. Ollama 모델 + CrewAI

(1) ollama 다운로드
(2) ollama를 통해서 llm 다운로드

> ollama pull llama3.1
> ollama pull phi3:3.8b
> ollama run phi3:3.8b

(3) CrewAI 설치
- 언어 모델의 API 관리를 편리하게 도와주는 라이브러리
- 모델 - 클로드, 젬미니, GPT3.5, GPT4o ..... => import OpenAI // 언어마다 SDK를 다운받아줘야해요.
  => CrewAI, LangChain이 이미 다 SDK구현을 끝내놓음.
  => LangChain 안하고 왜 CrewAI 하나요? => 가벼워서요. (러닝 커브가 낮아서요.)

> pip install crewai crewai-tools
> pip install langchain-ollama

### 3-2 Flack 사용해서 기본적인 챗봇