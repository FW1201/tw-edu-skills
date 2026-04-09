#!/usr/bin/env bash
# 臺灣 K-12 教育 Claude Code Skills v3.0 安裝腳本
set -e
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

echo -e "\n${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   臺灣 K-12 + 學術研究 Claude Code Skills v3.0      ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}\n"
mkdir -p "$SKILLS_DIR"

ALL_SKILLS=(
  tw-edu-lesson-plan-108 tw-edu-curriculum-mapper
  tw-edu-differentiated tw-edu-interdisciplinary
  tw-edu-exam-generator tw-edu-rubric-designer tw-edu-formative-assessment
  tw-edu-worksheet-creator tw-edu-slides-creator
  tw-edu-feedback-writer tw-edu-learning-portfolio
  tw-edu-parent-communication tw-edu-classroom-culture
  tw-edu-school-document tw-edu-meeting-facilitator
  tw-edu-pbl-designer tw-edu-mini-app
  tw-edu-research-viz tw-edu-citation-checker
  tw-edu-anti-ai-assessment
)

INSTALL_LIST=("${ALL_SKILLS[@]}")
[ -n "$1" ] && INSTALL_LIST=("$1") && echo -e "${YELLOW}→ 安裝單一 Skill：$1${NC}" || echo -e "${YELLOW}→ 安裝全部 19 種 Skills${NC}"

COUNT=0
for skill in "${INSTALL_LIST[@]}"; do
  SRC="$REPO_DIR/$skill"; DST="$SKILLS_DIR/$skill"
  [ ! -d "$SRC" ] && echo -e "  ⚠️  找不到 $skill" && continue
  rm -rf "$DST"; cp -r "$SRC" "$DST"
  COUNT=$((COUNT+1)); echo -e "  ${GREEN}✓${NC} $skill"
done

# 複製共用工具
for f in tw_edu_doc_utils.py tw_edu_grade_adapter.md tw_edu_guided_collection.md tw_edu_mcp_strategy.md; do
  cp "$REPO_DIR/$f" "$SKILLS_DIR/" 2>/dev/null && echo -e "  ${GREEN}✓${NC} 共用：$f"
done

echo -e "\n${GREEN}══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ 安裝完成！共安裝 $COUNT 種 Skills（含 1 個學術研究 + 1 個抗AI評量）${NC}"
echo -e "${GREEN}  路徑：$SKILLS_DIR${NC}"
echo -e "${GREEN}\n  ✨ v3.0 新功能：${NC}"
echo -e "${BLUE}  • 學術資料視覺化（Excalidraw MCP）${NC}"
echo -e "${BLUE}  • 學術文獻嚴格查核（Consensus MCP）${NC}"
echo -e "${BLUE}  • 會議全流程（Calendar + Drive + Gmail）${NC}"
echo -e "${BLUE}  • 全 19 skills MCP 最佳化${NC}"
echo -e "${GREEN}══════════════════════════════════════════════════${NC}\n"
[ -x "$(command -v pip)" ] && pip install -r "$REPO_DIR/requirements.txt" -q && echo -e "${GREEN}✓ Python 套件安裝完成${NC}"
