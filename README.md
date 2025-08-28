# 复旦大学数学科学学院成绩计算工具

## 📦 下载安装

前往 [Releases 页面](https://github.com/LvDAO/Fudan-Math-Grade-Computing/releases) 下载对应您系统的版本：

#### 🪟 Windows 用户

- 下载：`main-windows-x64.exe`
- 使用：在命令行中执行

#### 🍎 macOS 用户

**Intel Mac (x64)**

- 下载：`main-macos-x64.zip`
- 使用：解压后使用终端app运行

**Apple Silicon Mac (ARM64)**

- 下载：`main-macos-arm64.zip`
- 使用：解压后使用终端app运行

> **注意**：首次运行时可能需要在"系统偏好设置 > 安全性与隐私"中允许运行此应用。

#### 🐧 Linux 用户

- 下载：`main-linux-x64`
- 使用：添加执行权限后运行

```bash
chmod +x main-linux-x64
./main-linux-x64 --help
```

## 🚀 使用方法

### 命令行参数

```bash
main --c 课程列表文件 --g 成绩文件 -y 计算学年 -o 输出文件
```

#### 必需参数

- `--grades` / `-g`：成绩数据 CSV 文件路径

#### 可选参数

- `--course_list` / `-c`：课程列表 CSV 文件路径，不提供具体课程列表时使用默认内置的课程列表

- `--output` / `-o`：输出文件路径（默认：`output.csv`）

- `--year` / `-y`：要计算的学年，默认是计算所有学年的 GPA
### 使用示例

#### Windows

```cmd
# 在命令提示符中运行
main-windows-x64.exe -c CourseList.csv -g Grades.csv -o result.csv -y 2024-2025
```

#### macOS

```bash
# 在终端中运行（假设已解压到当前目录）
./main.app/Contents/MacOS/main -c CourseList.csv -g Grades.csv -o result.csv -y 2024-2025
```

#### Linux

```bash
# 在终端中运行
./main-linux-x64 -c CourseList.csv -g Grades.csv -o result.csv -y 2024-2025
```

## 📄 输入文件格式

### 课程列表文件 (CourseList.csv)

包含需要计算专业绩点的课程代码：

```csv
课程代码
MATH130001
MATH130002
COMP130001
...
```

### 成绩文件 (Grades.csv)

包含学生的详细成绩信息：

```csv
学号,姓名,课程序号,课程名称,学分,最终成绩,绩点
22300001,张三,MATH130001.01,数学分析,6,95,4.0
22300001,张三,COMP130001.01,程序设计,3,88,3.3
...
```

**重要字段说明：**

- `课程序号`：完整的课程序号（如 `MATH130001.01`）
- `最终成绩`：A/B+/B...或 P/NP/F/缓考
- `绩点`：对应的绩点值

## 📊 输出结果

程序会生成包含以下字段的 CSV 文件：

| 字段     | 说明                         |
| -------- | ---------------------------- |
| 学号     | 学生学号                     |
| 姓名     | 学生姓名                     |
| 专业绩点 | 基于课程列表计算的专业课绩点 |
| 总绩点   | 所有课程的总绩点             |
| 总学分   | 获得的总学分数               |

结果按总绩点降序排列。
