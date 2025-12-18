/**
 * 森系智韵智能空气管理平台 - 主JavaScript文件
 */

// 全局配置
const CONFIG = {
    API_BASE: '/api',
    BUTLER_WELCOME: '您好！我是森系智韵的AI空气管家。有什么可以帮助您的吗？',
    QUICK_REPLIES: [
        { text: '推荐产品', action: 'recommend' },
        { text: '空气知识', action: 'knowledge' },
        { text: '售后服务', action: 'service' },
        { text: '联系客服', action: 'contact' }
    ]
};

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initButlerWidget();
    initScrollEffects();
    initLazyLoading();
});

/**
 * AI空气管家浮窗
 */
function initButlerWidget() {
    const butlerWidget = document.getElementById('butler-widget');
    const butlerFab = document.getElementById('butler-fab');
    const openButlerBtn = document.getElementById('open-butler');
    const closeButlerBtn = document.getElementById('close-butler');
    const butlerMessages = document.getElementById('butler-messages');
    const butlerQuickReplies = document.getElementById('butler-quick-replies');
    const butlerInput = document.getElementById('butler-input');
    const butlerSend = document.getElementById('butler-send');
    
    if (!butlerWidget || !butlerFab) return;
    
    let isOpen = false;
    let conversationHistory = [];
    
    // 打开/关闭浮窗
    function toggleButler() {
        isOpen = !isOpen;
        butlerWidget.classList.toggle('hidden', !isOpen);
        butlerFab.classList.toggle('hidden', isOpen);
        
        if (isOpen && conversationHistory.length === 0) {
            // 首次打开，显示欢迎消息
            addBotMessage(CONFIG.BUTLER_WELCOME);
            showQuickReplies();
        }
    }
    
    // 添加机器人消息
    function addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-3';
        messageDiv.innerHTML = `
            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                <i data-lucide="bot" class="w-4 h-4 text-primary-600"></i>
            </div>
            <div class="bg-white border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-2 max-w-xs shadow-sm">
                <p class="text-gray-800 text-sm">${text}</p>
            </div>
        `;
        butlerMessages.appendChild(messageDiv);
        butlerMessages.scrollTop = butlerMessages.scrollHeight;
        lucide.createIcons();
        
        conversationHistory.push({ role: 'assistant', content: text });
    }
    
    // 添加用户消息
    function addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-3 flex-row-reverse';
        messageDiv.innerHTML = `
            <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center flex-shrink-0">
                <i data-lucide="user" class="w-4 h-4 text-white"></i>
            </div>
            <div class="bg-primary-600 text-white rounded-2xl rounded-br-sm px-4 py-2 max-w-xs">
                <p class="text-sm">${text}</p>
            </div>
        `;
        butlerMessages.appendChild(messageDiv);
        butlerMessages.scrollTop = butlerMessages.scrollHeight;
        lucide.createIcons();
        
        conversationHistory.push({ role: 'user', content: text });
    }
    
    // 显示快捷回复
    function showQuickReplies() {
        butlerQuickReplies.innerHTML = '';
        CONFIG.QUICK_REPLIES.forEach(reply => {
            const btn = document.createElement('button');
            btn.className = 'px-3 py-1 bg-gray-100 hover:bg-primary-100 text-gray-700 hover:text-primary-700 rounded-full text-sm transition-colors';
            btn.textContent = reply.text;
            btn.addEventListener('click', () => handleQuickReply(reply));
            butlerQuickReplies.appendChild(btn);
        });
    }
    
    // 处理快捷回复
    function handleQuickReply(reply) {
        addUserMessage(reply.text);
        butlerQuickReplies.innerHTML = '';
        
        // 显示加载状态
        showTypingIndicator();
        
        // 模拟API响应
        setTimeout(() => {
            hideTypingIndicator();
            
            switch(reply.action) {
                case 'recommend':
                    addBotMessage('根据您的需求，我推荐以下产品：\n\n1. 净界者·森林呼吸Pro - 适合40-60㎡空间\n2. 净界者·清新之风Max - 适合大户型\n\n您可以前往智能导购获取更精准的推荐。');
                    break;
                case 'knowledge':
                    addBotMessage('空气研究院为您提供专业的空气健康知识：\n\n• PM2.5的危害与防护\n• 甲醛去除指南\n• 室内空气质量标准\n\n点击导航栏"空气研究院"了解更多。');
                    break;
                case 'service':
                    addBotMessage('售后服务支持：\n\n• 产品保修：3年整机质保\n• 滤芯更换：支持上门服务\n• 故障报修：400-888-8888\n\n工作时间：9:00-21:00');
                    break;
                case 'contact':
                    addBotMessage('联系方式：\n\n📞 客服热线：400-888-8888\n📧 邮箱：service@senxi-air.com\n💬 在线客服：工作日9:00-21:00\n\n您也可以直接在这里向我提问！');
                    break;
            }
            
            showQuickReplies();
        }, 1000);
    }
    
    // 显示打字指示器
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'typing-indicator';
        indicator.className = 'flex items-start space-x-3';
        indicator.innerHTML = `
            <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                <i data-lucide="bot" class="w-4 h-4 text-primary-600"></i>
            </div>
            <div class="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        butlerMessages.appendChild(indicator);
        butlerMessages.scrollTop = butlerMessages.scrollHeight;
        lucide.createIcons();
    }
    
    // 隐藏打字指示器
    function hideTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
    
    // 发送消息
    async function sendMessage() {
        const text = butlerInput.value.trim();
        if (!text) return;
        
        addUserMessage(text);
        butlerInput.value = '';
        butlerQuickReplies.innerHTML = '';
        
        showTypingIndicator();
        
        try {
            const response = await fetch(`${CONFIG.API_BASE}/butler/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: text,
                    history: conversationHistory.slice(-10)
                })
            });
            
            const data = await response.json();
            hideTypingIndicator();
            addBotMessage(data.response || '抱歉，我暂时无法回答这个问题。请稍后再试或联系人工客服。');
        } catch (error) {
            hideTypingIndicator();
            // 本地回复
            const localResponse = getLocalResponse(text);
            addBotMessage(localResponse);
        }
        
        showQuickReplies();
    }
    
    // 本地响应（API不可用时的备用）
    function getLocalResponse(text) {
        const keywords = {
            '价格|多少钱|费用': '我们的产品价格从1299元到7999元不等，具体价格请查看产品详情页。您也可以使用智能导购，根据您的需求和预算获取推荐。',
            '甲醛|除醛|装修': '针对甲醛问题，我推荐使用净界者·森林呼吸Pro，它配备光触媒分解技术，可以有效分解甲醛。新装修的房间建议持续开启净化器。',
            '过敏|花粉|鼻炎': '对于过敏人群，我推荐选择配备H13级HEPA滤网的产品，可以过滤99.97%的过敏原。净界者·清新之风Max是不错的选择。',
            '噪音|声音|安静': '我们的产品在睡眠模式下噪音低至20分贝，不会影响您的休息。您可以在产品详情页查看具体的噪音参数。',
            '滤芯|更换|耗材': '滤芯建议6-12个月更换一次，具体取决于使用环境和频率。您可以在产品中心购买原装滤芯，我们提供上门更换服务。',
            '保修|质保|售后': '所有净界者产品享受3年整机质保，滤芯1年质保。如有问题，请拨打400-888-8888或在线提交售后申请。'
        };
        
        for (const [pattern, response] of Object.entries(keywords)) {
            if (new RegExp(pattern).test(text)) {
                return response;
            }
        }
        
        return '感谢您的咨询！您可以：\n\n1. 使用智能导购获取产品推荐\n2. 浏览空气研究院了解更多知识\n3. 拨打400-888-8888联系人工客服\n\n还有其他问题吗？';
    }
    
    // 事件绑定
    butlerFab.addEventListener('click', toggleButler);
    openButlerBtn?.addEventListener('click', toggleButler);
    closeButlerBtn?.addEventListener('click', toggleButler);
    butlerSend?.addEventListener('click', sendMessage);
    butlerInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}

/**
 * 滚动效果
 */
function initScrollEffects() {
    // 导航栏滚动效果
    const nav = document.querySelector('nav');
    if (nav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('shadow-md');
            } else {
                nav.classList.remove('shadow-md');
            }
        });
    }
    
    // 元素进入视口动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

/**
 * 图片懒加载
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

/**
 * 工具函数
 */
const Utils = {
    // 格式化价格
    formatPrice(price) {
        return new Intl.NumberFormat('zh-CN', {
            style: 'currency',
            currency: 'CNY',
            minimumFractionDigits: 0
        }).format(price);
    },
    
    // 格式化日期
    formatDate(date) {
        return new Intl.DateTimeFormat('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(new Date(date));
    },
    
    // 防抖
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // 节流
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // 显示提示
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 animate-fade-in ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' :
            'bg-gray-800 text-white'
        }`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
};

// 导出工具函数
window.Utils = Utils;
