from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)

# 1. 보안을 위한 비밀키 (아무 문자나 길게 적으세요)
app.secret_key = 'super_secret_key_for_my_school'
# 2. 로그인 유지 시간 설정 (예: 30분 동안 활동 없으면 로그아웃)
app.permanent_session_lifetime = timedelta(minutes=30)

# 임시 데이터 저장소 (서버 재시작 전까지만 유지됨)
counsel_logs = []

# --- 로그인 정보 설정 ---
ADMIN_ID = "admin"      # 사용할 아이디
ADMIN_PW = "1234"       # 사용할 비밀번호

@app.route('/')
def index():
    # 로그인이 안 되어 있으면 로그인 페이지로 보냄
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html', logs=counsel_logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        
        # 아이디와 비번이 맞는지 확인
        if user_id == ADMIN_ID and user_pw == ADMIN_PW:
            session.permanent = True # 세션 유지 설정 적용
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return "<script>alert('정보가 일치하지 않습니다.'); history.back();</script>"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() # 세션 삭제 (로그아웃)
    return redirect(url_for('login'))

@app.route('/save', methods=['POST'])
def save():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    data = {
        "id": len(counsel_logs) + 1,
        "counselor": request.form['counselor'],
        "target": request.form['target'],
        "duration": request.form['duration'],
        "content": request.form['content']
    }
    counsel_logs.insert(0, data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)