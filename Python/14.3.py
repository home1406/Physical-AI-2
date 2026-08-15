# Ollama 설치
# curl -fsSL https://ollama.com/install.sh | sh
# sudo systemctl start ollama

# 모델 다운로드 (라즈베리파이 권장)
# ollama pull gemma2:2b      # 1.6GB, 가장 빠름
# ollama pull llama3.2:1b    # 1.3GB

# 테스트
# ollama run gemma2:2b "안녕! 한국어로 자기소개 해줘"
import ollama, time

def chat_stream(prompt, model="gemma2:2b"):
    t0     = time.perf_counter()
    stream = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    print(f"[{model}] ", end="", flush=True)
    resp = ""
    for chunk in stream:
        text = chunk["message"]["content"]
        print(text, end="", flush=True)
        resp += text
    elapsed = time.perf_counter() - t0
    print(f"\n[{elapsed:.1f}초 | {len(resp)}자]")
    return resp
