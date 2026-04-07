async function loadStats() {
    try {
        const res = await fetch('/api/stats');
        const data = await res.json();
        
        document.getElementById('totalFeedbacks').textContent = data.total;
        document.getElementById('avgRating').textContent = data.avg_rating;
        document.getElementById('todayFeedbacks').textContent = data.today;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

async function loadFeedbacks() {
    try {
        const res = await fetch('/api/feedback');
        const feedbacks = await res.json();
        
        const container = document.getElementById('feedbacksList');
        
        if (feedbacks.length === 0) {
            container.innerHTML = '<p class="loading">Отзывов пока нет.</p>';
            return;
        }
        
        container.innerHTML = feedbacks.map(fb => `
            <div class="feedback-item ${fb.is_read ? 'is-read' : ''}">
                <div class="feedback-header">
                    <span class="feedback-author">👤 ${fb.author}</span>
                    <span class="feedback-rating">${'⭐'.repeat(fb.rating || 0)}</span>
                    <span class="feedback-category">${getCategoryLabel(fb.category)}</span>
                    ${!fb.is_read ? '<span class="badge badge-new">NEW</span>' : '<span class="badge badge-read">Прочитано</span>'}
                </div>
                <p class="feedback-message">${fb.message}</p>
                <div class="feedback-date">
                    ${new Date(fb.created_at).toLocaleString('ru-RU')}
                </div>
                <div class="feedback-actions">
                    ${!fb.is_read ? `<button class="btn-mark-read" onclick="markAsRead(${fb.id})">Отметить как прочитанное</button>` : ''}
                    <button class="btn-delete" onclick="deleteFeedback(${fb.id})">Удалить</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading feedbacks:', error);
        document.getElementById('feedbacksList').innerHTML = '<p class="loading">Ошибка загрузки отзывов.</p>';
    }
}

async function markAsRead(id) {
    try {
        await fetch(`/api/feedback/${id}/read`, { method: 'PUT' });
        await loadStats();
        await loadFeedbacks();
    } catch (error) {
        console.error('Error marking as read:', error);
    }
}

async function deleteFeedback(id) {
    if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) {
        return;
    }
    
    try {
        await fetch(`/api/feedback/${id}`, { method: 'DELETE' });
        await loadStats();
        await loadFeedbacks();
    } catch (error) {
        console.error('Error deleting feedback:', error);
    }
}

function getCategoryLabel(category) {
    const labels = {
        'coffee': '☕ Кофе',
        'service': '🤝 Обслуживание',
        'atmosphere': '🏠 Атмосфера',
        'other': '📝 Другое'
    };
    return labels[category] || category;
}

// Загрузка данных при открытии страницы
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadFeedbacks();
    
    // Автообновление каждые 30 секунд
    setInterval(() => {
        loadStats();
        loadFeedbacks();
    }, 30000);
});
