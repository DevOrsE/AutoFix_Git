
let items = [];

function addWorkItem() {
  const partSelect = document.getElementById("part");
  const serviceSelect = document.getElementById("service");
  const bodyPartSelect = document.getElementById("body-part");

  // Защита от пустого выбора кузовной детали
  if (bodyPartSelect.selectedIndex === -1) {
    alert("Выберите кузовную деталь!");
    return;
  }

  const partId = partSelect.value;
  const serviceId = serviceSelect.value;
  const bodyPartId = bodyPartSelect.value;

  const partText = partSelect.options[partSelect.selectedIndex].text;
  const serviceText = serviceSelect.options[serviceSelect.selectedIndex].text;
  const bodyText = bodyPartSelect.options[bodyPartSelect.selectedIndex].text;

  const priceMatch = serviceText.match(/(\d+(?:[.,]\d+)?)\s*₽/);
  const price = priceMatch ? parseFloat(priceMatch[1].replace(",", ".")) : 0;


  items.push({
    part_id: parseInt(partId),
    part_text: partText,
    service_id: parseInt(serviceId),
    service_text: serviceText,
    body_part_id: parseInt(bodyPartId),
    body_text: bodyText,
    price: price
  });

  renderList();
}


function renderList() {
  const list = document.getElementById("items-list");
  const base = document.getElementById("total-price");
  const final = document.getElementById("total-with-fee");
  list.innerHTML = "";

  let total = 0;

  items.forEach((item, index) => {
    total += item.price;

    const row = document.createElement("li");
    row.className = "list-group-item d-flex justify-content-between align-items-center";
    row.innerHTML = `
      <div>${item.service_text} — ${item.part_text} — ${item.body_text}</div>
      <div>
        ${item.price.toFixed(2)} ₽
        <button onclick="removeItem(${index})" class="btn btn-danger btn-sm ms-2">Удалить</button>
      </div>
    `;
    list.appendChild(row);
  });

  const finalPrice = total + total * 0.15;
  base.textContent = total.toFixed(2);
  final.textContent = finalPrice.toFixed(2);
}

function removeItem(index) {
  items.splice(index, 1);
  renderList();
}

function submitOrder() {
  const carId = document.getElementById("car_id").value;

  if (!items.length) {
    alert("Добавьте хотя бы одну работу в заказ!");
    return;
  }

  fetch("/confirm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ car_id: carId, items: items })
  })
  .then(res => {
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
  })
  .then(data => {
    if (data.success) {
      alert("✅ Заказ оформлен!");
      items = [];
      renderList();
      window.location.href = "/account";
    } else {
      alert("❌ Ошибка: " + data.message);
    }
  })
  .catch(err => alert("Ошибка при отправке: " + err));
}
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-complete").forEach(btn => {
    btn.addEventListener("click", function () {
      const orderId = this.dataset.orderId;
      fetch(`/orders/${orderId}/complete`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrf_token")  // если включён CSRF
        }
      }).then(res => {
        if (res.ok) {
          // Удаляем карточку
          this.closest(".col").remove();
        } else {
          alert("Не удалось обновить статус.");
        }
      });
    });
  });
});

// Функция для чтения куки (если CSRF включён)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

