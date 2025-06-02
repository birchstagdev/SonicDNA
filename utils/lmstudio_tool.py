import requests
import time


class LMStudioTool:
    def __init__(self, model="deepseek-r1-0528-qwen3-8b@q3_k_l", port=1234, max_retries=3, timeout=20):
        self.api_url = f"http://localhost:{port}/v1/chat/completions"
        self.model = model
        self.max_retries = max_retries
        self.timeout = timeout

    def ask(
            self,
            prompt,
            system_msg="You are an expert in Sonic DNA encoding. Reply with precision and conciseness.",
            temperature=0.2,
            max_tokens=256
    ):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = requests.post(self.api_url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data['choices'][0]['message']['content'].strip()
            except Exception as e:
                print(f"[LMStudioTool] Error (attempt {attempt}): {e}")
                if attempt < self.max_retries:
                    time.sleep(1)
                else:
                    raise


# ---- USAGE ----

if __name__ == "__main__":
    # Replace "your-model-name" with your actual model in LM Studio (e.g., "phi3", "llama3", etc.)
    lm = LMStudioTool(model="deepseek-r1-0528-qwen3-8b@q3_k_l", port=1234)

    # Example robust query:
    prompt = (
        "Given this Sonic DNA code: Tz9999. In Sonic DNA, T is timbre. "
        "The first letter (a-z) is grittiness (a=smoothest, z=most gritty), "
        "and the following 4 digits (0000-9999) indicate a specific tone or color. "
        "What does Tz9999 represent? Reply in a single clear sentence."
    )
    result = lm.ask(prompt)
    print("LLM answer:", result)