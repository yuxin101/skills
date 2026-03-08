#!/bin/bash
# PRISM_GEN_DEMO 一键安装脚本

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 输出函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否以root运行
check_root() {
    if [ "$EUID" -eq 0 ]; then 
        print_warning "不建议以root用户运行安装脚本"
        read -p "是否继续? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# 检查系统要求
check_system() {
    print_info "检查系统要求..."
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python $python_version 已安装"
        
        # 检查Python版本
        required_version="3.10"
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)"; then
            print_success "Python版本满足要求 (>=3.10)"
        else
            print_error "Python版本过低 (需要>=3.10，当前$python_version)"
            exit 1
        fi
    else
        print_error "Python3未安装"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 已安装"
    else
        print_warning "pip3 未安装，尝试安装..."
        if python3 -m ensurepip --user; then
            print_success "pip3 安装成功"
        else
            print_error "无法安装pip3，请手动安装"
            exit 1
        fi
    fi
    
    # 检查conda（可选）
    if command -v conda &> /dev/null; then
        conda_version=$(conda --version 2>&1)
        print_success "Conda $conda_version 已安装"
    else
        print_warning "Conda 未安装，将使用pip安装包"
    fi
}

# 安装Python包
install_python_packages() {
    print_info "安装Python依赖包..."
    
    # 检查requirements.txt
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt 文件不存在"
        exit 1
    fi
    
    # 安装包
    if command -v conda &> /dev/null; then
        print_info "使用Conda安装..."
        if conda install --yes --file requirements.txt; then
            print_success "Conda安装成功"
        else
            print_warning "Conda安装失败，尝试使用pip..."
            pip3 install -r requirements.txt --user
        fi
    else
        print_info "使用pip安装..."
        pip3 install -r requirements.txt --user
    fi
    
    # 验证安装
    print_info "验证包安装..."
    required_packages=("pandas" "numpy" "matplotlib" "seaborn")
    missing_packages=()
    
    for pkg in "${required_packages[@]}"; do
        if python3 -c "import $pkg" 2>/dev/null; then
            version=$(python3 -c "import $pkg; print($pkg.__version__)" 2>/dev/null || echo "未知")
            print_success "$pkg $version 已安装"
        else
            print_error "$pkg 未安装"
            missing_packages+=("$pkg")
        fi
    done
    
    if [ ${#missing_packages[@]} -gt 0 ]; then
        print_error "以下包安装失败: ${missing_packages[*]}"
        print_info "尝试手动安装: pip3 install ${missing_packages[*]} --user"
        exit 1
    fi
}

# 设置脚本权限
setup_permissions() {
    print_info "设置脚本执行权限..."
    
    # 给所有.sh文件添加执行权限
    if [ -d "scripts" ]; then
        chmod +x scripts/*.sh 2>/dev/null || true
        print_success "脚本权限设置完成"
    else
        print_error "scripts目录不存在"
        exit 1
    fi
    
    # 给.py文件添加执行权限
    chmod +x scripts/*.py 2>/dev/null || true
}

# 创建必要目录
create_directories() {
    print_info "创建必要目录..."
    
    directories=("output/filtered" "output/top" "plots" "logs")
    
    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_success "创建目录: $dir"
        else
            print_info "目录已存在: $dir"
        fi
    done
}

# 测试安装
test_installation() {
    print_info "测试安装..."
    
    # 测试Python环境
    if python3 -c "import pandas; print('✅ Pandas测试通过')"; then
        print_success "Python环境测试通过"
    else
        print_error "Python环境测试失败"
        exit 1
    fi
    
    # 测试脚本
    if [ -f "scripts/demo_list_sources.sh" ]; then
        if bash scripts/demo_list_sources.sh 2>&1 | grep -q "可用数据源"; then
            print_success "核心脚本测试通过"
        else
            print_warning "核心脚本测试警告（可能无数据文件）"
        fi
    fi
    
    # 测试数据目录
    if [ -d "data" ]; then
        csv_count=$(find data -name "*.csv" -type f 2>/dev/null | wc -l)
        if [ "$csv_count" -gt 0 ]; then
            print_success "数据目录包含 $csv_count 个CSV文件"
        else
            print_warning "数据目录为空，请添加CSV文件"
        fi
    else
        print_warning "数据目录不存在，请创建并添加CSV文件"
    fi
}

# 显示安装完成信息
show_completion() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}      PRISM_GEN_DEMO 安装完成！      ${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "📦 安装位置: $(pwd)"
    echo "🐍 Python环境: $(which python3)"
    echo "📊 核心包: pandas, numpy, matplotlib, seaborn"
    echo ""
    echo "🚀 快速开始:"
    echo "  1. 将PRISM CSV文件放入 data/ 目录"
    echo "  2. 运行测试: bash scripts/test_visualization.sh"
    echo "  3. 查看数据: bash scripts/demo_list_sources.sh"
    echo ""
    echo "📚 文档:"
    echo "  - README.md: 完整项目文档"
    echo "  - SKILL.md: OpenClaw技能定义"
    echo ""
    echo "🔧 故障排除:"
    echo "  如果遇到问题，请检查:"
    echo "  1. Python包是否安装成功"
    echo "  2. 脚本是否有执行权限"
    echo "  3. 数据文件格式是否正确"
    echo ""
    echo "💡 提示: 建议将本项目添加到OpenClaw技能目录:"
    echo "  ln -s $(pwd) ~/projects/openclaw/skills/prism-gen-demo"
    echo ""
    echo -e "${GREEN}========================================${NC}"
}

# 主函数
main() {
    echo -e "${BLUE}"
    echo "   ____  ____  ___  ____  __  __   ____  _____ "
    echo "  |  _ \|  _ \/ _ \/ ___||  \/  | / ___|| ____|"
    echo "  | |_) | | | | | |\___ \| |\/| | \___ \|  _|  "
    echo "  |  __/| |_| | |_| |___) | |  | |  ___) | |___ "
    echo "  |_|   |____/ \___/|____/|_|  |_| |____/|_____|"
    echo "            GEN_DEMO 安装程序"
    echo -e "${NC}"
    echo ""
    
    # 执行安装步骤
    check_root
    check_system
    install_python_packages
    setup_permissions
    create_directories
    test_installation
    show_completion
}

# 运行主函数
main "$@"