import os
import json
import argparse
from pathlib import Path
from datetime import datetime

class ARCArchiver:
    def __init__(self):
        # 路径探测逻辑：锁定 arc-reactor 技能根目录
        # 假设脚本位于 skills/arc-reactor/components/archive-manager.py
        self.skill_root = Path(__file__).resolve().parent.parent
        self.doc_root = self.skill_root.parent.parent / "arc-reactor-doc"
        
        # 定义子目录
        self.reports_dir = self.doc_root / "reports" / datetime.now().strftime("%Y-%m-%d")
        self.sources_dir = self.doc_root / "sources" / datetime.now().strftime("%Y-%m-%d")
        self.entities_dir = self.doc_root / "knowledge" / "entities"
        self.conflicts_dir = self.doc_root / "knowledge" / "conflicts"
        self.temp_dir = self.skill_root / "components" / "media" / "extractor_temp"

    def setup_dirs(self):
        """确保所有归档目录存在"""
        for d in [self.reports_dir, self.sources_dir, self.entities_dir, self.conflicts_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def archive_report(self, data):
        """处理调研报告归档"""
        title = data.get("title", "untitled_research").replace(" ", "_")
        report_content = data.get("report_content", "")
        formatted_transcript = data.get("formatted_transcript", "")
        
        # 1. 保存主报告
        report_path = self.reports_dir / f"{title}-调研报告.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        # 2. 保存洗稿后的文稿 (作为素材)
        if formatted_transcript:
            raw_path = self.sources_dir / f"{title}-文稿素材.md"
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(formatted_transcript)
        
        return report_path

    def update_knowledge(self, entities):
        """更新实体百科 Wiki"""
        for entity in entities:
            name = entity.get("name", "Unknown").replace(" ", "_")
            content = entity.get("content", "")
            file_path = self.entities_dir / f"{name}.md"
            
            # Smart Merge 逻辑：如果存在则追加或更新
            if file_path.exists():
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n--- [Update: {datetime.now().strftime('%Y-%m-%d')}] ---\n")
                    f.write(content)
            else:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"# {name}\n\n{content}")

    def cleanup(self):
        """物理清除临时垃圾"""
        if self.temp_dir.exists():
            for item in self.temp_dir.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        import shutil
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"Cleanup error for {item}: {e}")

    def run(self, payload_path):
        with open(payload_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        self.setup_dirs()
        
        # 执行归档
        report_path = self.archive_report(data)
        
        # 更新知识库
        if data.get("entities"):
            self.update_knowledge(data["entities"])
            
        # 清理垃圾
        self.cleanup()
        
        print(f"✅ ARC Archiving Complete.")
        print(f"📍 Report: {report_path}")
        print(f"📍 Doc Root: {self.doc_root}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARC Reactor Programmatic Archiver")
    parser.add_argument("--payload", required=True, help="Path to JSON payload file")
    args = parser.parse_args()
    
    archiver = ARCArchiver()
    archiver.run(args.payload)
