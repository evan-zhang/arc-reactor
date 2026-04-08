#!/usr/bin/env node

/**
 * OpenClaw 文档管理工具
 *
 * Usage:
 *   node docs-manager.js add [options]
 *   node docs-manager.js search [query]
 *   node docs-manager.js list
 *   node docs-manager.js stats
 */

const fs = require('fs')
const path = require('path')

const DOCS_ROOT = path.join(process.env.HOME, '.openclaw', 'docs')
const INDEX_FILE = path.join(DOCS_ROOT, 'index.json')
const INDEX_MD = path.join(DOCS_ROOT, 'index.md')

// 读取索引
function readIndex() {
  try {
    return JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'))
  } catch (error) {
    console.error('❌ 无法读取索引文件:', error.message)
    return null
  }
}

// 保存索引
function saveIndex(index) {
  try {
    index.lastUpdated = new Date().toISOString()

    fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2))
    console.log('✅ 索引已更新')
    return true
  } catch (error) {
    console.error('❌ 无法保存索引:', error.message)
    return false
  }
}

// 添加文档
function addDoc(options) {
  const index = readIndex()
  if (!index) return

  const doc = {
    id: options.id || `doc-${Date.now()}`,
    title: options.title,
    path: options.path,
    topic: options.topic,
    agent: options.agent,
    type: options.type || 'document',
    status: options.status || 'active',
    files: options.files || [],
    tags: options.tags || [],
    summary: options.summary || '',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }

  index.docs.push(doc)

  // 更新统计
  index.stats.totalDocs = index.docs.length
  index.stats.lastUpdated = new Date().toISOString()

  if (saveIndex(index)) {
    console.log(`\n✅ 文档已添加: ${doc.title}`)
    console.log(`   ID: ${doc.id}`)
    console.log(`   位置: ${doc.path}`)
  }
}

// 搜索文档
function searchDocs(query) {
  const index = readIndex()
  if (!index) return

  const q = query.toLowerCase()
  const results = index.docs.filter(doc =>
    doc.title.toLowerCase().includes(q) ||
    doc.summary.toLowerCase().includes(q) ||
    doc.tags.some(tag => tag.toLowerCase().includes(q)) ||
    doc.topic.toLowerCase().includes(q)
  )

  console.log(`\n🔍 搜索结果: "${query}" (${results.length} 个文档)\n`)

  results.forEach((doc, i) => {
    console.log(`${i + 1}. ${doc.title}`)
    console.log(`   ID: ${doc.id}`)
    console.log(`   位置: ${doc.path}`)
    console.log(`   Agent: ${doc.agent}`)
    console.log(`   主题: ${doc.topic}`)
    console.log(`   标签: ${doc.tags.join(', ')}`)
    console.log(`   摘要: ${doc.summary.substring(0, 100)}...`)
    console.log()
  })
}

// 列出所有文档
function listDocs() {
  const index = readIndex()
  if (!index) return

  console.log(`\n📋 所有文档 (${index.docs.length} 个)\n`)

  index.docs.forEach((doc, i) => {
    console.log(`${i + 1}. ${doc.title}`)
    console.log(`   ID: ${doc.id}`)
    console.log(`   位置: ${doc.path}`)
    console.log(`   状态: ${doc.status === 'completed' ? '✅' : '🔄'}`)
    console.log(`   更新: ${new Date(doc.updatedAt).toLocaleString('zh-CN')}`)
    console.log()
  })
}

// 显示统计
function showStats() {
  const index = readIndex()
  if (!index) return

  console.log('\n📊 文档统计\n')
  console.log(`总文档数: ${index.stats.totalDocs}`)
  console.log(`总 Agents: ${index.stats.totalAgents}`)
  console.log(`总主题: ${index.stats.totalTopics}`)
  console.log(`总大小: ${index.stats.totalSize}`)
  console.log(`最后更新: ${new Date(index.lastUpdated).toLocaleString('zh-CN')}`)

  console.log('\n📂 按 Agent:')
  index.agents.forEach(agent => {
    console.log(`  ${agent.name}: ${agent.docs} 个文档`)
  })

  console.log('\n📂 按主题:')
  index.topics.forEach(topic => {
    console.log(`  ${topic.name}: ${topic.docs} 个文档`)
  })

  console.log()
}

