import json
import os
from typing import Dict, List, Optional

class BotMappingManager:
    def __init__(self, config_file: str = 'bot_mapping.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """설정 파일 로드"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"❌ {self.config_file} 파일이 손상되었습니다. 새로 생성합니다.")
        
        # 기본 설정 생성
        return {
            "bot_mappings": [],
            "settings": {
                "forward_all_unknown_bots": False,
                "default_topic_id": None,
                "log_unknown_bots": True
            }
        }
    
    def save_config(self):
        """설정 파일 저장"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        print(f"✅ 설정이 {self.config_file}에 저장되었습니다.")
    
    def add_bot_mapping(self, bot_username: str, topic_id: int, description: str = ""):
        """봇 매핑 추가"""
        bot_username = bot_username.replace('@', '')
        
        # 기존 매핑 확인
        for mapping in self.config['bot_mappings']:
            if mapping['source_bot_username'] == bot_username:
                print(f"⚠️  @{bot_username}은 이미 토픽 {mapping['target_topic_id']}에 매핑되어 있습니다.")
                return False
        
        # 새 매핑 추가
        new_mapping = {
            "source_bot_username": bot_username,
            "target_topic_id": topic_id,
            "description": description or f"@{bot_username}의 메시지를 토픽 {topic_id}로 포워딩"
        }
        
        self.config['bot_mappings'].append(new_mapping)
        print(f"✅ @{bot_username} -> 토픽 {topic_id} 매핑이 추가되었습니다.")
        return True
    
    def remove_bot_mapping(self, bot_username: str) -> bool:
        """봇 매핑 제거"""
        bot_username = bot_username.replace('@', '')
        
        for i, mapping in enumerate(self.config['bot_mappings']):
            if mapping['source_bot_username'] == bot_username:
                removed = self.config['bot_mappings'].pop(i)
                print(f"✅ @{bot_username} 매핑이 제거되었습니다. (토픽 {removed['target_topic_id']})")
                return True
        
        print(f"❌ @{bot_username}에 대한 매핑을 찾을 수 없습니다.")
        return False
    
    def update_bot_mapping(self, bot_username: str, topic_id: int, description: str = None) -> bool:
        """봇 매핑 업데이트"""
        bot_username = bot_username.replace('@', '')
        
        for mapping in self.config['bot_mappings']:
            if mapping['source_bot_username'] == bot_username:
                old_topic = mapping['target_topic_id']
                mapping['target_topic_id'] = topic_id
                if description is not None:
                    mapping['description'] = description
                print(f"✅ @{bot_username} 매핑이 업데이트되었습니다. (토픽 {old_topic} -> {topic_id})")
                return True
        
        print(f"❌ @{bot_username}에 대한 매핑을 찾을 수 없습니다.")
        return False
    
    def list_mappings(self):
        """모든 봇 매핑 목록 출력"""
        if not self.config['bot_mappings']:
            print("📝 설정된 봇 매핑이 없습니다.")
            return
        
        print("📝 현재 봇 매핑 설정:")
        print("-" * 60)
        for i, mapping in enumerate(self.config['bot_mappings'], 1):
            print(f"{i}. @{mapping['source_bot_username']} -> 토픽 {mapping['target_topic_id']}")
            if mapping.get('description'):
                print(f"   설명: {mapping['description']}")
        print("-" * 60)
    
    def update_settings(self, **kwargs):
        """일반 설정 업데이트"""
        for key, value in kwargs.items():
            if key in self.config['settings']:
                old_value = self.config['settings'][key]
                self.config['settings'][key] = value
                print(f"✅ {key}: {old_value} -> {value}")
            else:
                print(f"❌ 알 수 없는 설정: {key}")
    
    def show_settings(self):
        """현재 설정 출력"""
        print("⚙️  현재 설정:")
        for key, value in self.config['settings'].items():
            print(f"  {key}: {value}")

def main():
    manager = BotMappingManager()
    
    while True:
        print("\n=== 텔레그램 봇 매핑 관리자 ===")
        print("1. 봇 매핑 목록 보기")
        print("2. 봇 매핑 추가")
        print("3. 봇 매핑 수정")
        print("4. 봇 매핑 삭제")
        print("5. 설정 보기/수정")
        print("6. 저장 및 종료")
        print("0. 저장하지 않고 종료")
        
        choice = input("\n선택하세요 (0-6): ").strip()
        
        if choice == '1':
            manager.list_mappings()
        
        elif choice == '2':
            bot_username = input("봇 사용자명 (@포함 가능): ").strip()
            if not bot_username:
                print("❌ 봇 사용자명을 입력해주세요.")
                continue
            
            try:
                topic_id = int(input("토픽 ID: ").strip())
            except ValueError:
                print("❌ 올바른 토픽 ID를 입력해주세요.")
                continue
            
            description = input("설명 (선택사항): ").strip()
            manager.add_bot_mapping(bot_username, topic_id, description)
        
        elif choice == '3':
            manager.list_mappings()
            if not manager.config['bot_mappings']:
                continue
            
            bot_username = input("수정할 봇 사용자명: ").strip()
            if not bot_username:
                continue
            
            try:
                topic_id = int(input("새 토픽 ID: ").strip())
            except ValueError:
                print("❌ 올바른 토픽 ID를 입력해주세요.")
                continue
            
            description = input("새 설명 (엔터로 건너뛰기): ").strip()
            manager.update_bot_mapping(bot_username, topic_id, description if description else None)
        
        elif choice == '4':
            manager.list_mappings()
            if not manager.config['bot_mappings']:
                continue
            
            bot_username = input("삭제할 봇 사용자명: ").strip()
            if bot_username:
                manager.remove_bot_mapping(bot_username)
        
        elif choice == '5':
            manager.show_settings()
            print("\n설정 수정 (엔터로 건너뛰기):")
            
            forward_all = input(f"알 수 없는 봇도 포워딩 (현재: {manager.config['settings']['forward_all_unknown_bots']}): ").strip().lower()
            if forward_all in ['true', 'false']:
                manager.config['settings']['forward_all_unknown_bots'] = forward_all == 'true'
            
            default_topic = input(f"기본 토픽 ID (현재: {manager.config['settings']['default_topic_id']}): ").strip()
            if default_topic:
                try:
                    manager.config['settings']['default_topic_id'] = int(default_topic) if default_topic != 'null' else None
                except ValueError:
                    print("❌ 올바른 토픽 ID를 입력해주세요.")
            
            log_unknown = input(f"알 수 없는 봇 로깅 (현재: {manager.config['settings']['log_unknown_bots']}): ").strip().lower()
            if log_unknown in ['true', 'false']:
                manager.config['settings']['log_unknown_bots'] = log_unknown == 'true'
        
        elif choice == '6':
            manager.save_config()
            print("👋 설정이 저장되었습니다. 프로그램을 종료합니다.")
            break
        
        elif choice == '0':
            print("👋 설정을 저장하지 않고 종료합니다.")
            break
        
        else:
            print("❌ 올바른 선택지를 입력해주세요.")

if __name__ == "__main__":
    main() 