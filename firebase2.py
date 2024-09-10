import pyrebase

# Firebase 설정
firebaseConfig = {
    "apiKey": "AIzaSyBhRFNM6BKCjgh0UmJ9DrLkAIOMXYIw9MQ",
    "authDomain": "labc-d8979.firebaseapp.com",
    "databaseURL": "https://labc-d8979-default-rtdb.firebaseio.com/",
    "storageBucket": "labc-d8979.appspot.com"
}

# Firebase 초기화
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def signup(email, password, user_id):
    try:
        # Firebase Authentication을 사용하여 사용자 생성
        user = auth.create_user_with_email_and_password(email, password)
        print("회원가입 성공: ", user['email'])
        
        # 사용자 ID를 데이터베이스에 저장
        db.child("user_ids").child(user_id).set({"email": email, "uid": user['localId']})
        print("사용자 ID가 데이터베이스에 저장되었습니다.")
    except Exception as e:
        print("회원가입 실패: ", e)

def login(user_id, password):
    try:
        # 데이터베이스에서 사용자 ID로 이메일 조회
        user_info = db.child("user_ids").child(user_id).get().val()
        if not user_info:
            print("로그인 실패: 사용자 ID를 찾을 수 없습니다.")
            return
        
        email = user_info['email']
        uid = user_info['uid']
        
        # Firebase Authentication을 사용하여 이메일과 비밀번호로 로그인
        user = auth.sign_in_with_email_and_password(email, password)
        
        if user['localId'] == uid:
            print("로그인 성공: ", user['email'])
        else:
            print("로그인 실패: 사용자 인증에 실패했습니다.")
    except Exception as e:
        print("로그인 실패: ", e)

if __name__ == "__main__":
    action = input("회원가입을 하려면 'signup', 로그인을 하려면 'login'을 입력하세요: ").strip().lower()

    if action == 'signup':
        email = input("이메일을 입력하세요: ").strip()
        password = input("비밀번호를 입력하세요: ").strip()
        user_id = input("사용자 ID를 입력하세요: ").strip()
        signup(email, password, user_id)
    elif action == 'login':
        user_id = input("사용자 ID를 입력하세요: ").strip()
        password = input("비밀번호를 입력하세요: ").strip()
        login(user_id, password)
    else:
        print("잘못된 입력입니다. 'signup' 또는 'login'을 입력하세요.")
        print("잘못된 입력입니다. 'signup' 또는 'login'을 입력하세요.")
