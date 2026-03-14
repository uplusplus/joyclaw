// JoyClaw Web 应用 JavaScript

// API 基础路径
const API_BASE = '/api';

// 显示加载动画
function showLoading() {
    document.getElementById('loading').style.display = 'flex';
}

// 隐藏加载动画
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

// 显示面板
function showPanel(panelName) {
    // 隐藏所有面板
    document.querySelectorAll('.panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    // 显示选中的面板
    document.getElementById(`${panelName}-panel`).classList.add('active');
    
    // 更新菜单状态
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
}

// 发送消息
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // 显示用户消息
    addMessage('user', message);
    input.value = '';
    
    // 调用 API
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: message})
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessage('assistant', data.response);
        } else {
            addMessage('assistant', `错误: ${data.error}`);
        }
    } catch (error) {
        addMessage('assistant', `网络错误: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// 添加消息到聊天框
function addMessage(role, content) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(content)}</div>`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// 清空历史
async function clearHistory() {
    if (!confirm('确定要清空对话历史吗？')) return;
    
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/history/clear`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('chat-messages').innerHTML = `
                <div class="message system">
                    <div class="message-content">对话历史已清空</div>
                </div>
            `;
        }
    } catch (error) {
        alert('清空失败: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 列出文件
async function listFiles() {
    const directory = document.getElementById('file-directory').value;
    const pattern = document.getElementById('file-pattern').value || null;
    
    showLoading();
    try {
        let url = `${API_BASE}/files/list?directory=${encodeURIComponent(directory)}`;
        if (pattern) {
            url += `&pattern=${encodeURIComponent(pattern)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            const filesList = document.getElementById('files-list');
            filesList.innerHTML = data.files.map(file => `
                <div class="file-item" onclick="readFile('${file}')">
                    📄 ${escapeHtml(file)}
                </div>
            `).join('');
        } else {
            document.getElementById('files-list').innerHTML = `<p class="empty-message">错误: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('files-list').innerHTML = `<p class="empty-message">网络错误: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// 读取文件
async function readFile(path) {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/files/read?path=${encodeURIComponent(path)}`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('file-content').innerHTML = `
                <h3>${escapeHtml(path)}</h3>
                <pre>${escapeHtml(data.content)}</pre>
            `;
            
            // 同时填充到编辑器
            document.getElementById('edit-file-path').value = path;
            document.getElementById('edit-file-content').value = data.content;
        } else {
            document.getElementById('file-content').innerHTML = `<p class="empty-message">错误: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('file-content').innerHTML = `<p class="empty-message">网络错误: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// 写入文件
async function writeFile() {
    const path = document.getElementById('edit-file-path').value;
    const content = document.getElementById('edit-file-content').value;
    
    if (!path) {
        alert('请输入文件路径');
        return;
    }
    
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/files/write`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path: path, content: content})
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('文件保存成功！');
            listFiles(); // 刷新文件列表
        } else {
            alert('保存失败: ' + data.error);
        }
    } catch (error) {
        alert('网络错误: ' + error.message);
    } finally {
        hideLoading();
    }
}

// 执行命令
async function executeCommand() {
    const command = document.getElementById('command-input').value;
    const cwd = document.getElementById('command-cwd').value || null;
    
    if (!command) {
        alert('请输入命令');
        return;
    }
    
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/command/execute`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({command: command, cwd: cwd})
        });
        
        const data = await response.json();
        
        const outputDiv = document.getElementById('command-output');
        if (data.success) {
            outputDiv.innerHTML = `
<strong>$ ${escapeHtml(command)}</strong>

${data.stdout ? '<span style="color: #00ff00;">' + escapeHtml(data.stdout) + '</span>' : ''}
${data.stderr ? '<span style="color: #ff6b6b;">' + escapeHtml(data.stderr) + '</span>' : ''}

返回码: ${data.return_code}
            `;
        } else {
            outputDiv.innerHTML = `<span style="color: #ff6b6b;">错误: ${escapeHtml(data.error)}</span>`;
        }
    } catch (error) {
        document.getElementById('command-output').innerHTML = `<span style="color: #ff6b6b;">网络错误: ${error.message}</span>`;
    } finally {
        hideLoading();
    }
}

// 快速命令
function quickCommand(cmd) {
    document.getElementById('command-input').value = cmd;
    executeCommand();
}

// 获取系统信息
async function getSystemInfo() {
    showLoading();
    try {
        const response = await fetch(`${API_BASE}/system/info`);
        const data = await response.json();
        
        if (data.success) {
            const info = data.info;
            document.getElementById('system-info').innerHTML = `
                <div class="info-item">
                    <span class="info-label">操作系统</span>
                    <span class="info-value">${info.system} ${info.release}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">版本</span>
                    <span class="info-value">${info.version}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">架构</span>
                    <span class="info-value">${info.machine}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">处理器</span>
                    <span class="info-value">${info.processor || 'N/A'}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">主机名</span>
                    <span class="info-value">${info.hostname}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">当前用户</span>
                    <span class="info-value">${info.user}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Python 版本</span>
                    <span class="info-value">${info.python_version}</span>
                </div>
            `;
        } else {
            document.getElementById('system-info').innerHTML = `<p class="empty-message">错误: ${data.error}</p>`;
        }
    } catch (error) {
        document.getElementById('system-info').innerHTML = `<p class="empty-message">网络错误: ${error.message}</p>`;
    } finally {
        hideLoading();
    }
}

// HTML 转义
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 键盘事件
document.addEventListener('DOMContentLoaded', function() {
    // Ctrl+Enter 发送消息
    document.getElementById('user-input').addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Enter 执行命令
    document.getElementById('command-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            executeCommand();
        }
    });
});
