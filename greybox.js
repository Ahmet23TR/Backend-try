// Ürünlerin olduğu listeyi seçin ve her birine tıklandığında işlevsellik ekleyin
document.querySelectorAll(".product-item").forEach((item) => {
  item.addEventListener("click", () => {
    clearAndSelectItem(item);
    updateProductName(item);
    focusQuantityInput();
    toggleHighlight(item);
  });
});

// Tüm ürünlerin üzerindeki seçimi kaldırın ve ardından seçilen ürünü işaretleyin
function clearAndSelectItem(selectedItem) {
  document
    .querySelectorAll(".product-item.selected")
    .forEach((el) => el.classList.remove("selected"));
  selectedItem.classList.add("selected");
}

// Seçilen ürünün adını güncelleyen işlev
function updateProductName(selectedItem) {
  const productName = selectedItem.textContent.trim();
  document.getElementById("selected-product-name").textContent = productName;
}

// Miktar giriş kutusuna odaklanan işlev
function focusQuantityInput() {
  document.getElementById("quantity").focus();
}

// Seçilen ürünün kutucuğunun rengini güncelleyen işlev
function toggleHighlight(selectedItem) {
  if (document.getElementById("quantity").value.trim() === "") return;
  selectedItem.classList.toggle("highlight");
  document.querySelectorAll(".product-item").forEach((item) => {
    if (item !== selectedItem) item.classList.remove("highlight");
  });
}

// Ürün ve miktarını tutan nesne
let orderTable = {};
let orders = [];

// Sipariş ekleme işlevi
function addOrder() {
  var selectedProductName = document.getElementById(
    "selected-product-name"
  ).innerText;
  var productQuantity = document.getElementById("quantity").value;
  const quantityInput = document.getElementById("quantity");
  const quantity = parseFloat(quantityInput.value);

  // Yeni siparişi oluştur
  const newOrder = {
    product: selectedProductName,
    quantity: quantity,
  };

  // Siparişi dizinin başına ekle
  orders.unshift(newOrder);

  // Eğer sipariş sayısı üçten fazla ise, en eskisini çıkar
  if (orders.length > 3) {
    orders.pop();
  }

  orderTable[selectedProductName] =
    (orderTable[selectedProductName] || 0) + quantity;

  updateProductDisplay(selectedProductName, orderTable[selectedProductName]);

  updateOrderTotal();
  resetOrderInputs();
  updateLastOrders();
}

function updateLastOrders() {
  // Son siparişleri göstermek için HTML elementlerini temizle
  const lastAddedItems = document.getElementById("last-added-item");
  lastAddedItems.innerHTML = "";

  // Son üç siparişi ekrana yazdır
  orders.slice(0, 3).forEach((order, index) => {
    const orderElement = document.createElement("div");
    orderElement.textContent = `${index + 1}. Ürün: ${order.product}, Adet: ${
      order.quantity
    }`;
    lastAddedItems.appendChild(orderElement);
  });
}

// Ürün gösterimini güncelleme işlevi
function updateProductDisplay(productName, quantity) {
  const productItems = document.querySelectorAll(".product-item");
  productItems.forEach((item) => {
    if (item.textContent.trim() === productName) {
      const quantityDisplay =
        item.nextElementSibling.querySelector(".quantity");
      quantityDisplay.textContent = quantity;
      item.style.backgroundColor = quantity > 0 ? "#dbc310" : "";
    }
  });
}

// Toplam sipariş miktarını güncelleme işlevi
function updateOrderTotal() {
  const totalOrders = Object.values(orderTable).reduce(
    (total, quantity) => total + quantity,
    0
  );
  document.getElementById("total-orders").textContent = totalOrders;
}

// Siparişin geçerliliğini kontrol eden işlev
function isValidOrder(productName, quantity) {
  if (productName === "---" || isNaN(quantity)) {
    alert("Lütfen geçerli bir ürün seçin ve miktar giriniz.");
    return false;
  }
  return true;
}

// Seçilen ürün ve miktar girişini sıfırlama işlevi
function resetOrderInputs() {
  document.getElementById("selected-product-name").textContent = "---";
  document.getElementById("quantity").value = "";
}

// Miktar giriş kutusunun olay dinleyicilerini ayarlayın
function setupQuantityInputListeners() {
  const selectedProductNameElement = document.getElementById(
    "selected-product-name"
  );
  const quantityInput = document.getElementById("quantity");

  selectedProductNameElement.addEventListener("click", () => {
    quantityInput.disabled = false;
  });

  quantityInput.addEventListener("blur", () => {
    if (selectedProductNameElement.textContent === "---") {
      quantityInput.value = "";
    }
  });

  quantityInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") addOrder();
  });
}

// Seçilen ürün miktarını ve toplam sipariş adedini güncelleme
function updateQuantityTable(productName, quantity) {
  const productItem = document.querySelector(
    `.product-item[data-name="${productName}"]`
  ); // Ürün adına göre doğru ürünü seç
  const quantityDisplay = productItem.querySelector(".quantity");
  quantityDisplay.textContent =
    (parseFloat(quantityDisplay.textContent) || 0) + quantity;

  updateOrderTotal();
}

// Sipariş butonunu dinleyin
document.querySelector(".order-button").addEventListener("click", addOrder);

// Miktar giriş kutusu için olay dinleyicilerini kurun
setupQuantityInputListeners();

const selectedDateInput = document.getElementById("selected-date");

// Tarih seçici değeri değiştiğinde
selectedDateInput.addEventListener("change", () => {
  document.getElementById("selected-date-display").textContent =
    selectedDateInput.value;
});

// Miktar giriş kutusunun "input" olayını dinle
document.getElementById("quantity").addEventListener("input", function () {
  updateProductItemColor(this.value);
});

// Eğer miktar 0'dan farklıysa, ürün kutusunun rengini değiştir
function updateProductItemColor(quantity) {
  const productItem = document.querySelector(".product-item.selected");
  if (productItem) {
    productItem.style.backgroundColor = quantity != 0 ? "#dbc310" : ""; // Varsayılan rengi geri yükleyin
  }
}

// Yapışkan navigasyon (Sticky Navigation) için IntersectionObserver
const orderDetails = document.querySelector(".order-details");
const headerObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      orderDetails.classList.toggle("sticky", !entry.isIntersecting);
    });
  },
  { root: null, threshold: 0 }
);

headerObserver.observe(document.querySelector(".header")); // Hedef olarak .header seçildi

// Sayfa yüklendikten sonra ürün konteynerine olay delegasyonu uygulayın
document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelector(".product-container")
    .addEventListener("input", (e) => {
      if (e.target && e.target.classList.contains("quantity")) {
        const productItem = e.target.closest(".product-quantity-table");
        const quantity = parseFloat(e.target.value);
        updateProductBoxColorBasedOnQuantity(productItem, quantity);
      }
    });
});

// Miktar bazında ürün kutusunun rengini güncelleme işlevi
function updateProductBoxColorBasedOnQuantity(productItem, quantity) {
  productItem.style.backgroundColor = quantity > 0 ? "#dbc310" : "";
}

// Tema değişikliği işlevi
function themeChange() {
  document.body.classList.toggle("dark");
  document
    .querySelectorAll(
      ".product-item, .quantity-container, .product-title, .selected-product, .total, .DerasHeader, .selected-date, .last-item"
    )
    .forEach((element) => element.classList.toggle("dark"));

  const logo = document.querySelector(".logo");
  if (logo) logo.classList.toggle("logo-dark-mode");
}
