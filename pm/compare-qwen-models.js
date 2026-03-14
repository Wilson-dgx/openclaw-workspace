#!/usr/bin/env node
/**
 * Qwen3.5-27B vs Qwen3.5-35B-A3B 对比测试
 * 测试维度：编程能力、复杂问题解决、Token性能、响应时间
 */

const http = require('http');
const { performance } = require('perf_hooks');

const API_BASE = 'http://localhost:1234/v1';
const MODELS = [
  { id: 'qwen3.5-27b', name: 'Qwen3.5-27B', color: 'cyan' },
  { id: 'qwen/qwen3.5-35b-a3b', name: 'Qwen3.5-35B-A3B', color: 'yellow' }
];

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
async function callAPI(model, prompt, maxTokens = 2048, temperature = 0.7) {
  return new Promise((resolve, reject) => {
    const startTime = performance.now();
    
    const requestData = JSON.stringify({
      model: model.id,
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
      },
      timeout: 120000 // 2分钟超时
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
          const responseTime = endTime - startTime;
          
          resolve({
            content,
            promptTokens: usage.prompt_tokens || 0,
            completionTokens: usage.completion_tokens || 0,
            totalTokens: usage.total_tokens || 0,
            responseTime,
            tokensPerSecond: usage.completion_tokens ? 
              (usage.completion_tokens / (responseTime / 1000)).toFixed(2) : 0,
            timeToFirstToken: responseTime * 0.1 // 估算
          });
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    req.write(requestData);
    req.end();
  });
}

// 测试用例（精简版，专注于对比）
const testCases = [
  {
    name: '编程 - 快速排序实现',
    category: 'programming',
    difficulty: '★☆☆',
    prompt: `用Python实现快速排序算法，要求：
1. 使用列表推导式
2. 包含时间复杂度分析
3. 提供2个测试用例

简洁输出，不要多余的话。`
  },
  {
    name: '编程 - 并发Bug修复',
    category: 'programming',
    difficulty: '★★★',
    prompt: `这段Python代码有并发bug，请找出所有问题并修复：

\`\`\`python
import threading

class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        current = self.value
        import time; time.sleep(0.001)
        self.value = current + 1

counter = Counter()
threads = [threading.Thread(target=counter.increment) for _ in range(100)]
for t in threads: t.start()
for t in threads: t.join()
print(f"最终值: {counter.value}")  # 期望100，实际小于100
\`\`\`

请：
1. 指出所有bug
2. 提供修复后的代码
3. 解释修复原理`
  },
  {
    name: '逻辑 - 三门问题',
    category: 'reasoning',
    difficulty: '★★☆',
    prompt: `三门问题：有3扇门，1扇后有汽车，2扇后有山羊。你选了1号门，主持人打开3号门（山羊），问要不要换到2号门？

请：
1. 给出答案和理由
2. 用贝叶斯定理证明
3. 如果是100扇门呢？`
  },
  {
    name: '系统设计 - URL短链接',
    category: 'system',
    difficulty: '★★★★',
    prompt: `设计一个短链接服务（类似bit.ly），需要：
- 每天100万次访问，1万次创建
- 短链接≤7字符
- 统计点击数据

请设计：
1. 架构图（文字描述）
2. 数据库表结构
3. 短链接生成算法
4. 缓存策略

输出要简洁清晰。`
  },
  {
    name: '性能优化 - SQL慢查询',
    category: 'optimization',
    difficulty: '★★★★',
    prompt: `MySQL查询性能问题：
- orders表2000万行
- 查询：SELECT * FROM orders WHERE user_id = ? AND status IN (1,2) ORDER BY created_at DESC LIMIT 20
- user_id有索引，status和created_at无索引
- 最近营销活动订单量增长3倍，查询从200ms变到5秒

请：
1. 分析3个可能的瓶颈
2. 短期解决方案（今天上线）
3. 中长期优化方案`
  }
];

// 评估代码质量
function evaluateCodeQuality(content) {
  const issues = [];
  let score = 100;
  
  // 检查常见错误
  if (content.includes('self.ccache')) {
    issues.push('拼写错误: ccache -> cache');
    score -= 10;
  }
  if (content.includes('.bbalance')) {
    issues.push('拼写错误: bbalance -> balance');
    score -= 10;
  }
  if (content.includes('列表推导式 if')) {
    issues.push('变量名错误: 应为arr而非"列表推导式"');
    score -= 10;
  }
  if (content.includes('def ') && content.includes('(') && !content.includes('):')) {
    issues.push('函数定义可能缺少冒号');
    score -= 5;
  }
  
  return { score, issues };
}

// 测试单个用例
async function runTest(model, testCase, index) {
  log(`\n  [${index + 1}] ${testCase.name} (${testCase.difficulty})`, model.color);
  
  try {
    const result = await callAPI(model, testCase.prompt);
    
    const quality = testCase.category === 'programming' ? 
      evaluateCodeQuality(result.content) : { score: null, issues: [] };
    
    log(`    ✓ 速度: ${result.tokensPerSecond} tok/s`, 'green');
    log(`    ✓ 时间: ${(result.responseTime/1000).toFixed(1)}s`, 'green');
    log(`    ✓ Tokens: ${result.completionTokens}`, 'green');
    if (quality.score !== null) {
      log(`    ✓ 代码质量: ${quality.score}分`, quality.score >= 80 ? 'green' : 'yellow');
      if (quality.issues.length > 0) {
        quality.issues.forEach(issue => log(`      - ${issue}`, 'red'));
      }
    }
    
    return {
      name: testCase.name,
      category: testCase.category,
      difficulty: testCase.difficulty,
      success: true,
      metrics: result,
      quality
    };
  } catch (error) {
    log(`    ✗ 失败: ${error.message}`, 'red');
    return {
      name: testCase.name,
      success: false,
      error: error.message
    };
  }
}

// 测试单个模型
async function testModel(model) {
  log(`\n${'═'.repeat(60)}`, model.color);
  log(`🤖 测试模型: ${model.name}`, 'bright');
  log(`${'═'.repeat(60)}`, model.color);
  
  const results = [];
  const categories = {
    programming: [],
    reasoning: [],
    system: [],
    optimization: []
  };
  
  for (let i = 0; i < testCases.length; i++) {
    const result = await runTest(model, testCases[i], i);
    results.push(result);
    
    if (result.success && categories[result.category]) {
      categories[result.category].push(result);
    }
    
    // 间隔1秒，避免过载
    if (i < testCases.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  return { model, results, categories };
}

// 生成对比报告
function generateComparisonReport(modelResults) {
  log(`\n\n${'█'.repeat(70)}`, 'bright');
  log('📊 模型对比报告', 'bright');
  log(`${'█'.repeat(70)}`, 'bright');
  
  // 提取数据
  const [r1, r2] = modelResults;
  const m1 = r1.model;
  const m2 = r2.model;
  
  // 计算统计数据
  const stats1 = calculateStats(r1.results);
  const stats2 = calculateStats(r2.results);
  
  // 1. 总体性能对比
  log(`\n【1️⃣ 总体性能对比】`, 'cyan');
  log('─'.repeat(70), 'cyan');
  log(`\n  指标                ${m1.name.padEnd(20)} ${m2.name}`, 'bright');
  log('  ' + '─'.repeat(65));
  
  const metrics = [
    { name: '测试成功率', v1: `${stats1.successRate}/${testCases.length}`, v2: `${stats2.successRate}/${testCases.length}` },
    { name: '平均生成速度', v1: `${stats1.avgSpeed} tok/s`, v2: `${stats2.avgSpeed} tok/s` },
    { name: '最快速度', v1: `${stats1.maxSpeed} tok/s`, v2: `${stats2.maxSpeed} tok/s` },
    { name: '最慢速度', v1: `${stats1.minSpeed} tok/s`, v2: `${stats2.minSpeed} tok/s` },
    { name: '平均响应时间', v1: `${(stats1.avgTime/1000).toFixed(1)}s`, v2: `${(stats2.avgTime/1000).toFixed(1)}s` },
    { name: '总Token消耗', v1: stats1.totalTokens.toString(), v2: stats2.totalTokens.toString() }
  ];
  
  metrics.forEach(m => {
    const winner = compareMetric(m.name, m.v1, m.v2);
    const indicator = winner === 1 ? '🥇' : winner === 2 ? '🥈' : '  ';
    log(`  ${indicator} ${m.name.padEnd(16)} ${m.v1.padEnd(20)} ${m.v2}`);
  });
  
  // 2. 分类性能对比
  log(`\n【2️⃣ 分类性能对比】`, 'yellow');
  log('─'.repeat(70), 'yellow');
  
  const categories = [
    { key: 'programming', name: '编程能力', icon: '💻' },
    { key: 'reasoning', name: '逻辑推理', icon: '🧠' },
    { key: 'system', name: '系统设计', icon: '🏗️' },
    { key: 'optimization', name: '性能优化', icon: '⚡' }
  ];
  
  categories.forEach(cat => {
    const c1 = r1.categories[cat.key];
    const c2 = r2.categories[cat.key];
    
    if (c1.length === 0 && c2.length === 0) return;
    
    const avg1 = c1.length > 0 ? (c1.reduce((sum, r) => sum + parseFloat(r.metrics?.tokensPerSecond || 0), 0) / c1.length).toFixed(2) : '-';
    const avg2 = c2.length > 0 ? (c2.reduce((sum, r) => sum + parseFloat(r.metrics?.tokensPerSecond || 0), 0) / c2.length).toFixed(2) : '-';
    
    const winner = parseFloat(avg1) > parseFloat(avg2) ? '🥇' : parseFloat(avg1) < parseFloat(avg2) ? '🥈' : '  ';
    
    log(`\n  ${cat.icon} ${cat.name}`, 'bright');
    log(`     ${m1.name}: ${avg1} tok/s`);
    log(`     ${m2.name}: ${avg2} tok/s`);
    log(`     ${winner} ${parseFloat(avg1) > parseFloat(avg2) ? m1.name : m2.name} 胜出`);
  });
  
  // 3. 代码质量对比
  log(`\n【3️⃣ 代码质量对比】`, 'magenta');
  log('─'.repeat(70), 'magenta');
  
  const codeTests1 = r1.results.filter(r => r.category === 'programming' && r.success);
  const codeTests2 = r2.results.filter(r => r.category === 'programming' && r.success);
  
  const avgQuality1 = codeTests1.length > 0 ? 
    (codeTests1.reduce((sum, r) => sum + (r.quality?.score || 0), 0) / codeTests1.length).toFixed(0) : '-';
  const avgQuality2 = codeTests2.length > 0 ?
    (codeTests2.reduce((sum, r) => sum + (r.quality?.score || 0), 0) / codeTests2.length).toFixed(0) : '-';
  
  log(`\n  ${m1.name}: ${avgQuality1}分`);
  codeTests1.forEach(t => {
    if (t.quality && t.quality.issues.length > 0) {
      log(`    - ${t.name}: ${t.quality.score}分`);
      t.quality.issues.forEach(issue => log(`      ⚠️  ${issue}`, 'yellow'));
    }
  });
  
  log(`\n  ${m2.name}: ${avgQuality2}分`);
  codeTests2.forEach(t => {
    if (t.quality && t.quality.issues.length > 0) {
      log(`    - ${t.name}: ${t.quality.score}分`);
      t.quality.issues.forEach(issue => log(`      ⚠️  ${issue}`, 'yellow'));
    }
  });
  
  // 4. 详细测试结果
  log(`\n【4️⃣ 详细测试结果】`, 'blue');
  log('─'.repeat(70), 'blue');
  
  testCases.forEach((tc, i) => {
    log(`\n  测试 ${i+1}: ${tc.name} (${tc.difficulty})`, 'bright');
    
    const r1Result = r1.results[i];
    const r2Result = r2.results[i];
    
    if (r1Result.success && r2Result.success) {
      const speed1 = parseFloat(r1Result.metrics.tokensPerSecond);
      const speed2 = parseFloat(r2Result.metrics.tokensPerSecond);
      const time1 = r1Result.metrics.responseTime;
      const time2 = r2Result.metrics.responseTime;
      
      log(`    ${m1.name}: ${speed1.toFixed(2)} tok/s, ${(time1/1000).toFixed(1)}s, ${r1Result.metrics.completionTokens} tok`);
      log(`    ${m2.name}: ${speed2.toFixed(2)} tok/s, ${(time2/1000).toFixed(1)}s, ${r2Result.metrics.completionTokens} tok`);
      
      if (speed1 > speed2 * 1.05) {
        log(`    🏆 ${m1.name} 速度领先 ${((speed1/speed2 - 1) * 100).toFixed(1)}%`, 'cyan');
      } else if (speed2 > speed1 * 1.05) {
        log(`    🏆 ${m2.name} 速度领先 ${((speed2/speed1 - 1) * 100).toFixed(1)}%`, 'yellow');
      } else {
        log(`    🤝 速度相当`, 'green');
      }
    } else {
      if (!r1Result.success) log(`    ❌ ${m1.name}: 失败`, 'red');
      if (!r2Result.success) log(`    ❌ ${m2.name}: 失败`, 'red');
    }
  });
  
  // 5. 总结和建议
  log(`\n【5️⃣ 总结和建议】`, 'green');
  log('─'.repeat(70), 'green');
  
  const overallWinner = parseFloat(stats1.avgSpeed) > parseFloat(stats2.avgSpeed) ? m1 : m2;
  const speedDiff = Math.abs(parseFloat(stats1.avgSpeed) - parseFloat(stats2.avgSpeed));
  const speedDiffPercent = (speedDiff / Math.min(parseFloat(stats1.avgSpeed), parseFloat(stats2.avgSpeed)) * 100).toFixed(1);
  
  log(`\n  🎯 速度冠军: ${overallWinner.name}`);
  log(`     平均速度差异: ${speedDiffPercent}%`);
  
  const quality1 = parseFloat(avgQuality1) || 0;
  const quality2 = parseFloat(avgQuality2) || 0;
  if (quality1 > 0 || quality2 > 0) {
    const qualityWinner = quality1 > quality2 ? m1 : m2;
    log(`\n  📝 代码质量冠军: ${qualityWinner.name}`);
    log(`     平均得分: ${quality1 > quality2 ? avgQuality1 : avgQuality2}分`);
  }
  
  log(`\n  💡 使用建议:`);
  if (speedDiffPercent < 10) {
    log(`     - 两个模型速度相当，可根据具体需求选择`);
  } else {
    log(`     - 追求速度: ${overallWinner.name}`);
  }
  
  if (quality1 > 0 && quality2 > 0 && Math.abs(quality1 - quality2) > 5) {
    const qWinner = quality1 > quality2 ? m1.name : m2.name;
    log(`     - 代码生成: ${qWinner} (质量更高)`);
  }
  
  log(`     - 复杂任务: 两个模型都能胜任`);
  log(`     - 日常使用: 建议根据模型大小和速度需求选择`);
  
  return {
    stats1,
    stats2,
    overallWinner: overallWinner.name,
    speedDiff: speedDiffPercent
  };
}

// 计算统计数据
function calculateStats(results) {
  const successResults = results.filter(r => r.success);
  
  const speeds = successResults.map(r => parseFloat(r.metrics.tokensPerSecond));
  const times = successResults.map(r => r.metrics.responseTime);
  const tokens = successResults.map(r => r.metrics.completionTokens);
  
  return {
    successRate: successResults.length,
    avgSpeed: (speeds.reduce((a, b) => a + b, 0) / speeds.length).toFixed(2),
    maxSpeed: Math.max(...speeds).toFixed(2),
    minSpeed: Math.min(...speeds).toFixed(2),
    avgTime: times.reduce((a, b) => a + b, 0) / times.length,
    totalTokens: tokens.reduce((a, b) => a + b, 0)
  };
}

// 比较指标
function compareMetric(name, v1, v2) {
  if (typeof v1 === 'string' && typeof v2 === 'string') {
    const n1 = parseFloat(v1);
    const n2 = parseFloat(v2);
    
    if (isNaN(n1) || isNaN(n2)) return 0;
    
    // 对于时间，越小越好
    if (name.includes('时间')) {
      return n1 < n2 ? 1 : n1 > n2 ? 2 : 0;
    }
    
    // 其他指标，越大越好
    return n1 > n2 ? 1 : n1 < n2 ? 2 : 0;
  }
  return 0;
}

// 主测试流程
async function main() {
  log('\n🚀 Qwen3.5-27B vs Qwen3.5-35B-A3B 对比测试', 'bright');
  log('═'.repeat(70), 'bright');
  log(`测试时间: ${new Date().toLocaleString('zh-CN')}`, 'cyan');
  log(`测试用例: ${testCases.length}个`, 'cyan');
  log(`API地址: ${API_BASE}`, 'cyan');
  
  // 检查模型可用性
  log('\n🔍 检查模型可用性...', 'yellow');
  try {
    const modelsRes = await new Promise((resolve, reject) => {
      http.get('http://localhost:1234/v1/models', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve(JSON.parse(data)));
      }).on('error', reject);
    });
    
    const availableModels = modelsRes.data.map(m => m.id);
    log(`  可用模型: ${availableModels.join(', ')}`, 'green');
    
    // 检查我们要测试的模型是否都可用
    for (const model of MODELS) {
      if (!availableModels.includes(model.id)) {
        log(`  ❌ 模型 ${model.name} 不可用！`, 'red');
        process.exit(1);
      }
    }
    log('  ✅ 所有目标模型可用', 'green');
  } catch (error) {
    log(`  ❌ 无法连接到LMstudio: ${error.message}`, 'red');
    process.exit(1);
  }
  
  // 测试两个模型
  const modelResults = [];
  
  for (const model of MODELS) {
    const result = await testModel(model);
    modelResults.push(result);
    
    // 模型之间间隔5秒
    if (modelResults.length < MODELS.length) {
      log(`\n  ⏳ 等待5秒后测试下一个模型...`, 'yellow');
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  
  // 生成对比报告
  const summary = generateComparisonReport(modelResults);
  
  // 保存结果
  const reportPath = '/Users/ciss-ai/.openclaw/agents/pm/qwen-comparison-report.json';
  const fs = require('fs');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    models: MODELS.map(m => m.name),
    testCases: testCases.map(tc => ({ name: tc.name, category: tc.category })),
    results: modelResults.map(mr => ({
      model: mr.model.name,
      stats: calculateStats(mr.results),
      tests: mr.results.map(r => ({
        name: r.name,
        success: r.success,
        speed: r.metrics?.tokensPerSecond,
        time: r.metrics?.responseTime,
        tokens: r.metrics?.completionTokens,
        quality: r.quality?.score
      }))
    })),
    summary
  }, null, 2));
  
  log(`\n\n✅ 对比测试完成！`, 'green');
  log(`📄 报告已保存: ${reportPath}`, 'green');
}

main().catch(console.error);
