import os
import json
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramForwarderBot:
    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.group_chat_id = int(os.getenv('GROUP_CHAT_ID', 0))
        
        # 기존 단일 봇 설정 (하위 호환성)
        self.legacy_target_topic_id = int(os.getenv('TARGET_TOPIC_ID', 0)) if os.getenv('TARGET_TOPIC_ID') else None
        self.legacy_source_bot_username = os.getenv('SOURCE_BOT_USERNAME', '')
        
        if not all([self.bot_token, self.group_chat_id]):
            raise ValueError("BOT_TOKEN과 GROUP_CHAT_ID는 필수 환경 변수입니다.")
        
        # 봇 매핑 설정 로드
        self.bot_mappings = self.load_bot_mappings()
        self.settings = self.load_settings()
        
        self.application = Application.builder().token(self.bot_token).build()
        self.setup_handlers()
    
    def load_bot_mappings(self):
        """봇 매핑 설정을 로드"""
        try:
            with open('bot_mapping.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                mappings = {}
                
                # JSON 파일의 매핑 로드
                for mapping in data.get('bot_mappings', []):
                    username = mapping['source_bot_username'].replace('@', '').lower()
                    mappings[username] = {
                        'topic_id': mapping['target_topic_id'],
                        'description': mapping.get('description', '')
                    }
                
                # 기존 환경 변수 설정이 있으면 추가 (하위 호환성)
                if self.legacy_source_bot_username and self.legacy_target_topic_id:
                    legacy_username = self.legacy_source_bot_username.replace('@', '').lower()
                    if legacy_username not in mappings:
                        mappings[legacy_username] = {
                            'topic_id': self.legacy_target_topic_id,
                            'description': '환경 변수에서 로드된 레거시 설정'
                        }
                
                logger.info(f"봇 매핑 로드 완료: {len(mappings)}개 봇 설정")
                for username, config in mappings.items():
                    logger.info(f"  @{username} -> 토픽 {config['topic_id']} ({config['description']})")
                
                return mappings
                
        except FileNotFoundError:
            logger.warning("bot_mapping.json 파일을 찾을 수 없습니다. 환경 변수 설정을 사용합니다.")
            if self.legacy_source_bot_username and self.legacy_target_topic_id:
                username = self.legacy_source_bot_username.replace('@', '').lower()
                return {
                    username: {
                        'topic_id': self.legacy_target_topic_id,
                        'description': '환경 변수 설정'
                    }
                }
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"bot_mapping.json 파일 파싱 오류: {e}")
            return {}
    
    def load_settings(self):
        """일반 설정을 로드"""
        try:
            with open('bot_mapping.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('settings', {
                    'forward_all_unknown_bots': False,
                    'default_topic_id': None,
                    'log_unknown_bots': True
                })
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                'forward_all_unknown_bots': False,
                'default_topic_id': None,
                'log_unknown_bots': True
            }
    
    def save_bot_mappings(self):
        """봇 매핑을 파일에 저장"""
        try:
            # 현재 매핑을 JSON 형태로 변환
            bot_mappings_list = []
            for username, config in self.bot_mappings.items():
                bot_mappings_list.append({
                    'source_bot_username': username,
                    'target_topic_id': config['topic_id'],
                    'description': config['description']
                })
            
            data = {
                'bot_mappings': bot_mappings_list,
                'settings': self.settings
            }
            
            with open('bot_mapping.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info("봇 매핑이 파일에 저장되었습니다.")
            return True
        except Exception as e:
            logger.error(f"봇 매핑 저장 중 오류: {e}")
            return False
    
    def setup_handlers(self):
        """메시지 및 명령어 핸들러 설정"""
        # 명령어 핸들러
        self.application.add_handler(CommandHandler("set", self.handle_set_command))
        self.application.add_handler(CommandHandler("list", self.handle_list_command))
        self.application.add_handler(CommandHandler("remove", self.handle_remove_command))
        self.application.add_handler(CommandHandler("help", self.handle_help_command))
        
        # 메시지 핸들러 (명령어가 아닌 일반 메시지)
        message_handler = MessageHandler(filters.ALL & ~filters.COMMAND, self.handle_message)
        self.application.add_handler(message_handler)
    
    async def handle_set_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """봇 매핑 설정 명령어 처리"""
        try:
            # 그룹에서만 동작
            if update.effective_chat.id != self.group_chat_id:
                return
            
            # 관리자 권한 확인 (선택사항)
            user = update.effective_user
            chat_member = await context.bot.get_chat_member(self.group_chat_id, user.id)
            if chat_member.status not in ['administrator', 'creator']:
                await update.message.reply_text("❌ 이 명령어는 관리자만 사용할 수 있습니다.")
                return
            
            # 명령어 파싱: /set @bot_username topic_id [description]
            args = context.args
            if len(args) < 2:
                await update.message.reply_text(
                    "❌ 사용법: `/set @bot_username topic_id [설명]`\n"
                    "예시: `/set @news_bot 123 뉴스 봇 매핑`",
                    parse_mode='Markdown'
                )
                return
            
            # 디버깅 로그 추가
            original_input = args[0]
            bot_username = args[0].replace('@', '').lower()
            logger.info(f"디버깅: 원본 입력 '{original_input}' -> 처리된 사용자명 '{bot_username}'")
            
            try:
                topic_id = int(args[1])
            except ValueError:
                await update.message.reply_text("❌ 토픽 ID는 숫자여야 합니다.")
                return
            
            description = ' '.join(args[2:]) if len(args) > 2 else f"@{bot_username}의 메시지를 토픽 {topic_id}로 포워딩"
            
            # 매핑 추가/업데이트
            old_mapping = self.bot_mappings.get(bot_username)
            self.bot_mappings[bot_username] = {
                'topic_id': topic_id,
                'description': description
            }
            
            # 파일에 저장
            if self.save_bot_mappings():
                if old_mapping:
                    await update.message.reply_text(
                        f"✅ 봇 매핑이 업데이트되었습니다!\n"
                        f"@{bot_username}: 토픽 {old_mapping['topic_id']} → {topic_id}\n"
                        f"설명: {description}"
                    )
                else:
                    await update.message.reply_text(
                        f"✅ 새 봇 매핑이 추가되었습니다!\n"
                        f"@{bot_username} → 토픽 {topic_id}\n"
                        f"설명: {description}"
                    )
            else:
                await update.message.reply_text("❌ 설정 저장 중 오류가 발생했습니다.")
                
        except Exception as e:
            logger.error(f"set 명령어 처리 중 오류: {e}")
            await update.message.reply_text("❌ 명령어 처리 중 오류가 발생했습니다.")
    
    async def handle_list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """봇 매핑 목록 조회 명령어 처리"""
        try:
            # 그룹에서만 동작
            if update.effective_chat.id != self.group_chat_id:
                return
            
            if not self.bot_mappings:
                await update.message.reply_text("📝 설정된 봇 매핑이 없습니다.")
                return
            
            message = "📋 **현재 봇 매핑 설정:**\n\n"
            for i, (username, config) in enumerate(self.bot_mappings.items(), 1):
                message += f"{i}. @{username} → 토픽 {config['topic_id']}\n"
                if config['description']:
                    message += f"   📝 {config['description']}\n"
                message += "\n"
            
            message += "💡 **사용법:**\n"
            message += "• `/set @bot_username topic_id [설명]` - 매핑 추가/수정\n"
            message += "• `/remove @bot_username` - 매핑 삭제\n"
            message += "• `/list` - 매핑 목록 조회"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"list 명령어 처리 중 오류: {e}")
            await update.message.reply_text("❌ 명령어 처리 중 오류가 발생했습니다.")
    
    async def handle_remove_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """봇 매핑 제거 명령어 처리"""
        try:
            # 그룹에서만 동작
            if update.effective_chat.id != self.group_chat_id:
                return
            
            # 관리자 권한 확인
            user = update.effective_user
            chat_member = await context.bot.get_chat_member(self.group_chat_id, user.id)
            if chat_member.status not in ['administrator', 'creator']:
                await update.message.reply_text("❌ 이 명령어는 관리자만 사용할 수 있습니다.")
                return
            
            # 명령어 파싱: /remove @bot_username
            args = context.args
            if len(args) != 1:
                await update.message.reply_text(
                    "❌ 사용법: `/remove @bot_username`\n"
                    "예시: `/remove @news_bot`",
                    parse_mode='Markdown'
                )
                return
            
            bot_username = args[0].replace('@', '').lower()
            
            if bot_username in self.bot_mappings:
                removed_mapping = self.bot_mappings.pop(bot_username)
                if self.save_bot_mappings():
                    await update.message.reply_text(
                        f"✅ @{bot_username} 매핑이 제거되었습니다.\n"
                        f"(토픽 {removed_mapping['topic_id']})"
                    )
                else:
                    # 실패 시 복원
                    self.bot_mappings[bot_username] = removed_mapping
                    await update.message.reply_text("❌ 설정 저장 중 오류가 발생했습니다.")
            else:
                await update.message.reply_text(f"❌ @{bot_username}에 대한 매핑을 찾을 수 없습니다.")
                
        except Exception as e:
            logger.error(f"remove 명령어 처리 중 오류: {e}")
            await update.message.reply_text("❌ 명령어 처리 중 오류가 발생했습니다.")
    
    async def handle_help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """도움말 명령어 처리"""
        try:
            # 그룹에서만 동작
            if update.effective_chat.id != self.group_chat_id:
                return
            
            help_text = """
🤖 **텔레그램 포워더 봇 도움말**

**명령어:**
• `/set @bot_username topic_id [설명]` - 봇 매핑 추가/수정
• `/list` - 현재 매핑 목록 조회
• `/remove @bot_username` - 봇 매핑 삭제
• `/help` - 이 도움말 표시

**사용 예시:**
• `/set @news_bot 123 뉴스 봇`
• `/set @weather_bot 456`
• `/remove @news_bot`

**동작 방식:**
1. 메인 채널에서 매핑된 봇이 메시지 전송
2. 자동으로 해당 토픽으로 포워딩

**권한:** 관리자만 설정 변경 가능
            """
            
            await update.message.reply_text(help_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"help 명령어 처리 중 오류: {e}")
            await update.message.reply_text("❌ 명령어 처리 중 오류가 발생했습니다.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """메시지 처리 함수"""
        try:
            message = update.message
            if not message:
                return
            
            # 그룹 채팅에서만 동작
            if message.chat.id != self.group_chat_id:
                return
            
            # 메인 채널(토픽이 없는 메시지)에서만 감지
            if message.message_thread_id is not None:
                return
            
            # 봇 메시지인지 확인
            if not message.from_user or not message.from_user.is_bot:
                return
            
            # 매핑된 봇인지 확인하고 타겟 토픽 찾기
            target_topic_id = self.get_target_topic_for_bot(message.from_user)
            
            if target_topic_id is None:
                if self.settings.get('log_unknown_bots', True):
                    logger.info(f"매핑되지 않은 봇 메시지: @{message.from_user.username or 'N/A'} ({message.from_user.first_name})")
                return
            
            logger.info(f"봇 메시지 감지: @{message.from_user.username or 'N/A'} -> 토픽 {target_topic_id}")
            logger.info(f"메시지 내용: {message.text[:50] if message.text else 'Media message'}")
            
            # 메시지를 해당 토픽으로 포워딩
            await self.forward_to_topic(message, context, target_topic_id)
            
        except Exception as e:
            logger.error(f"메시지 처리 중 오류 발생: {e}")
    
    def get_target_topic_for_bot(self, bot_user):
        """봇 사용자에 대한 타겟 토픽 ID를 찾기"""
        # 사용자명으로 매핑 확인
        if bot_user.username:
            username = bot_user.username.lower()
            if username in self.bot_mappings:
                return self.bot_mappings[username]['topic_id']
        
        # 이름으로 매핑 확인 (부분 일치)
        bot_name = bot_user.first_name.lower()
        for mapped_username, config in self.bot_mappings.items():
            if mapped_username in bot_name or bot_name in mapped_username:
                return config['topic_id']
        
        # 알 수 없는 봇에 대한 기본 처리
        if self.settings.get('forward_all_unknown_bots', False):
            return self.settings.get('default_topic_id')
        
        return None
    
    async def forward_to_topic(self, message, context, target_topic_id):
        """메시지를 특정 토픽으로 포워딩"""
        try:
            # 텍스트 메시지인 경우
            if message.text:
                await context.bot.send_message(
                    chat_id=self.group_chat_id,
                    text=message.text,
                    message_thread_id=target_topic_id,
                    parse_mode=message.parse_entities() and 'HTML' or None
                )
            
            # 사진 메시지인 경우
            elif message.photo:
                await context.bot.send_photo(
                    chat_id=self.group_chat_id,
                    photo=message.photo[-1].file_id,
                    caption=message.caption,
                    message_thread_id=target_topic_id
                )
            
            # 문서 메시지인 경우
            elif message.document:
                await context.bot.send_document(
                    chat_id=self.group_chat_id,
                    document=message.document.file_id,
                    caption=message.caption,
                    message_thread_id=target_topic_id
                )
            
            # 비디오 메시지인 경우
            elif message.video:
                await context.bot.send_video(
                    chat_id=self.group_chat_id,
                    video=message.video.file_id,
                    caption=message.caption,
                    message_thread_id=target_topic_id
                )
            
            # 음성 메시지인 경우
            elif message.voice:
                await context.bot.send_voice(
                    chat_id=self.group_chat_id,
                    voice=message.voice.file_id,
                    caption=message.caption,
                    message_thread_id=target_topic_id
                )
            
            # 스티커 메시지인 경우
            elif message.sticker:
                await context.bot.send_sticker(
                    chat_id=self.group_chat_id,
                    sticker=message.sticker.file_id,
                    message_thread_id=target_topic_id
                )
            
            # 기타 메시지 타입의 경우 포워딩 사용
            else:
                await context.bot.forward_message(
                    chat_id=self.group_chat_id,
                    from_chat_id=message.chat.id,
                    message_id=message.message_id,
                    message_thread_id=target_topic_id
                )
            
            logger.info(f"메시지를 토픽 {target_topic_id}로 포워딩 완료")
            
        except Exception as e:
            logger.error(f"메시지 포워딩 중 오류 발생: {e}")
    
    def run(self):
        """봇 실행"""
        logger.info("텔레그램 포워더 봇을 시작합니다...")
        logger.info(f"그룹 ID: {self.group_chat_id}")
        logger.info(f"설정된 봇 매핑: {len(self.bot_mappings)}개")
        
        if not self.bot_mappings:
            logger.warning("설정된 봇 매핑이 없습니다. /set 명령어로 매핑을 추가하세요.")
        
        logger.info("사용 가능한 명령어: /set, /list, /remove, /help")
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    try:
        bot = TelegramForwarderBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("봇이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        logger.error(f"봇 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main() 