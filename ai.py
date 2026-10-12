import os
import requests
import json


def analyze_chat(chat_text):
    # 调用 DeepSeek API
    url = "https://api.deepseek.com/chat/completions"

    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise RuntimeError("未配置 DeepSeek API Key")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-flash",
        "messages": [
            {
                "role": "system",
                "content": """你是聊天情绪分析助手。

    请根据双方的完整聊天上下文，分析对方可能的情绪。

    要求：
    1. 区分“我”和“对方”。
    2. 结合上下文分析，不要只看最后一句话。
    3. 不要过度猜测对方的心理。
    4. 如果信息不足，明确指出不确定性。
    5. 给出三条自然、不同风格的回复建议。

    只返回JSON对象，包含：
    emotion：可能的情绪
    confidence：判断可信程度（高、中、低）
    reason：分析依据
    suggestions：三条回复建议
    """
            },
            {
                "role": "user",
                "content": chat_text
            }
        ],
        "response_format": {
            "type": "json_object"
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    print("状态码：", response.status_code)

    response.raise_for_status()
    # 解析 JSON

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    analysis = json.loads(content)

    return analysis