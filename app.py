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
            "và cung cấp lời khuyên tài chính phù hợp. Bạn luôn trả lời bằng tiếng Việt và giữ ngữ điệu chuyên nghiệp, thân thiện.\n\n"
            "Các chủ đề phổ biến bao gồm:\n"
            "1. Hỗ trợ về các tính năng trong ứng dụng ZaloPay (ví dụ: kiểm tra số dư, thanh toán, khuyến mãi)\n"
            "2. Quản lý tài chính cá nhân (ví dụ: tiết kiệm, đầu tư, chi tiêu)\n"
            "3. Giải đáp các thắc mắc về bảo mật và thanh toán qua ZaloPay.\n\n"
            "Làm sao bạn có thể giúp tôi hôm nay?"
        )

        # Thêm các prompt mẫu cho các chủ đề khác nhau:
        if "tiết kiệm" in user_message or "tiết kiệm bao nhiêu" in user_message:
            user_message = "Tôi nên tiết kiệm bao nhiêu phần trăm thu nhập hàng tháng?"
            system_prompt = system_prompt + "\n\nUser Question: " + user_message + "\nAssistant Answer: Bạn nên tiết kiệm ít nhất 20% thu nhập hàng tháng để chuẩn bị cho các mục tiêu dài hạn hoặc tình huống khẩn cấp. Bạn có thể sử dụng tính năng 'Gửi tiết kiệm' trên ZaloPay."
        
        elif "khuyến mãi" in user_message:
            user_message = "Tôi muốn kiểm tra các khuyến mãi hiện tại trên ZaloPay."
            system_prompt = system_prompt + "\n\nUser Question: " + user_message + "\nAssistant Answer: Bạn vào mục 'Ưu đãi' trong ứng dụng ZaloPay để xem danh sách các khuyến mãi hiện tại. Đừng quên cập nhật ứng dụng thường xuyên để không bỏ lỡ ưu đãi mới."

        elif "thanh toán" in user_message or "liên kết thẻ" in user_message:
            user_message = "Tôi muốn biết làm thế nào để liên kết thẻ tín dụng?"
            system_prompt = system_prompt + "\n\nUser Question: " + user_message + "\nAssistant Answer: Bạn vào phần 'Liên kết tài khoản/thẻ' trong ứng dụng ZaloPay, chọn 'Liên kết thẻ tín dụng' và nhập thông tin thẻ theo hướng dẫn."

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }
        payload = {
            "model": "llama3-8b-8192",  # Mô hình Groq 
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

        response_data = response.json()
        assistant_message = response_data['choices'][0]['message']['content'].strip()
        return jsonify({'response': assistant_message})

    except requests.RequestException as e:
        print(f"Lỗi API Groq: {str(e)}")
        return jsonify({'error': f"Lỗi khi gửi yêu cầu tới API Groq: {str(e)}"}), 500

    except Exception as e:
        print(f"Lỗi bất ngờ: {str(e)}")
        return jsonify({'error': f"Lỗi bất ngờ: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
