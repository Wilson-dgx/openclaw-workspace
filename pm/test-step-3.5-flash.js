#!/usr/bin/env node
/**
 * step-3.5-flash 综合能力测试
 * 测试维度：编程能力、复杂问题解决、Token性能
 */

const http = require('http');
const { performance } = require('perf_hooks');

const API_BASE = 'http://localhost:1234/v1';
const MODEL = 'step-3.5-flash';

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  magenta: '\x1b[35m'
};

function log(msg, color = 'reset') {
  console.log(`${colors[color]}${msg}${colors.reset}`);
}

// 调用LMstudio API
async function callAPI(prompt, maxTokens = 2048, temperature = 0.7) {
  return new Promise((resolve, reject) => {
    const startTime = performance.now();
    
    const requestData = JSON.stringify({
      model: MODEL,
      messages: [{ role: 'user', content: prompt }],
      max_tokens: maxTokens,
      temperature: temperature,
      stream: false
    });

    const options = {
      hostname: 'localhost',
      port: 1234,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(requestData)
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const endTime = performance.now();
          const response = JSON.parse(data);
          
          if (response.error) {
            reject(new Error(response.error.message));
            return;
          }

          const content = response.choices[0].message.content;
          const usage = response.usage || {};
          
          resolve({
            content,
            promptTokens: usage.prompt_tokens || 0,
            completionTokens: usage.completion_tokens || 0,
            totalTokens: usage.total_tokens || 0,
            responseTime: endTime - startTime,
            tokensPerSecond: usage.completion_tokens ? 
              (usage.completion_tokens / ((endTime - startTime) / 1000)).toFixed(2) : 0
          });
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(requestData);
    req.end();
  });
}

// 测试用例定义
const testCases = {
  // 编程能力测试
  programming: [
    {
      name: '基础算法 - 快速排序',
      difficulty: '★☆☆☆☆',
      prompt: `请用Python实现快速排序算法，要求：
1. 使用列表推导式
2. 包含详细注释
3. 提供时间复杂度分析
4. 给出一个使用示例

只输出代码和必要说明，不要多余的话。`
    },
    {
      name: '数据结构 - LRU缓存',
      difficulty: '★★★☆☆',
      prompt: `实现一个LRU（最近最少使用）缓存机制，要求：
1. 使用Python的OrderedDict
2. 支持get和put操作
3. 容量满时自动删除最久未使用的数据
4. 时间复杂度O(1)
5. 提供完整测试用例

只输出代码和测试，不要多余解释。`
    },
    {
      name: 'Bug修复 - 并发问题',
      difficulty: '★★★★☆',
      prompt: `下面这段Python多线程代码存在严重的并发bug，请找出所有问题并修复：

\`\`\`python
import threading

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def deposit(self, amount):
        current = self.balance
        # 模拟处理延迟
        import time; time.sleep(0.001)
        self.balance = current + amount
    
    def withdraw(self, amount):
        if self.balance >= amount:
            current = self.balance
            import time; time.sleep(0.001)
            self.balance = current - amount
            return True
        return False
    
    def transfer(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)

# 测试
account1 = BankAccount(1000)
account2 = BankAccount(1000)

threads = []
for _ in range(100):
    t1 = threading.Thread(target=account1.transfer, args=(account2, 10))
    t2 = threading.Thread(target=account2.transfer, args=(account1, 10))
    threads.extend([t1, t2])

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"账户1: {account1.balance}, 账户2: {account2.balance}")
print(f"总余额: {account1.balance + account2.balance}")  # 应该是2000
\`\`\`

请：
1. 指出所有并发bug
2. 提供修复后的完整代码
3. 解释修复原理`
    },
    {
      name: '系统设计 - 短链接服务',
      difficulty: '★★★★★',
      prompt: `设计一个类似bit.ly的短链接服务，需要考虑：

需求：
- 每天1000万次访问，10万次创建
- 短链接长度不超过7个字符
- 支持自定义短链接
- 需要统计点击数据（时间、来源、地域）
- 防止恶意使用

请设计：
1. 系统架构（画简图）
2. 数据库表结构
3. 短链接生成算法（避免冲突）
4. 缓存策略
5. 高可用保障
6. 核心API设计

用markdown格式输出设计文档。`
    }
  ],
  
  // 复杂问题解决测试
  complexProblems: [
    {
      name: '逻辑推理 - 三门问题',
      difficulty: '★★★☆☆',
      prompt: `经典的三门问题（Monty Hall problem）：

假设你参加一个游戏节目，有三扇门。其中一扇门后是汽车，另外两扇门后是山羊。
你选择了一扇门（比如1号门）。主持人知道每扇门后是什么，他打开了另一扇门（比如3号门），后面是山羊。
现在主持人问你：要不要换选2号门？

问题：
1. 应该换还是不换？为什么？
2. 用贝叶斯定理证明你的结论
3. 如果有100扇门，主持人打开98扇山羊门，换门的概率是多少？
4. 用Python模拟10000次验证结果

请给出详细的数学推导和验证代码。`
    },
    {
      name: '数学问题 - 水壶问题',
      difficulty: '★★★★☆',
      prompt: `经典的量水问题：

你有一个3升的壶和一个5升的壶，还有无限的水。
问题：如何准确地量出4升水？

要求：
1. 给出详细的操作步骤
2. 用BFS算法证明这是最少的步骤数
3. 扩展：如何量出1升、2升、6升、7升？
4. 编写通用算法：给定两个壶的容量和目标水量，判断是否可以量出，如果能，给出最少步骤

请提供算法思路、代码实现和测试用例。`
    },
    {
      name: '场景分析 - 性能优化',
      difficulty: '★★★★★',
      prompt: `实际场景：数据库查询性能问题

问题现象：
一个电商平台的订单查询页面，最近响应时间从200ms飙升到5-10秒。
数据库CPU使用率从30%涨到90%。

现有架构：
- MySQL 5.7，单主从复制
- orders表：2000万行数据
- 查询SQL：SELECT * FROM orders WHERE user_id = ? AND status IN (...) ORDER BY created_at DESC LIMIT 20

已知信息：
- user_id有索引
- status和created_at没有组合索引
- 最近做了营销活动，订单量增长了3倍
- 大部分查询只查最近3个月的数据

请分析：
1. 可能的性能瓶颈是什么？（至少3个）
2. 如何验证你的猜测？（具体操作命令）
3. 短期解决方案（今天能上线）
4. 中长期优化方案
5. 如何监控防止再次发生？

输出详细的诊断和优化方案。`
    }
  ],
  
  // 综合能力测试
  comprehensive: [
    {
      name: '综合实战 - 日志分析系统',
      difficulty: '★★★★★',
      prompt: `设计并实现一个实时日志分析系统：

需求：
1. 每秒接收10万条日志（格式：timestamp, level, service, message）
2. 实时统计：
   - 各服务错误率（5分钟窗口）
   - 异常流量模式检测
   - 关键错误告警
3. 支持10个并发查询（最近1小时的日志）
4. 数据保留7天

技术约束：
- 单机部署（16核CPU，64GB内存）
- 使用Python或Go
- 可使用Redis、ClickHouse等开源组件

请提供：
1. 架构设计（组件和流程）
2. 数据结构设计（内存+持久化）
3. 核心代码实现（至少500行）
4. 性能优化技巧
5. 压测结果预估

注意：这是实际工程问题，需要考虑边界情况、容错、性能。`
    }
  ]
};

// 评分标准
const rubric = {
  programming: {
    correctness: { weight: 0.4, criteria: '代码正确性、能否运行' },
    efficiency: { weight: 0.25, criteria: '算法复杂度、优化程度' },
    readability: { weight: 0.2, criteria: '代码风格、注释质量' },
    completeness: { weight: 0.15, criteria: '是否满足所有要求' }
  },
  complexProblems: {
    correctness: { weight: 0.35, criteria: '答案正确性' },
    reasoning: { weight: 0.3, criteria: '推理过程清晰度' },
    methodology: { weight: 0.2, criteria: '方法论的合理性' },
    verification: { weight: 0.15, criteria: '验证方法的严谨性' }
  },
  comprehensive: {
    design: { weight: 0.3, criteria: '架构设计合理性' },
    implementation: { weight: 0.3, criteria: '代码实现质量' },
    performance: { weight: 0.25, criteria: '性能考量是否充分' },
    robustness: { weight: 0.15, criteria: '边界情况和容错' }
  }
};

// 测试单个用例
async function runTest(category, testCase, index) {
  log(`\n${'='.repeat(60)}`, 'cyan');
  log(`测试 [${index + 1}] ${testCase.name}`, 'bright');
  log(`难度: ${testCase.difficulty}`, 'yellow');
  log(`${'='.repeat(60)}`, 'cyan');
  
  try {
    const result = await callAPI(testCase.prompt);
    
    log(`\n✓ 响应时间: ${result.responseTime.toFixed(0)}ms`, 'green');
    log(`✓ Token统计: 输入=${result.promptTokens}, 输出=${result.completionTokens}, 总计=${result.totalTokens}`, 'green');
    log(`✓ 生成速度: ${result.tokensPerSecond} tokens/s`, 'magenta');
    
    log(`\n${'─'.repeat(60)}`, 'blue');
    log('响应内容:', 'blue');
    log(`${'─'.repeat(60)}`, 'blue');
    console.log(result.content);
    
    return {
      name: testCase.name,
      difficulty: testCase.difficulty,
      success: true,
      metrics: result
    };
  } catch (error) {
    log(`\n✗ 测试失败: ${error.message}`, 'red');
    return {
      name: testCase.name,
      success: false,
      error: error.message
    };
  }
}

// 生成测试报告
function generateReport(results) {
  log(`\n\n${'█'.repeat(60)}`, 'green');
  log('📊 测试报告', 'bright');
  log(`${'█'.repeat(60)}`, 'green');
  
  // 按类别统计
  const categories = {
    programming: { name: '编程能力', tests: [], color: 'cyan' },
    complexProblems: { name: '复杂问题解决', tests: [], color: 'yellow' },
    comprehensive: { name: '综合实战', tests: [], color: 'magenta' }
  };
  
  results.forEach(r => {
    if (categories[r.category]) {
      categories[r.category].tests.push(r);
    }
  });
  
  // 输出各类别统计
  Object.entries(categories).forEach(([key, cat]) => {
    if (cat.tests.length === 0) return;
    
    log(`\n【${cat.name}】`, cat.color);
    log('─'.repeat(50), cat.color);
    
    const successTests = cat.tests.filter(t => t.success);
    const totalTokens = successTests.reduce((sum, t) => sum + (t.metrics?.totalTokens || 0), 0);
    const avgSpeed = successTests.length > 0 ?
      (successTests.reduce((sum, t) => sum + parseFloat(t.metrics?.tokensPerSecond || 0), 0) / successTests.length).toFixed(2) :
      0;
    
    log(`  成功率: ${successTests.length}/${cat.tests.length}`, 'reset');
    log(`  平均速度: ${avgSpeed} tokens/s`, 'reset');
    log(`  总Token: ${totalTokens}`, 'reset');
    
    cat.tests.forEach(t => {
      const status = t.success ? '✓' : '✗';
      const info = t.success ? 
        `(${t.metrics.tokensPerSecond} tok/s, ${t.metrics.completionTokens} tok)` :
        `(${t.error})`;
      log(`    ${status} ${t.name} ${info}`, 'reset');
    });
  });
  
  // 总体统计
  const allSuccess = results.filter(r => r.success);
  const overallStats = {
    totalTests: results.length,
    successCount: allSuccess.length,
    avgSpeed: allSuccess.length > 0 ?
      (allSuccess.reduce((sum, t) => sum + parseFloat(t.metrics.tokensPerSecond || 0), 0) / allSuccess.length).toFixed(2) : 0,
    maxSpeed: Math.max(...allSuccess.map(t => parseFloat(t.metrics.tokensPerSecond || 0))).toFixed(2),
    minSpeed: Math.min(...allSuccess.map(t => parseFloat(t.metrics.tokensPerSecond || 0))).toFixed(2),
    totalTokens: allSuccess.reduce((sum, t) => sum + (t.metrics?.totalTokens || 0), 0)
  };
  
  log(`\n${'█'.repeat(60)}`, 'green');
  log('📈 总体性能', 'bright');
  log(`${'█'.repeat(60)}`, 'green');
  log(`  测试成功率: ${overallStats.successCount}/${overallStats.totalTests}`, 'reset');
  log(`  平均速度: ${overallStats.avgSpeed} tokens/s`, 'reset');
  log(`  速度范围: ${overallStats.minSpeed} - ${overallStats.maxSpeed} tokens/s`, 'reset');
  log(`  总Token消耗: ${overallStats.totalTokens}`, 'reset');
  
  return overallStats;
}

// 主测试流程
async function main() {
  log('\n🚀 step-3.5-flash 综合能力测试', 'bright');
  log('═'.repeat(60), 'bright');
  log(`模型: ${MODEL}`, 'cyan');
  log(`API: ${API_BASE}`, 'cyan');
  log(`时间: ${new Date().toLocaleString('zh-CN')}`, 'cyan');
  
  const results = [];
  
  // 测试编程能力
  log('\n\n📦 阶段1: 编程能力测试', 'cyan');
  log('═'.repeat(60), 'cyan');
  for (let i = 0; i < testCases.programming.length; i++) {
    const result = await runTest('programming', testCases.programming[i], i);
    result.category = 'programming';
    results.push(result);
    await new Promise(resolve => setTimeout(resolve, 2000)); // 间隔2秒
  }
  
  // 测试复杂问题解决
  log('\n\n🧩 阶段2: 复杂问题解决测试', 'yellow');
  log('═'.repeat(60), 'yellow');
  for (let i = 0; i < testCases.complexProblems.length; i++) {
    const result = await runTest('complexProblems', testCases.complexProblems[i], i);
    result.category = 'complexProblems';
    results.push(result);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  // 综合实战测试
  log('\n\n🎯 阶段3: 综合实战测试', 'magenta');
  log('═'.repeat(60), 'magenta');
  for (let i = 0; i < testCases.comprehensive.length; i++) {
    const result = await runTest('comprehensive', testCases.comprehensive[i], i);
    result.category = 'comprehensive';
    results.push(result);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  
  // 生成报告
  const stats = generateReport(results);
  
  // 保存结果到文件
  const reportPath = '/Users/ciss-ai/.openclaw/agents/pm/test-results-step-3.5-flash.json';
  require('fs').writeFileSync(reportPath, JSON.stringify({
    model: MODEL,
    timestamp: new Date().toISOString(),
    stats,
    results: results.map(r => ({
      name: r.name,
      category: r.category,
      difficulty: r.difficulty,
      success: r.success,
      metrics: r.metrics
    }))
  }, null, 2));
  
  log(`\n✅ 测试报告已保存: ${reportPath}`, 'green');
}

main().catch(console.error);