// 生成 Markdown 索引
function generateMarkdownIndex() {
  const index = readIndex()
  if (!index) return

  let md = `# OpenClaw 文档中心

> 统一的文档管理和索引系统
> 最后更新：${new Date(index.lastUpdated).toLocaleDateString('zh-CN')}

---

## 📊 统计

- **总文档数**: ${index.stats.totalDocs}
- **涉及 Agents**: ${index.stats.totalAgents}
- **主题分类**: ${index.stats.totalTopics}
- **总大小**: ${index.stats.totalSize}

---

## 📂 按主题分类

`

  // 按主题分组
  const byTopic = {}
  index.docs.forEach(doc => {
    if (!byTopic[doc.topic]) byTopic[doc.topic] = []
    byTopic[doc.topic].push(doc)
  })

  // 生成主题部分
  Object.entries(byTopic).forEach(([topic, docs]) => {
    const topicName = topic.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')
    md += `### ${topicName}\n\n`

    docs.forEach(doc => {
      md += `#### ${doc.title}\n\n`
      md += `**文档 ID**: \`${doc.id}\`\n`
      md += `**Agent**: ${doc.agent}\n`
      md += `**状态**: ${doc.status === 'completed' ? '✅ 已完成' : '🔄 进行中'}\n`
      md += `**标签**: ${doc.tags.join(', ')}\n\n`

      md += `**概述**:\n${doc.summary}\n\n`

      if (doc.files && doc.files.length > 0) {
        md += `**文件**:\n`
        doc.files.forEach((file, i) => {
          md += `${i + 1}. \`${file.name}\`\n`
          if (file.description) {
            md += `   - ${file.description}\n`
          }
        })
        md += '\n'
      }

      md += `**位置**: \`${doc.path}\`\n`
      md += `**更新时间**: ${new Date(doc.updatedAt).toLocaleDateString('zh-CN')}\n\n`
      md += `---\n\n`
    })
  })

  fs.writeFileSync(INDEX_MD, md)
  console.log('✅ Markdown 索引已生成')
}

// 主函数
function main() {
  const args = process.argv.slice(2)
  const command = args[0]

  switch (command) {
    case 'add':
      const options = {
        id: args['--id'],
        title: args['--title'],
        path: args['--path'],
        topic: args['--topic'],
        agent: args['--agent'],
        type: args['--type'],
        status: args['--status'],
        summary: args['--summary'],
        tags: args['--tags'] ? args['--tags'].split(',') : []
      }
      addDoc(options)
      break

    case 'search':
      searchDocs(args[1] || '')
      break

    case 'list':
      listDocs()
      break

    case 'stats':
      showStats()
      break

    case 'generate':
      generateMarkdownIndex()
      break

    case 'help':
    case '--help':
    case '-h':
      console.log(`
📚 OpenClaw 文档管理工具

用法:
  node docs-manager.js add [options]         添加新文档
  node docs-manager.js search [query]         搜索文档
  node docs-manager.js list                   列出所有文档
  node docs-manager.js stats                  显示统计信息
  node docs-manager.js generate               生成 Markdown 索引
  node docs-manager.js help                   显示帮助

添加文档选项:
  --id <id>              文档 ID
  --title <title>         文档标题
  --path <path>           文件路径
  --topic <topic>         主题分类
  --agent <agent>         所属 agent
  --type <type>           文档类型
  --status <status>       状态
  --summary <summary>     摘要
  --tags <tags>           标签（逗号分隔）

示例:
  node docs-manager.js search model
  node docs-manager.js list
  node docs-manager.js stats
  node docs-manager.js generate
`)
      break

    default:
      console.log('❌ 未知命令。使用 "help" 查看帮助')
  }
}

if (require.main === module) {
  main()
}

module.exports = {
  readIndex,
  saveIndex,
  addDoc,
  searchDocs,
  listDocs,
  showStats,
  generateMarkdownIndex
}
