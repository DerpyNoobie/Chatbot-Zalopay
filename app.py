from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# API Key của Groq
GROQ_API_KEY = "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"

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api', methods=['POST'])
def chat_api():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message parameter missing'}), 400

    user_message = data['message']

    try:
        # Prompt định nghĩa vai trò Robo-advisor
        system_prompt = (
            "Bạn là một Robo-advisor thông minh của ZaloPay tại Việt Nam. "
            "Nhiệm vụ của bạn là hỗ trợ người dùng quản lý giá cả, giải đáp thắc mắc về ZaloPay, "
            "và cung cấp lời khuyên tài chính phù hợp. Bạn luôn trả lời bằng tiếng Việt và giữ ngữ điệu chuyên nghiệp, thân thiện."
        )

        # Tạo payload cho Groq API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        payload = {
            "model": "llama3-8b-8192",  # Mô hình Groq bạn sử dụng
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            return jsonify({'error': f"Groq API error: {response.text}"}), response.status_code

        # Xử lý phản hồi từ Groq API
        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']['content'].strip()
        return jsonify({'response': assistant_message})

    except requests.RequestException as e:
        # Lỗi khi gửi yêu cầu tới Groq API
        print(f"Lỗi API Groq: {str(e)}")
        return jsonify({'error': f"Lỗi khi gửi yêu cầu tới API Groq: {str(e)}"}), 500

    except Exception as e:
        # Xử lý lỗi bất ngờ
        print(f"Lỗi bất ngờ: {str(e)}")
        return jsonify({'error': f"Lỗi bất ngờ: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
