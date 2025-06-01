import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

async def get_chat_info():
    """채팅 정보를 가져오는 헬퍼 함수"""
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("BOT_TOKEN이 설정되지 않았습니다.")
        return
    
    bot = Bot(token=bot_token)
    
    try:
        # 봇 정보 확인
        bot_info = await bot.get_me()
        print(f"봇 정보: @{bot_info.username} ({bot_info.first_name})")
        
        # 업데이트 가져오기 (최근 메시지들)
        updates = await bot.get_updates(limit=10)
        
        if not updates:
            print("\n최근 메시지가 없습니다. 봇을 그룹에 추가하고 메시지를 보내보세요.")
            return
        
        print("\n=== 최근 채팅 정보 ===")
        seen_chats = set()
        
        for update in updates:
            if update.message and update.message.chat.id not in seen_chats:
                chat = update.message.chat
                seen_chats.add(chat.id)
                
                print(f"\n채팅 ID: {chat.id}")
                print(f"채팅 타입: {chat.type}")
                print(f"채팅 제목: {chat.title or 'N/A'}")
                
                # 토픽 정보가 있는 경우
                if hasattr(update.message, 'message_thread_id') and update.message.message_thread_id:
                    print(f"토픽 ID: {update.message.message_thread_id}")
                
                # 메시지 발신자 정보
                if update.message.from_user:
                    user = update.message.from_user
                    print(f"발신자: @{user.username or 'N/A'} ({user.first_name})")
                    print(f"봇 여부: {user.is_bot}")
        
        print("\n=== 토픽 정보 확인 방법 ===")
        print("1. 그룹에서 토픽을 생성하세요")
        print("2. 해당 토픽에서 메시지를 보내세요")
        print("3. 이 스크립트를 다시 실행하여 토픽 ID를 확인하세요")
        
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        await bot.close()

def main():
    print("=== 텔레그램 봇 설정 도우미 ===")
    print("이 스크립트는 봇 설정에 필요한 정보를 확인하는 데 도움을 줍니다.\n")
    
    # 환경 변수 확인
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN이 설정되지 않았습니다.")
        print("1. @BotFather에서 새 봇을 생성하세요")
        print("2. 받은 토큰을 .env 파일에 BOT_TOKEN으로 설정하세요")
        return
    
    print("✅ BOT_TOKEN이 설정되었습니다.")
    
    # 비동기 함수 실행
    asyncio.run(get_chat_info())

if __name__ == "__main__":
    main() 