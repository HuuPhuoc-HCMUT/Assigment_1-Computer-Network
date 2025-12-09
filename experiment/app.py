from flask import Flask, request, jsonify
from flask_cors import CORS # Cần thiết để cho phép Frontend truy cập

app = Flask(__name__)
# Cho phép tất cả các nguồn gốc (origins) truy cập API. 
# Trong thực tế, bạn nên chỉ định rõ tên miền của Frontend.
CORS(app) 


SAMPLE_ITEMS = [
    {"id": 1, "name": "Bút chì", "price": 5000},
    {"id": 2, "name": "Sổ tay A5", "price": 15000},
    {"id": 3, "name": "Tẩy", "price": 2000}
]



@app.route('/api/items', methods=['GET'])
def get_all_items():
    """
    Endpoint API này trả về toàn bộ danh sách vật phẩm.
    """
    try:
        # Logic: Lấy dữ liệu (giả định là từ Database)
        
        # 1. Tạo phản hồi JSON
        response = {
            'status': 'success',
            'data': SAMPLE_ITEMS,
            'count': len(SAMPLE_ITEMS)
        }
        # 2. Trả về phản hồi với mã 200 OK
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'message': f'Lỗi server khi lấy dữ liệu: {str(e)}'}), 500



@app.route('/api/greeting', methods=['POST'])
def get_greeting():
    """
    Endpoint API này nhận dữ liệu JSON từ Frontend và trả về lời chào.
    """
    try:
        # 1. Nhận dữ liệu từ yêu cầu POST
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'message': 'Dữ liệu không hợp lệ'}), 400

        name = data.get('name')
        
        # 2. Xử lý logic Backend
        greeting_message = f"Chào mừng bạn, {name}! Bạn đã kết nối thành công với API Flask."
        
        # 3. Trả về phản hồi JSON
        response = {
            'status': 'success',
            'greeting': greeting_message
        }
        return jsonify(response), 200

    except Exception as e:
        # Xử lý lỗi nếu có
        return jsonify({'message': f'Lỗi server: {str(e)}'}), 500

if __name__ == '__main__':
    # Chạy ứng dụng Flask trên cổng mặc định 5000
    app.run(debug=True, port=5000)