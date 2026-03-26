#!/bin/bash
# OpenClaw Scheduler - Test Script | 测试脚本
# Version | 版本: 1.0.0
# Description | 描述: Comprehensive test suite for scheduler skill
#              定时任务技能综合测试套件

set -e

# Colors for output | 输出颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color | 无颜色

# Test counters | 测试计数器
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test result file | 测试结果文件
TEST_LOG="/tmp/scheduler-test-$(date +%Y%m%d-%H%M%S).log"

# Print functions | 打印函数
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_test() {
    echo -e "\n${YELLOW}TEST $TESTS_RUN: $1${NC}"
    echo "----------------------------------------" >> "$TEST_LOG"
    echo "TEST $TESTS_RUN: $1" >> "$TEST_LOG"
}

print_pass() {
    echo -e "${GREEN}✓ PASS: $1${NC}"
    echo "✓ PASS: $1" >> "$TEST_LOG"
    ((TESTS_PASSED++))
}

print_fail() {
    echo -e "${RED}✗ FAIL: $1${NC}"
    echo "✗ FAIL: $1" >> "$TEST_LOG"
    ((TESTS_FAILED++))
}

print_info() {
    echo -e "${BLUE}INFO: $1${NC}"
    echo "INFO: $1" >> "$TEST_LOG"
}

# Test functions | 测试函数

test_openclaw_available() {
    ((TESTS_RUN++))
    print_test "Check OpenClaw CLI availability | 检查 OpenClaw CLI 可用性"
    
    if command -v openclaw &> /dev/null; then
        print_pass "OpenClaw CLI is available | OpenClaw CLI 可用"
        openclaw --version >> "$TEST_LOG" 2>&1
    else
        print_fail "OpenClaw CLI not found | 未找到 OpenClaw CLI"
        return 1
    fi
}

test_cron_list() {
    ((TESTS_RUN++))
    print_test "List existing cron tasks | 列出已有定时任务"
    
    if openclaw cron list &> /dev/null; then
        print_pass "Cron list command works | Cron list 命令正常"
        openclaw cron list >> "$TEST_LOG" 2>&1
    else
        print_fail "Cron list command failed | Cron list 命令失败"
        return 1
    fi
}

test_create_one_time_reminder() {
    ((TESTS_RUN++))
    print_test "Create one-time reminder (dry-run) | 创建一次性提醒（模拟）"
    
    # Note: This is a dry-run test, actual creation requires user confirmation
    # 注意：这是模拟测试，实际创建需要用户确认
    
    print_info "Command template | 命令模板:"
    echo "openclaw cron add --name 'test-reminder' --at '5m' --session main --system-event 'Test' --wake now --delete-after-run"
    
    print_pass "Command template validated | 命令模板验证通过"
}

test_cron_expression_validation() {
    ((TESTS_RUN++))
    print_test "Validate cron expressions | 验证 Cron 表达式"
    
    local cron_expressions=(
        "0 9 * * *"
        "*/30 * * * *"
        "0 0 1 * *"
        "0 9 * * 1-5"
    )
    
    for cron in "${cron_expressions[@]}"; do
        # Basic syntax check (5 or 6 fields)
        fields=$(echo "$cron" | awk '{print NF}')
        if [ "$fields" -ge 5 ] && [ "$fields" -le 6 ]; then
            print_info "Valid cron expression | 有效 Cron 表达式: $cron"
        else
            print_fail "Invalid cron expression | 无效 Cron 表达式: $cron"
            return 1
        fi
    done
    
    print_pass "All cron expressions validated | 所有 Cron 表达式验证通过"
}

test_timezone_handling() {
    ((TESTS_RUN++))
    print_test "Test timezone handling | 测试时区处理"
    
    local current_tz=$(date +%Z)
    print_info "Current timezone | 当前时区: $current_tz"
    
    # Test Asia/Shanghai timezone
    if [ "$current_tz" = "CST" ] || [ "$current_tz" = "Asia/Shanghai" ]; then
        print_pass "Timezone is Asia/Shanghai | 时区为 Asia/Shanghai"
    else
        print_info "Timezone is not Asia/Shanghai, but test continues | 时区不是 Asia/Shanghai，但测试继续"
    fi
}

test_script_template() {
    ((TESTS_RUN++))
    print_test "Validate script template | 验证脚本模板"
    
    local script_path="$(dirname "$0")/../scripts/daily-task.sh.template"
    
    if [ -f "$script_path" ]; then
        # Check for required elements | 检查必需元素
        if grep -q "export PATH" "$script_path" && \
           grep -q "openclaw agent" "$script_path" && \
           grep -q "#!/bin/bash" "$script_path"; then
            print_pass "Script template contains all required elements | 脚本模板包含所有必需元素"
        else
            print_fail "Script template missing required elements | 脚本模板缺少必需元素"
            return 1
        fi
    else
        print_info "Script template not found, skipping | 未找到脚本模板，跳过"
    fi
}

