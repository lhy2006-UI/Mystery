#!/bin/bash
# 神秘复苏 - 本地APK打包脚本
# 在Ubuntu/Debian Linux上运行

set -e

echo "=========================================="
echo "  神秘复苏 - Android APK 本地打包工具"
echo "=========================================="

# 1. 安装系统依赖
echo "[1/5] 安装系统依赖..."
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    build-essential python3-venv

# 2. 创建虚拟环境
echo "[2/5] 创建Python虚拟环境..."
python3 -m venv buildenv
source buildenv/bin/activate

# 3. 安装Python依赖
echo "[3/5] 安装打包工具..."
pip install --upgrade pip setuptools wheel
pip install buildozer "cython<3.0" appdirs colorama jinja2 "sh<3.0" \
    meson ninja build toml packaging

# 4. 修复buildozer的--user参数问题（虚拟环境下不需要）
echo "[4/5] 配置打包环境..."
PYTHON_SITE=$(python -c "import site; print(site.getsitepackages()[0])")
sed -i 's/options = \["--user"\]/options = []/g' \
    "$PYTHON_SITE/buildozer/targets/android.py"

# 5. 开始打包
echo "[5/5] 开始打包APK（首次需要下载SDK/NDK，约20-30分钟）..."
buildozer android debug

echo ""
echo "=========================================="
echo "  打包完成！"
echo "  APK文件位置: bin/*.apk"
echo "=========================================="
