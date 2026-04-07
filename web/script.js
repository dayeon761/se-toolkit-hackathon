document.getElementById('feedbackForm').onsubmit = async (e) => {
    e.preventDefault();
    
    const author = document.getElementById('author').value || 'Аноним';
    const rating = parseInt(document.getElementById('rating').value);
    const category = document.getElementById('category').value;
    const message = document.getElementById('message').value;

    const data = {
        author: author,
        rating: rating,
        category: category,
        message: message
    };

    try {
        const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            document.getElementById('result').innerHTML = '<p style="color: #27ae60; font-weight: 600;">✅ Спасибо за отзыв!</p>';
            document.getElementById('feedbackForm').reset();
            setTimeout(() => {
                document.getElementById('result').innerHTML = '';
            }, 3000);
        } else {
            document.getElementById('result').innerHTML = '<p style="color: #e74c3c; font-weight: 600;">❌ Ошибка. Попробуйте позже.</p>';
        }
    } catch (error) {
        document.getElementById('result').innerHTML = '<p style="color: #e74c3c; font-weight: 600;">❌ Ошибка соединения с сервером.</p>';
    }
};