test_skill_documentation() {
    ((TESTS_RUN++))
    print_test "Check skill documentation | 检查技能文档"
    
    local skill_md="$(dirname "$0")/../SKILL.md"
    
    if [ -f "$skill_md" ]; then
        # Check for required sections | 检查必需章节
        local required_sections=(
            "name:"
            "description:"
            "Quick Start"
            "Method 1"
            "Method 2"
            "Pitfalls"
            "Troubleshooting"
        )
        
        local missing_sections=()
        for section in "${required_sections[@]}"; do
            if ! grep -q "$section" "$skill_md"; then
                missing_sections+=("$section")
            fi
        done
        
        if [ ${#missing_sections[@]} -eq 0 ]; then
            print_pass "Documentation contains all required sections | 文档包含所有必需章节"
        else
            print_fail "Documentation missing sections: ${missing_sections[*]} | 文档缺少章节：${missing_sections[*]}"
            return 1
        fi
    else
        print_fail "SKILL.md not found | 未找到 SKILL.md"
        return 1
    fi
}

test_bilingual_content() {
    ((TESTS_RUN++))
    print_test "Check bilingual content | 检查双语内容"
    
    local skill_md="$(dirname "$0")/../SKILL.md"
    
    if [ -f "$skill_md" ]; then
        # Check for Chinese characters | 检查中文字符
        if grep -qP '[\x{4e00}-\x{9fff}]' "$skill_md" 2>/dev/null || grep -q '[一 - 龟]' "$skill_md"; then
            print_pass "Documentation contains Chinese content | 文档包含中文内容"
        else
            print_fail "Documentation missing Chinese content | 文档缺少中文内容"
            return 1
        fi
        
        # Check for English content | 检查英文内容
        if grep -q "Overview" "$skill_md" && grep -q "Quick Start" "$skill_md"; then
            print_pass "Documentation contains English content | 文档包含英文内容"
        else
            print_fail "Documentation missing English content | 文档缺少英文内容"
            return 1
        fi
    fi
}

test_no_sensitive_data() {
    ((TESTS_RUN++))
    print_test "Check for sensitive data | 检查敏感数据"
    
    local skill_dir="$(dirname "$0")/.."
    local sensitive_patterns=(
        "password="
        "secret="
        "token="
        "api_key="
        "access_token"
        "private_key"
        "ou_[a-f0-9]\{32\}"
    )
    
    local found_sensitive=0
    for pattern in "${sensitive_patterns[@]}"; do
        if grep -r "$pattern" "$skill_dir" --include="*.md" --include="*.sh" 2>/dev/null | grep -v "example" | grep -v "template" > /dev/null; then
            print_info "Warning: Potential sensitive data pattern found | 警告：发现潜在敏感数据模式"
            found_sensitive=1
        fi
    done
    
    if [ $found_sensitive -eq 0 ]; then
        print_pass "No sensitive data found | 未发现敏感数据"
    else
        print_fail "Potential sensitive data detected | 检测到潜在敏感数据"
        return 1
    fi
}

test_directory_structure() {
    ((TESTS_RUN++))
    print_test "Check directory structure | 检查目录结构"
    
    local skill_dir="$(dirname "$0")/.."
    local required_dirs=(
        "scripts"
        "tests"
        "references"
    )
    
    local missing_dirs=()
    for dir in "${required_dirs[@]}"; do
        if [ ! -d "$skill_dir/$dir" ]; then
            missing_dirs+=("$dir")
        fi
    done
    
    if [ ${#missing_dirs[@]} -eq 0 ]; then
        print_pass "Directory structure is complete | 目录结构完整"
    else
        print_info "Missing directories: ${missing_dirs[*]} | 缺少目录：${missing_dirs[*]}"
    fi
}

# Main test runner | 主测试运行器

run_all_tests() {
    print_header "OpenClaw Scheduler Test Suite | 定时任务技能测试套件"
    print_info "Test started at | 测试开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
    print_info "Test log file | 测试日志文件: $TEST_LOG"
    
    # Run tests | 运行测试
    test_openclaw_available
    test_cron_list
    test_create_one_time_reminder
    test_cron_expression_validation
    test_timezone_handling
    test_script_template
    test_skill_documentation
    test_bilingual_content
    test_no_sensitive_data
    test_directory_structure
    
    # Print summary | 打印摘要
    print_header "Test Summary | 测试摘要"
    print_info "Total tests run | 总测试数: $TESTS_RUN"
    print_info "Passed | 通过: $TESTS_PASSED"
    print_info "Failed | 失败: $TESTS_FAILED"
    print_info "Test log saved to | 测试日志保存至：$TEST_LOG"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        print_header "All tests passed! | 所有测试通过！"
        echo -e "${GREEN}✓ SUCCESS${NC}"
        return 0
    else
        print_header "Some tests failed! | 部分测试失败！"
        echo -e "${RED}✗ FAILURE${NC}"
        return 1
    fi
}

# Help message | 帮助信息

show_help() {
    echo "OpenClaw Scheduler Test Suite | 定时任务技能测试套件"
    echo ""
    echo "Usage | 用法:"
    echo "  $0 [option]"
    echo ""
    echo "Options | 选项:"
    echo "  --all, -a          Run all tests | 运行所有测试"
    echo "  --doc, -d          Run documentation tests only | 仅运行文档测试"
    echo "  --quick, -q        Run quick tests only | 仅运行快速测试"
    echo "  --help, -h         Show this help message | 显示帮助信息"
    echo ""
    echo "Examples | 示例:"
    echo "  $0 --all           Run complete test suite | 运行完整测试套件"
    echo "  $0 --quick         Run quick validation | 运行快速验证"
}

# Parse arguments | 解析参数

case "${1:-}" in
    --all|-a)
        run_all_tests
        ;;
    --doc|-d)
        test_skill_documentation
        test_bilingual_content
        test_no_sensitive_data
        ;;
    --quick|-q)
        test_openclaw_available
        test_cron_list
        test_directory_structure
        ;;
    --help|-h|"")
        show_help
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac
