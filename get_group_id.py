import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_group_id():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN이 설정되지 않았습니다.")
        print("1. .env 파일을 확인하세요")
        print("2. BOT_TOKEN=your_actual_token 형태로 설정하세요")
        return
    
    print(f"🤖 봇 토큰: {bot_token[:10]}...")
    
    try:
        # getUpdates API 호출
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url)
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ API 오류: {data.get('description', 'Unknown error')}")
            return
        
        updates = data.get('result', [])
        
        if not updates:
            print("📝 최근 메시지가 없습니다.")
            print("\n다음 단계를 수행하세요:")
            print("1. 봇을 그룹에 추가")
            print("2. 그룹에서 아무 메시지나 전송")
            print("3. 이 스크립트를 다시 실행")
            return
        
        print("\n📋 발견된 채팅 정보:")
        print("-" * 50)
        
        seen_chats = set()
        for update in updates:
            if 'message' in update:
                chat = update['message']['chat']
                chat_id = chat['id']
                
                if chat_id not in seen_chats:
                    seen_chats.add(chat_id)
                    
                    print(f"채팅 ID: {chat_id}")
                    print(f"채팅 타입: {chat.get('type', 'unknown')}")
                    print(f"채팅 제목: {chat.get('title', 'N/A')}")
                    
                    if chat.get('type') == 'supergroup':
                        print(f"✅ 이것이 그룹 채팅 ID입니다: {chat_id}")
                    
                    print("-" * 30)
        
        print("\n💡 팁:")
        print("- 그룹 채팅 ID는 보통 음수입니다 (예: -1001234567890)")
        print("- 'supergroup' 타입이 일반적인 그룹입니다")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    get_group_id() 