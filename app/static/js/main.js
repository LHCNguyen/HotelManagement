function addToCart(roomId) {
        fetch(`/add_to_cart/${roomId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Cập nhật số lượng hiển thị trong giỏ hàng ngay lập tức
                document.getElementById('cart-count').textContent = data.cart_size;
            }
        })
        .catch(error => console.error('Error:', error));
    }

function removeFromCart(roomId) {
    fetch(`/remove_from_cart/${roomId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            console.error('Network response was not ok', response);
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            const cartCounter = document.getElementById('cart-count');
            if (cartCounter) {
                cartCounter.textContent = data.cart_size;
            } else {
                console.warn("Không tìm thấy phần tử với id 'cart-count'");
            }
            const itemElement = document.getElementById(`cart-item-${roomId}`);
            if (itemElement) {
                itemElement.remove();
            }

            const totalElement = document.getElementById('total-price');
            if (totalElement) {
                totalElement.textContent = `${data.total.toLocaleString()} VND`;
            }
        } else {
            console.error("Không thể xóa phòng khỏi giỏ hàng", data);
        }
    })
    .catch(error => console.error('Error:', error));
}
